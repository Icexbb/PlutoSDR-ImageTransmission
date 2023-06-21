# -*- coding: utf-8 -*-


import socket
import sys
import threading
from multiprocessing import Manager

sys.path.append('..')

from ofdm.ofdm_utils import OfdmConfig
from ofdm.pluto_interface import pluto_receiver
from ofdm.support import *

class OfdmRx(threading.Thread):
    def __init__(self, rx_type, rx_args,
                 n=64, cp_len=16, qam_mod_size=2, pilot_pattern='custom', preamble_type='802.11', num_symbol=100,
                 verbose=False):
        """ OFDM receiver
        :param rx_type:                 'pluto', 'socket'
        :param rx_args:                 including parameters below
                    rx_args:            PlutoSDR device ip address
                    rx_freq:            center frequency
                    bandwidth:          bandwidth/sample rate in Hz
                    rx_gain:            reception gain in dB ([0, 75]dB)
                    rx_buffer_size:     reception buffer size of PlutoSDR device
                    gain_control_mode:  'manual', 'fast_attack', 'slow_attack'
        :param n:                       the DFT size in OFDM
        :param cp_len:                  length of the cyclic prefix
        :param qam_mod_size:            size of the constellation of QAM modulation
        :param pilot_pattern:           'comb', 'staggered', 'custom'
        :param preamble_type:           only '802.11' is supported
        :param num_symbol:              the number of ofdm symbols
        :param verbose:                 print PHY-layer info
        """
        # Rx params
        threading.Thread.__init__(self)
        self.rx_sample_queue = Manager().Queue()  # raw samples from PlutoSDR device
        self.rx_sample_queue_size = 20
        self.rx_packet_queue = Manager().Queue()  # packet bits
        self.rx_packet_queue_size = 20
        self.rx_type = rx_type
        self.preamble_lts = np.load("preamble_lts.npy")
        if self.rx_type == "pluto":
            rx_args, rx_freq, bandwidth, rx_gain, rx_buffer_size, gain_control_mode = rx_args
            sdr_rx = pluto_receiver(rx_args, rx_freq, bandwidth, rx_gain, rx_buffer_size,
                                    gain_control_mode, verbose=True).pluto
            self.rx_sample_queue_watcher_thread = rx_sample_queue_watcher_thread(sdr_rx,
                                                                                 self.rx_sample_queue,
                                                                                 self.rx_sample_queue_size,
                                                                                 verbose=verbose)
        elif self.rx_type == "socket":
            rx_ipaddr, rx_port = rx_args
            self.rx_packet_queue_watcher_thread = rx_packet_queue_watcher_thread(rx_ipaddr, rx_port,
                                                                                 self.rx_packet_queue,
                                                                                 self.rx_packet_queue_size,
                                                                                 verbose=verbose)
        else:
            raise ValueError("Invalid rx type.")

        # OFDM params
        self.ofdm_config = OfdmConfig(n, cp_len, qam_mod_size, pilot_pattern)  # type: OfdmConfig
        self.preamble_type = preamble_type
        self.num_symbol = num_symbol
        self.pilot_index = [7, 21, 43, 57]                    # note: data are arranged in this order
        self.data_index = list(range(1,7))+list(range(8,21))+list(range(22,27))+list(range(38,43))+list(range(44,57))+list(range(58,64))
        self.index=list(range(64))   # note: data are arranged in this order
        self.nbits = num_symbol * 48
        self.preamble_lts = np.load("preamble_lts.npy")  
        self.preamble_sts = np.load("preamble_sts.npy")
        self.lts_frequency = np.fft.fft(self.preamble_lts, 64)
        self.prev_samples = np.array([])
        self.packet_length = self.ofdm_config.preamble_sts_len + self.ofdm_config.preamble_lts_len + \
                             self.num_symbol * self.ofdm_config.sym_len

        self.verbose = verbose
        self.nrx = 0
        self.nrxok = 0

        self.keep_running = True
        self.start()

    def done(self):
        self.keep_running = False

    def run(self):
        """ thread for sample process
        """
        if self.rx_type == "pluto":
            while self.keep_running:
                self.process()
        elif self.rx_type == "socket":
            return

    def get(self):
        """ interface for upper layers
        """
        return self.rx_packet_queue.get() if not self.rx_packet_queue.empty() else None

    def process(self):
        """ Demodulate received samples and put packet into rx_packet_queue """
        signal = self.rx_sample_queue.get()
        index = detect_preamble_cross_correlation(self.preamble_lts, signal)
        if index is not None:
            if index  > 1680:
                signal1 = self.rx_sample_queue.get()
                signal = np.hstack((signal[index:], signal1[0:index]))
                index = 0
            #print(index)
            #np.save("signal.npy", signal)
            start_pos = index
            rx_samples = signal[start_pos:start_pos+64*2+self.num_symbol*80-1]
            rx_samples_lts_raw = rx_samples[0:127]
            cfo = cfo_estimation(rx_samples_lts_raw)

            # #cfo compensation
            for i in range(len(rx_samples)):
                rx_samples[i] = rx_samples[i]* np.exp( -1j * 2 * np.pi * cfo * i)

            # #channel estimation by preamble
            rx_samples_lts = rx_samples[0:127]
            h_tilde = channel_estimation(rx_samples_lts, self.index, self.lts_frequency)

            # #demodulation

            rx_samples_data = rx_samples[128:-1]
            demod_signal,p = detfcount(rx_samples_data,h_tilde,self.num_symbol,self.pilot_index,self.data_index)
            """ Put packet to FIFO queue """
            if self.rx_packet_queue.qsize() > self.rx_packet_queue_size:
                self.rx_packet_queue.get()
            self.rx_packet_queue.put(demod_signal)


class rx_sample_queue_watcher_thread(threading.Thread):
    """ Rx Queue Monitor
    """

    # TODO
    def __init__(self, sdr_rx, rx_queue, rx_queue_size, verbose=False):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.keep_running = True
        self.sdr_rx = sdr_rx
        self.rx_queue = rx_queue
        self.rx_queue_size = rx_queue_size
        self.verbose = verbose
        self.start()

    def done(self):
        self.keep_running = False

    def run(self):
        while self.keep_running:
            try:
                """ Put packet to FIFO queue """
                if self.rx_queue.qsize() > self.rx_queue_size:
                    self.rx_queue.get()
                self.rx_queue.put_nowait(self.sdr_rx.rx())
                if self.verbose:
                    # can be used to check if rx queue is processed timely
                    pass
                    #print("[PlutoRxQueue] RX queue size: {}".format(self.rx_queue.qsize()))
            except:
                break


class rx_packet_queue_watcher_thread(threading.Thread):
    """ Rx Queue Monitor
    """

    def __init__(self, rx_ipaddr, rx_port, rx_queue, rx_queue_size, verbose=False):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.keep_running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rx_ipaddr = rx_ipaddr
        self.rx_port = rx_port
        self.sock.bind((self.rx_ipaddr, self.rx_port))
        self.rx_queue = rx_queue
        self.rx_queue_size = rx_queue_size
        self.verbose = verbose
        self.start()

    def done(self):
        self.keep_running = False

    def run(self):
        while self.keep_running:
            try:
                """ Put packet to FIFO queue """
                if self.rx_queue.qsize() > self.rx_queue_size:
                    self.rx_queue.get()
                # byte->decimal->bit
                data_bits = np.unpackbits(np.frombuffer(self.sock.recvfrom(10240)[0], dtype=np.uint8))
                self.rx_queue.put_nowait(data_bits)
                if self.verbose:
                    # can be used to check if rx queue is processed timely
                    print("[SocketRxQueue] RX queue size: {}".format(self.rx_queue.qsize()))
            except:
                self.sock.close()
                break

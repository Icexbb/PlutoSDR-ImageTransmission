# -*- coding: utf-8 -*-

"""OFDM transmitter.

"""

# compatibility of Python 2/3
from __future__ import division
from __future__ import print_function

import sys
import threading
from multiprocessing import Manager

import numpy as np

sys.path.append('..')

from lib.ofdm.ofdm_utils import OfdmConfig
from lib.ofdm.pluto_interface import pluto_transmitter


class OfdmTx(object):
    def __init__(self, tx_type, tx_args,
                 n=64, cp_len=16, qam_mod_size=2, pilot_pattern='custom', preamble_type='802.11', num_symbol=100,
                 verbose=False):
        """ OFDM transmitter
        :param tx_type:             'pluto', 'socket'
        :param tx_args:             including parameters below
                    tx_ipaddr:      PlutoSDR device ip address
                    tx_freq:        center frequency
                    bandwidth:      bandwidth/sample rate in Hz
                    tx_gain:        transmission gain in dB ([-90, 0]dB)
        :param n:                   the DFT size in OFDM
        :param cp_len:              length of the cyclic prefix
        :param qam_mod_size:        size of the constellation of QAM modulation
        :param pilot_pattern:       'comb', 'staggered', 'custom'
        :param preamble_type:       only '802.11' is supported
        :param num_symbol:          the number of ofdm symbols
        :param verbose:             print PHY-layer info
        """
        # Tx params
        self.tx_queue = Manager().Queue()  # thread safe
        self.tx_queue_size = 20
        self.tx_type = tx_type
        if self.tx_type == "pluto":
            tx_ipaddr, tx_freq, bandwidth, tx_gain = tx_args
            sdr_tx = pluto_transmitter(tx_ipaddr, tx_freq, bandwidth, tx_gain, verbose=True).pluto
            self.tx_sample_queue_watcher_thread_pluto = tx_sample_queue_watcher_thread_pluto(sdr_tx,
                                                                                             self.tx_queue,
                                                                                             self.tx_queue_size,
                                                                                             verbose=verbose)
        elif self.tx_type == "socket":
            tx_ipaddr, tx_port = tx_args
            self.tx_sample_queue_watcher_thread_socket = tx_sample_queue_watcher_thread_socket(tx_ipaddr, tx_port,
                                                                                               self.tx_queue,
                                                                                               self.tx_queue_size,
                                                                                               verbose=verbose)
        else:
            raise ValueError("Invalid tx type.")

        # OFDM params
        self.ofdm_config = OfdmConfig(n, cp_len, qam_mod_size, pilot_pattern)  # type: OfdmConfig
        self.preamble_type = preamble_type
        self.num_symbol = num_symbol
        self.packet_bit_size = 48 * num_symbol
        self.verbose = verbose

    def put(self, bin_message):
        """ interface for upper layers """
        if self.tx_type == "pluto":
            self.tx_queue.put(bin_message)

        elif self.tx_type == "socket":
            # put packet for socket
            # TODO: You should modulate the frames into baseband samples
            pass

    def process(self, bin_message, is_with_preamble=True):
        """Calculate the time-domain samples to be transmitted
        :param bin_message:         (numpy.array) binary message array
        :param is_with_preamble:    (boolean) whether to use the preamble
        :return: (numpy.array) baseband time-domain samples to be transmitted
        """
        encoded = bin_message
        # zero-padding the encoded to fill a multiple of OFDM symbols
        encoded = np.concatenate((encoded, np.zeros(
            (self.ofdm_config.n_cbps - encoded.size % self.ofdm_config.n_cbps) % self.ofdm_config.n_cbps, dtype=int)))
        assert encoded.size % self.ofdm_config.n_cbps == 0

        """ QAM Modulation """
        modulated = self.ofdm_config.qam_mod.modulate(encoded) / self.ofdm_config.qam_mod.qam_max_axis
        modulated_len = modulated.size

        """ frequency domain: fill in data and pilots """
        ofdm_sym_num = self.ofdm_config.how_many_symbols(modulated_len)  # the OFDM symbol number that can hold the data
        all_sc = np.zeros((self.ofdm_config.n, ofdm_sym_num), dtype=complex)
        pilot_index_array, data_index_array = self.ofdm_config.ofdm_pilot.get_index_array_at_symbol(
            np.array(range(0, ofdm_sym_num)))
        all_sc[pilot_index_array] = self.ofdm_config.training_signal_freq[pilot_index_array[0]]
        all_sc[data_index_array] = np.concatenate(
            (modulated, np.zeros(len(data_index_array[0]) - modulated_len, dtype=complex)))

        """ IFFT: freq domain to time domain """
        time_symbols = np.fft.ifft(all_sc, n=self.ofdm_config.n, axis=0)

        """ cyclic prefix (CP) """
        time_symbols_cp = np.concatenate((time_symbols[-self.ofdm_config.cp_len:, :], time_symbols), axis=0)
        # serialization
        ofdm_symbols = np.reshape(time_symbols_cp, (self.ofdm_config.sym_len * ofdm_sym_num,), order='F')

        """ packet format: preamble + OFDM symbols
        10 STS + 2 LTS as the preamble
        """
        if is_with_preamble:
            tx_packet = np.concatenate((self.ofdm_config.preamble, ofdm_symbols))
        else:
            tx_packet = ofdm_symbols

        assert tx_packet.size % self.ofdm_config.sym_len == 0

        return tx_packet


class tx_sample_queue_watcher_thread_pluto(threading.Thread):
    """ TX Sample Queue Monitor
    """

    def __init__(self, sdr_tx, tx_queue, tx_queue_size, verbose=False):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.ntx = 0
        self.tx_queue = tx_queue
        self.tx_queue_size = tx_queue_size
        self.verbose = verbose
        self.sdr_tx = sdr_tx
        # self.sdr_tx.tx_cyclic_buffer = False

        self.keep_running = True
        self.start()

    def done(self):
        self.keep_running = False

    def run(self):
        while self.keep_running:
            try:
                if self.tx_queue.qsize() > self.tx_queue_size:
                    self.tx_queue.get()
                if not self.tx_queue.empty():
                    # bit->decimal->byte
                    # data_bytes = bytes(np.packbits(self.tx_queue.get()))
                    data_bytes = self.tx_queue.get()
                    self.sdr_tx.tx(data_bytes)
                    if self.verbose:
                        self.ntx += 1
                        print("[SocketTx] TX: ntx={}".format(self.ntx))
            except Exception as e:
                print('stop')
                raise e
                break


class tx_sample_queue_watcher_thread_socket(threading.Thread):
    """ TX UDP Packet Queue Monitor
    """
    # TODO:You should get the complex samples and convert them into bytes
    pass

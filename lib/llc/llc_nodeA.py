# -*- coding: utf-8 -*-
# @Author  : Zhirong Tang
# @Time    : 2022/4/14 20:22

""" Basic version of LLC-layer transmitter
"""

import sys
import threading
import time

import numpy as np

sys.path.append('..')

from lib.ofdm.ofdm_tx import OfdmTx
from lib.ofdm.ofdm_rx import OfdmRx
from lib.llc.llc_utils import calc_crc32, check_crc32, dec2bin, bin2dec


class NodeALLC(threading.Thread):
    def __init__(self, ofdm_tx, ofdm_rx, packet_bit_size=20 * 48):
        """ LLC-layer transmitter side
        :param ofdm_tx:         physical-layer ofdm transmitter instance
        :param ofdm_rx:         physical-layer ofdm receiver instance
        :param packet_bit_size: # of bits within a frame
        """
        threading.Thread.__init__(self)

        # PHY-layer parameters
        self.ofdm_tx = ofdm_tx  # type: OfdmTx
        self.ofdm_rx = ofdm_rx  # type: OfdmRx

        # LLC-layer frame parameters
        self.packet_bit_size = packet_bit_size
        self.crc_bit_size = 32

        # LLC-layer tx parameters
        self.ntx = 0
        self.tx_seq_no = 0

        # LLC-layer rx counters
        self.nrx = 0
        self.nrxok = 0
        self.ack = 0
        self.rtt = 0
        self.pkt_loss = 100
        self.avg_rtt = 0
        self.tot_rtt = 0

        self.keep_running = True

    def done(self):
        self.keep_running = False

    def run(self):
        while self.keep_running:
            self.recv(arq_mode="stop-and-wait-ARQ")

    def send(self, tx_pkt, pkt_size, num_frame, is_dbl_link=False, arq_mode="null-ARQ", pause=0.1):
        if arq_mode == "null-ARQ":
            if is_dbl_link:
                # start thread to receive ACK
                self.start()
            while self.keep_running:
                random_bit_size = self.packet_bit_size - self.crc_bit_size
                frame = np.random.randint(low=0, high=2, size=random_bit_size)
                # add crc32 for error detection, which is actually done by LLC layer
                crc = calc_crc32(frame)
                frame = np.concatenate((frame, crc))
                self.ofdm_tx.put(frame)

                self.ntx += 1
                print("[NodeA] LLCTx: ntx={}".format(self.ntx))
                time.sleep(pause)

        elif arq_mode == "stop-and-wait-ARQ":
            # TODO: 实现stop-and-wait-ARQ protocol
            # - 提取数据, 生成协议的header
            if is_dbl_link:
                # start thread to receive ACK
                self.start()
            while self.keep_running:
                frame = tx_pkt[self.ntx * pkt_size: (self.ntx + 1) * pkt_size]
                # add crc32 for error detection, which is actually done by LLC layer
                # frame_len=dec2bin(len(frame))
                frame_num = dec2bin(self.ntx, 16)
                # frame = np.concatenate((frame_len,frame))
                frame = np.concatenate((frame_num, frame))
                crc = calc_crc32(frame)
                frame = np.concatenate((frame, crc))
                # np.save("frame.npy", frame)
                frame = self.ofdm_tx.process(frame)
                frame = frame * (2 ** 14)
                self.ofdm_tx.put(frame)
                print("[NodeA] LLCTx: ntx={}".format(self.ntx))
                time.sleep(pause)

    def recv(self, arq_mode):
        frame = self.ofdm_rx.get()
        if frame is None:
            return
        if arq_mode == "null-ARQ":
            if check_crc32(frame.flatten()):
                self.nrxok += 1
                self.nrx += 1
                print("[NodeA] LLCRx: pkt=ok, nrxok={}, nrx={}".format(self.nrxok, self.nrx))
            else:
                self.nrx += 1
                print("[NodeA] LLCRX: pkt=false, nrxok={}, nrx={}".format(self.nrxok, self.nrx))

        if arq_mode == "stop-and-wait-ARQ":
            # TODO: 实现stop-and-wait-ARQ protocol
            # - 提取frame的其他字段, 处理协议流程; 处理数据
            frame = frame.flatten()
            if check_crc32(frame):
                rxnum = bin2dec(np.array2string(frame[0:16]).translate({ord(i): None for i in '[] '}))
                if rxnum == self.ntx:
                    self.nrxok += 1
                    self.ntx += 1
                print("[NodeA] LLCRX: pkt=ok, nrxok={}, ntx_next={}".format(self.nrxok, self.ntx))
            else:
                self.nrx += 1
                print("[NodeA] LLCRX: pkt=false, nrxok={}, nrx={}".format(self.nrxok, self.nrx))

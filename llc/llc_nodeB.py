# -*- coding: utf-8 -*-
# @Author  : Zhirong Tang
# @Time    : 2022/4/14 20:22

""" Basic version of double-link LLC-layer receiver
"""

import sys
import threading

import numpy as np

sys.path.append('..')

from ofdm.ofdm_tx import OfdmTx
from ofdm.ofdm_rx import OfdmRx
from llc.llc_utils import calc_crc32, check_crc32, simu_pkt_loss_delay, dec2bin, bin2dec


class NodeBLLC(threading.Thread):
    def __init__(self, ofdm_tx, ofdm_rx, packet_bit_size=20 * 48):
        """ LLC-layer receiver side
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

        # LLC-layer rx counters
        self.nrx = 0
        self.nrxok = 0
        self.keep_running = True

    def done(self):
        self.keep_running = False

    # def run(self):
    #     while self.keep_running:
    #         self.ack(phy_type="pluto",arq_mode="stop-and-wait-ARQ")

    def recv(self, pkt_size, num_frame, phy_type="pluto", is_dbl_link=True, arq_mode="null-ARQ"):
        rx_pkt = [0] * num_frame * pkt_size
        while self.keep_running:
            frame = self.ofdm_rx.get()
            if frame is None:
                # print("frame none")
                continue
            # np.save("jietiao",frame)
            if phy_type == "socket":
                # packet loss and delay emulator
                is_not_dropped = simu_pkt_loss_delay()
                if not is_not_dropped:
                    print("[NodeB] !!! {frame} dropped !!!")
                    continue

            if arq_mode == "null-ARQ":
                if check_crc32(frame):
                    self.nrxok += 1
                    self.nrx += 1
                    print("[NodeB] LLCRx: pkt=ok, nrxok={}, nrx={}".format(self.nrxok, self.nrx))
                else:
                    self.nrx += 1
                    print("[NodeB] LLCRx: pkt=false, nrxok={}, nrx={}".format(self.nrxok, self.nrx))

                if is_dbl_link:
                    self.ack(phy_type, arq_mode)

            if arq_mode == "stop-and-wait-ARQ":
                # TODO: 实现stop-and-wait-ARQ protocol
                # - 提取header处理协议流程
                # - 提取并处理frame的数据;
                # np.save('jietiao.npy',frame)
                frame = frame.flatten()
                if check_crc32(frame):
                    num_frame = 33
                    self.nrx = bin2dec(np.array2string(frame[0:16]).translate({ord(i): None for i in '[] '}))
                    # frame_len = bin2dec(np.array2string(frame[32:64]).translate({ord(i):None for i in '[] '}))
                    pyload = frame[16:16 + pkt_size]
                    rx_pkt[self.nrx * pkt_size: (self.nrx + 1) * pkt_size] = pyload
                    self.nrxok += 1
                    print("[NodeB] LLCRx: pkt=ok, nrxok={}, nrx={}".format(self.nrxok, self.nrx))
                    self.nrx += 1
                else:
                    self.nrxok += 1
                    print("[NodeB] LLCRx: pkt=false, nrxok={}, nrx={}".format(self.nrxok, self.nrx))
                if self.nrx >= num_frame - 1:
                    print("saving...")
                    # np.save('rx_pkt.npy', rx_pkt)
                    # save_image(rx_pkt, r'recv.jpg')
                    return rx_pkt
                if is_dbl_link:
                    self.ack(phy_type, arq_mode)
                # np.save('frame.npy',frame)

    def ack(self, phy_type="pluto", arq_mode="null-ARQ"):
        if phy_type == "socket":
            # packet loss and delay emulator
            is_not_dropped = simu_pkt_loss_delay()
            if not is_not_dropped:
                print("[NodeB] !!! {ack} dropped !!!")
                return

        if arq_mode == "null-ARQ":
            random_bit_size = self.packet_bit_size - 32
            frame = np.random.randint(low=0, high=2, size=random_bit_size)
            # add crc32 for error detection, which is actually done by LLC layer
            crc = calc_crc32(frame)
            frame = np.concatenate((frame, crc))
            self.ofdm_tx.put(frame)

            self.ntx += 1
            print("[NodeB] LLCTx: ntx={}".format(self.ntx))
        elif arq_mode == "stop-and-wait-ARQ":
            # TODO: 实现stop-and-wait-ARQ protocol
            # - 生成ack frame
            self.ntx = self.nrx - 1
            frame = dec2bin(self.ntx, 16)
            # frame = np.pad(frame,(0,4752),'constant')
            crc = calc_crc32(frame)
            frame = np.concatenate((frame, crc))
            # np.save('ack.npy',frame)
            # add crc32 for error detection, which is actually done by LLC layer
            self.ofdm_tx.put(frame)
            print("[NodeB] LLCTx: ntx={}".format(self.ntx))

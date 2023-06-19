import math

from PySide6 import QtCore

from lib.llc.llc_nodeA import NodeALLC
from lib.llc.llc_nodeB import NodeBLLC
from lib.ofdm.ofdm_rx import OfdmRx
from lib.ofdm.ofdm_tx import OfdmTx
from lib.test_read_save_img import read_image, save_image

PKT_SIZE = 100 * 48 - 64 - 32
PHY_TYPE = "pluto"
ARQ_MODE = "stop-and-wait-ARQ"
FREQ = 1105e6


class ReceiveThread(QtCore.QThread):
    def __init__(self, filepath: str, plutoIP: str, frameCount: int):
        super().__init__()
        self.llc = None
        self.filepath = filepath
        self.plutoIP = plutoIP
        self.frameCount = frameCount

        self.initLLC()

    def initLLC(self):
        # Parameters for OFDM PHY
        n = 64
        cp = 16
        qam_size = 2
        pilot_pattern = 'custom'
        preamble_type = '802.11'
        tx_num_symbol = 1
        # tx_packet_bit_size = tx_num_symbol * 48
        rx_num_symbol = 100
        rx_packet_bit_size = rx_num_symbol * 48

        # Parameters for PlutoSDR device
        tx_ipaddr = f"ip:{self.plutoIP}"
        tx_freq = FREQ
        bandwidth = 1e6
        tx_gain = -20
        tx_args = [tx_ipaddr, tx_freq, bandwidth, tx_gain]

        rx_args = f"ip:{self.plutoIP}"
        rx_freq = FREQ
        bandwidth = 1e6
        rx_gain = 0
        rx_buffer_size = 1e4
        gain_control_mode = "fast_attack"
        rx_args = [rx_args, rx_freq, bandwidth, rx_gain, rx_buffer_size, gain_control_mode]

        phy_rx = OfdmRx(PHY_TYPE, rx_args,
                        n, cp, qam_size, pilot_pattern, preamble_type, rx_num_symbol, verbose=True)

        print("Test double-direction LLC-layer")
        phy_tx = OfdmTx(PHY_TYPE, tx_args,
                        n, cp, qam_size, pilot_pattern, preamble_type, tx_num_symbol, verbose=True)
        llc_rx = NodeBLLC(phy_tx, phy_rx, rx_packet_bit_size)
        self.llc = llc_rx

    def run(self) -> None:
        rx_pkt = self.llc.recv(PKT_SIZE, self.frameCount, PHY_TYPE, is_dbl_link=True, arq_mode=ARQ_MODE)
        save_image(rx_pkt, self.filepath)


class TransmitThread(QtCore.QThread):
    def __init__(self, filepath: str, plutoIP: str):
        super().__init__()
        self.llc = None
        self.filepath = filepath
        self.plutoIP = plutoIP

        # tx
        self.tx_pkt = list(read_image(self.filepath))
        self.num_frame = math.ceil(len(self.tx_pkt) / PKT_SIZE)
        self.initLLC()

    def initLLC(self):
        # Parameters for OFDM PHY
        n = 64
        cp = 16
        qam_size = 2
        pilot_pattern = 'custom'
        preamble_type = '802.11'
        tx_num_symbol = 100
        tx_packet_bit_size = tx_num_symbol * 48
        rx_num_symbol = 1
        # rx_packet_bit_size = rx_num_symbol * 48

        # Parameters for PlutoSDR device
        tx_ipaddr = f"ip:{self.plutoIP}"
        tx_freq = FREQ
        bandwidth = 1e6
        tx_gain = -20
        tx_args = [tx_ipaddr, tx_freq, bandwidth, tx_gain]

        rx_args = f"ip:{self.plutoIP}"
        rx_freq = FREQ
        bandwidth = 1e6
        rx_gain = 0
        rx_buffer_size = 1e4
        gain_control_mode = "fast_attack"
        rx_args = [rx_args, rx_freq, bandwidth, rx_gain, rx_buffer_size, gain_control_mode]
        phy_tx = OfdmTx(PHY_TYPE, tx_args,
                        n, cp, qam_size, pilot_pattern, preamble_type, tx_num_symbol, verbose=True)

        print("Test double-direction LLC-layer")
        phy_rx = OfdmRx(PHY_TYPE, rx_args,
                        n, cp, qam_size, pilot_pattern, preamble_type, rx_num_symbol, verbose=True)
        llc_tx = NodeALLC(phy_tx, phy_rx, tx_packet_bit_size)
        self.llc = llc_tx

    def run(self) -> None:
        self.llc.send(self.tx_pkt, PKT_SIZE, self.num_frame, is_dbl_link=True, arq_mode=ARQ_MODE)

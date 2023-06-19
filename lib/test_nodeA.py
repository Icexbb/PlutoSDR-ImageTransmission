# -*- coding: utf-8 -*-
# @Author  : Zhirong Tang, Lizhao You
# @Email   : ttangzr@stu.xmu.edu.cn, lizhaoyou@xmu.edu.cn
# @Time    : 2022/4/13 15:03, 2023/2/14 20:05

""" Test LLC-layer node A
"""

import sys

sys.path.append('..')
import getopt
import math
from ofdm import OfdmTx
from ofdm import OfdmRx
from llc import NodeALLC
from test_read_save_img import read_image, extract_image_info


def test_nodeA():
    """ LLC-layer node A
    """
    phy_type = "socket"
    llc_type = "double"
    arq_mode = "null-ARQ"

    opts = None
    try:
        argv = sys.argv[1:]
        opts, args = getopt.getopt(argv, "p:l:a", ["phy-type=", "llc-type=", "arq-mode="])
    except Exception as e:
        print("Exception: ", e)

    for opt, arg in opts:
        if opt in ['-p', '--phy-type']:
            phy_type = arg
        elif opt in ['-l', '--llc-type']:
            llc_type = arg
        elif opt in ['-a', '--arq-mode']:
            arq_mode = arg

    # Parameters for OFDM PHY
    n = 64
    cp = 16
    qam_size = 2
    pilot_pattern = 'custom'
    preamble_type = '802.11'
    tx_num_symbol = 100
    tx_packet_bit_size = tx_num_symbol * 48
    rx_num_symbol = 1
    rx_packet_bit_size = rx_num_symbol * 48

    pkt_size = 100 * 48 - 16 - 32

    # tx
    tx_pkt = list(read_image(r'xmu3.jpg'))
    width, height, greyLevel = extract_image_info(tx_pkt)
    num_frame = math.ceil(len(tx_pkt) / pkt_size)
    if phy_type == "socket":
        # Parameters for UDP socket
        tx_ipaddr = "127.0.0.1"
        tx_port = 52002
        tx_args = [tx_ipaddr, tx_port]

        rx_ipaddr = "127.0.0.1"
        rx_port = 52003
        rx_args = [rx_ipaddr, rx_port]
    elif phy_type == "pluto":
        # Parameters for PlutoSDR device
        tx_ipaddr = "ip:192.168.3.1"
        tx_freq = 1105e6  # TODO: modify it according to your group #
        bandwidth = 1e6
        tx_gain = -20
        tx_args = [tx_ipaddr, tx_freq, bandwidth, tx_gain]

        rx_args = "ip:192.168.3.1"
        rx_freq = 1115e6  # TODO: modify it according to your group #
        bandwidth = 1e6
        rx_gain = 0
        rx_buffer_size = 1e4
        gain_control_mode = "fast_attack"
        rx_args = [rx_args, rx_freq, bandwidth, rx_gain, rx_buffer_size, gain_control_mode]
    else:
        raise ValueError("Invalid PHY type!")

    phy_tx = OfdmTx(phy_type, tx_args,
                    n, cp, qam_size, pilot_pattern, preamble_type, tx_num_symbol, verbose=True)

    if llc_type == "single":
        print("Test single-direction LLC-layer")
        phy_rx = None
        llc_tx = NodeALLC(phy_tx, phy_rx, tx_packet_bit_size)
        llc_tx.send(is_dbl_link=False, arq_mode=arq_mode)
    elif llc_type == "double":
        print("Test double-direction LLC-layer")
        phy_rx = OfdmRx(phy_type, rx_args,
                        n, cp, qam_size, pilot_pattern, preamble_type, rx_num_symbol, verbose=True)
        llc_tx = NodeALLC(phy_tx, phy_rx, tx_packet_bit_size)
        llc_tx.send(tx_pkt, pkt_size, num_frame, is_dbl_link=True, arq_mode=arq_mode)
    else:
        raise ValueError("Invalid LLC type!")


if __name__ == '__main__':
    try:
        """ test with: python test_nodeA.py -p socket/pluto -l single/double -a null-ARQ/stop-and-wait-ARQ"""
        test_nodeA()
    except Exception as e:
        print("Exception: ", e)
        raise e

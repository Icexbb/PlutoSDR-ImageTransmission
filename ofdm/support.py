import numpy
import numpy as np
from matplotlib import pyplot


def findindex(m, windowsize, model, sigma):
    index = np.where(m > sigma)[0]
    if index.size <= 0:
        return None
    elif index.size == 1:
        return index[0]
    c = []
    mid = []
    left = []
    for i in range(len(index) - 1):
        if (index[i + 1] - index[i]) < windowsize:
            c.append(index[i])
        elif (index[i + 1] - index[i]) >= windowsize:
            c.append(index[i])
            mid.append(c[len(c) // 2])
            left.append(c[0])
            if i + 1 == index.size - 1:
                c.append(index[i + 1])
                mid.append(c[len(c) // 2])
                left.append(c[0])
            c = []
    if len(c) > 0:
        mid.append(c[len(c) // 2])
        left.append(c[0])
    if model == 0:
        return mid
    elif model == 1:
        return left
    else:
        print("error model!")
        return None


def detect_preamble_cross_correlation(preamble, signal):
    len1 = len(preamble)
    len2 = len(signal)
    pn1 = sum(preamble * preamble.conj())
    pn2 = np.convolve(abs(signal) ** 2, np.ones(len1))[len1 - 1:len2]
    c = np.abs(np.correlate(signal, preamble))
    p = np.sqrt(np.real(pn1 * pn2))
    m = c / p
    max_v = np.real(np.max(m))
    # 输出可视化结果
    # plt.plot(range(len(m)), m, 'b')
    # plt.title("cross correlation")
    # plt.show()
    if max_v > 0.7:
        return np.argmax(m)
    else:
        return None


def detect_preamble_auto_correlation(signal, short_preamble_len):
    L = short_preamble_len
    c = np.zeros((signal.shape[0], 1))
    p = np.zeros((signal.shape[0], 1))
    for k in range(signal.shape[0] - L - 1 - short_preamble_len):
        c[k] = numpy.absolute(np.dot(signal[k:k + short_preamble_len], signal[k + L:k + L + short_preamble_len].conj()))
        p[k] = np.sum(numpy.absolute(signal[k:k + short_preamble_len]) ** 2) * np.sum(
            numpy.absolute(signal[k + L:k + L + short_preamble_len].conj()) ** 2)
        # p[k]=np.sum(numpy.absolute(signal[k:k+L])**2)
    m = c[:signal.shape[0] - L - 1 - short_preamble_len] / np.sqrt(p[:signal.shape[0] - L - 1 - short_preamble_len])
    ##递归算法
    # c=np.zeros((signal.shape[0],1),dtype=complex)
    # p=np.zeros((signal.shape[0],1))
    # c[0]=np.dot(signal[0:short_preamble_len],signal[L:2*L].conj())
    # for k in range(signal.shape[0]-2*L):
    #     c[k+1]=c[k]+signal[k+L]*signal[k+2*L].conj()-signal[k]*signal[k+L].conj()
    #     p[k]=np.sum(numpy.absolute(signal[k:k+short_preamble_len])**2)*np.sum(numpy.absolute(signal[k+L:k+L+short_preamble_len].conj())**2)
    # m=numpy.absolute(c[:signal.shape[0]-2*L])/np.sqrt(p[:signal.shape[0]-2*L])
    pyplot.plot(m)
    pyplot.show()
    return findindex(m, 160, 1, 0.95)


def detect_preamble_by_energy(signal):
    # L=20
    np.zeros((signal.shape[0], 1))
    # for k in range(signal.shape[0]-1):
    #     c[k]=numpy.absolute(np.dot(signal[k:k+L],signal[k:k+L].conj()))
    #     c[k]=np.sum(numpy.absolute(signal[k:k+L])**2)
    c = numpy.absolute(signal) ** 2
    # c=c/(np.sum(signal-np.mean(signal))**2)
    # c=(c-min(c))/(max(c)-min(c))
    pyplot.plot(c)
    pyplot.show()
    return findindex(c, 160, 1, 200000)


def detect_preamble_by_sliding_window(signal, short_preamble_len):
    c = np.zeros((signal.shape[0], 1))
    d = np.zeros((signal.shape[0], 1))
    for k in range(signal.shape[0] - 2 * short_preamble_len):
        # c[k]=np.dot(signal[k:k+short_preamble_len],signal[k:k+short_preamble_len].conj())
        c[k] = np.sum(numpy.absolute(signal[k:k + short_preamble_len]) ** 2)
        d[k] = np.sum(numpy.absolute(signal[k + short_preamble_len:k + 2 * short_preamble_len]) ** 2)
        # d[k]=np.dot(signal[k+short_preamble_len:k+2*short_preamble_len],signal[k+short_preamble_len:k+2*short_preamble_len].conj())
    m = d[:signal.shape[0] - 2 * short_preamble_len] / c[:signal.shape[0] - 2 * short_preamble_len]
    pyplot.plot(m)
    pyplot.show()
    return list(np.asarray(findindex(m, 160, 0, 5)) + short_preamble_len)


def cfo_estimation(rx_samples_lts):
    preamble_lts_1 = rx_samples_lts[0:63]
    preamble_lts_2 = rx_samples_lts[64:127]
    lts_corr = np.sum(np.dot(preamble_lts_1.conj(), preamble_lts_2))
    cfo_comp = np.angle(lts_corr) / (2 * np.pi) / 64
    return cfo_comp


def detfcount(rx_samples_data, h_tilde, sym_num, pilot_index, data_index):
    demod = np.zeros((48 * sym_num, 1), dtype=np.uint8)
    np.zeros((1, 4), dtype=complex)
    # x=range(-21,22,14)
    for symi in range(sym_num):
        rx_data_samples_time = rx_samples_data[symi * 80 + 16: (symi + 1) * 80 - 1]
        rx_data_samples_freq = np.fft.fft(rx_data_samples_time, 64).reshape((-1, 1)) / h_tilde
        detf = np.unwrap(np.angle(rx_data_samples_freq[pilot_index]).T, discont=np.pi / 2, period=np.pi).T
        ff = np.polyfit(pilot_index, detf, 1).T  # fit a line to the data.  y=ax+b.  y=detf[k]

        phase = np.array((range(64))) * (ff[0][0]) + ff[0][1]
        rx_data_samples_freq = rx_data_samples_freq * np.exp(-1j * phase.reshape((-1, 1)))
        #    pyplot.scatter(rx_data_samples_freq.real,rx_data_samples_freq.imag)
        #    pyplot.yticks([-1,-0.5,0,0.5,1])
        #    pyplot.show()
        for subi in range(len(data_index)):
            dis0 = abs(-1 - rx_data_samples_freq[data_index[subi]])
            dis1 = abs(1 - rx_data_samples_freq[data_index[subi]])
            if dis0 > dis1:
                demod[subi + symi * len(data_index)] = 1
            else:
                demod[subi + symi * len(data_index)] = 0
    return demod, phase


def bpsk_demodulation(rx_samples_data, h_tilde, sym_num, data_index):
    demod = np.zeros((48 * sym_num, 1), dtype=complex)
    for symi in range(sym_num):
        rx_data_samples_time = rx_samples_data[symi * 80 + 16: (symi + 1) * 80 - 1]
        # 信道均衡
        rx_data_samples_freq = np.fft.fft(rx_data_samples_time, 64).reshape((-1, 1)) / h_tilde
        pyplot.scatter(rx_data_samples_freq.real, rx_data_samples_freq.imag)
        pyplot.show()
        for subi in range(len(data_index)):
            dis0 = abs(-1 - rx_data_samples_freq[data_index[subi]])
            dis1 = abs(1 - rx_data_samples_freq[data_index[subi]])
            if dis0 > dis1:
                demod[subi + symi * len(data_index)] = 1
            else:
                demod[subi + symi * len(data_index)] = 0
    return demod


def qpsk_demodulation(rx_samples_data, h_tilde, sym_num, pilot_index, data_index):
    demod = np.zeros((48 * 2 * sym_num, 1), dtype=complex)
    np.zeros((1, 4), dtype=complex)
    # x=range(-21,22,14)
    for symi in range(sym_num):
        rx_data_samples_time = rx_samples_data[symi * 80 + 16: (symi + 1) * 80 - 1]
        rx_data_samples_freq = np.fft.fft(rx_data_samples_time, 64).reshape((-1, 1)) / h_tilde
        detf = np.unwrap(np.angle(rx_data_samples_freq[pilot_index]).T, discont=np.pi / 2, period=np.pi).T
        ff = np.polyfit(pilot_index, detf, 1).T  # fit a line to the data.  y=ax+b.  y=detf[k]

        phase = np.array((range(64))) * (ff[0][0]) + ff[0][1]
        rx_data_samples_freq = rx_data_samples_freq * np.exp(-1j * phase.reshape((-1, 1)))
        #    pyplot.scatter(rx_data_samples_freq.real,rx_data_samples_freq.imag)
        #    pyplot.yticks([-1,-0.5,0,0.5,1])
        #    pyplot.show()
        for subi in range(len(data_index)):
            dis00 = abs(1 + 1j - rx_data_samples_freq[data_index[subi]])
            dis01 = abs(-1 + 1j - rx_data_samples_freq[data_index[subi]])
            dis11 = abs(-1 - 1j - rx_data_samples_freq[data_index[subi]])
            dis10 = abs(1 - 1j - rx_data_samples_freq[data_index[subi]])
            dis = [dis00, dis01, dis11, dis10]
            mindis = min(dis)
            if mindis == dis00:
                demod[(subi + symi * len(data_index)) * 2] = 1
                demod[(subi + symi * len(data_index)) * 2 + 1] = 1
            elif mindis == dis01:
                demod[(subi + symi * len(data_index)) * 2] = 0
                demod[(subi + symi * len(data_index)) * 2 + 1] = 1
            elif mindis == dis11:
                demod[(subi + symi * len(data_index)) * 2] = 0
                demod[(subi + symi * len(data_index)) * 2 + 1] = 0
            elif mindis == dis10:
                demod[(subi + symi * len(data_index)) * 2] = 1
                demod[(subi + symi * len(data_index)) * 2 + 1] = 0
    return demod


def channel_estimation(preamble_lts, index, lts_frequency):
    preamble_lts_1 = preamble_lts[0:63]
    preamble_lts_2 = preamble_lts[64:127]
    preamble_lts_avg = (preamble_lts_1 + preamble_lts_2) / 2
    preamble_lts_avg_f = np.fft.fft(preamble_lts_avg, 64)
    h = np.zeros((64, 1), dtype=complex)
    for i in range(len(index)):
        h[index[i], 0] = preamble_lts_avg_f[index[i]] / lts_frequency[index[i]]
    return h


if __name__ == '__main__':
    # This cell will test your implementation of `detect_preamble`  
    short_preamble_length = 20
    signal_length = 1000
    short_preamble = np.exp(2j * np.pi * np.random.random(short_preamble_length))
    preamble = np.tile(short_preamble, 10)  # 重复十次
    noise = np.random.normal(size=signal_length) + 1j * np.random.normal(size=signal_length)
    signalA = 0.1 * noise
    signalB = 0.1 * noise
    preamble_start_idx = 123
    signalB[preamble_start_idx:preamble_start_idx + len(preamble)] += preamble
    # print(detect_preamble_cross_correlation(preamble, signalB))
    # print(detect_preamble_auto_correlation(signalB,short_preamble_length))
    # print(detect_preamble_by_energy(signalB))
    # print(detect_preamble_by_sliding_window(signalB,short_preamble_length))
    preamble_lts = np.load("preamble_lts.npy")
    preamble_sts = np.load("preamble_sts.npy")
    received_signal_weak = np.load("recorded_signal_weak.npy")
    received_signal_strong = np.load("recorded_signal_strong.npy")
    received_signal = np.load("recorded_signal.npy")
    tx_signal = np.load("tx_signal.npy")
    preamble_sts_new = np.tile(preamble_sts, 10)
    preamble_lts_new = np.tile(preamble_lts, 2)
    # print(detect_preamble_cross_correlation(preamble_lts_new, received_signal))
    # print(detect_preamble_auto_correlation(received_signal,len(preamble_lts)))
    # print(detect_preamble_by_energy(received_signal))
    print(detect_preamble_by_sliding_window(received_signal, len(preamble_lts)))

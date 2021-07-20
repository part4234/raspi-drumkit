import matplotlib.pyplot as plt
import numpy as np

from .peak_detect import PeakDetect


def plot(data, alg: PeakDetect):
    print('[Plot] plotting graphs...')
    x = np.arange(1, len(data)+1)
    avgFilter = np.asarray(alg.avgFilter)
    stdFilter = np.asarray(alg.stdFilter)

    plt.subplot(211)
    plt.plot(x, data)
    plt.plot(x, alg.avgFilter, color="cyan", lw=2)
    plt.plot(x, avgFilter + alg.threshold * stdFilter, color="green", lw=2)
    plt.plot(x, avgFilter - alg.threshold * stdFilter, color="green", lw=2)

    # plt.subplot(312)
    # plt.step(x, alg.signals, color="red", lw=2)
    # plt.ylim(-1.5, 1.5)

    plt.subplot(212)
    plt.step(x, alg.strengths, color="purple", lw=2)
    plt.show()

import time
import matplotlib.pyplot as plt

from helpers.acc_reader import AccReader


def main():
    input('Press Enter to start logging...')
    data = []
    acc = AccReader()
    t_end = time.time() + 5

    while time.time() < t_end:
        data.append(acc.accleration[2])

    plot_graph(data)

def plot_graph(data):
    plt.plot(data)
    plt.show()

if __name__ == "__main__":
    main()

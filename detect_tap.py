import time

from helpers.acc_reader import AccReader
from helpers.mixer import Mixer


def main():
    ctrl = DetectTap()
    ctrl.start()


class DetectTap:
    def __init__(self):
        self.mixer = Mixer()
        self.acc = AccReader()
        self.__load_config()

        input('Press Enter to start calibration.')
        self.__calibrate()

    def __load_config(self):
        self.lag = 0.1
        self.threshold = 0.2
        self.peak_scale = 1.1
        self.peak_buffer = 0.2
        self.volume_lowest = 0.1
        self.volume_scale = 1.2
        self.cal_time = 5

    def __calibrate(self):
        self.peak = self.__get_peak()

    def __get_peak(self):
        print('Calibrating peak...')
        print('Please tap with hardest strength.')

        max_val = 0
        t_end = time.time() + self.cal_time
        while time.time() < t_end:
            max_val = max(max_val, self.acc.accleration[2])
        peak = max_val * self.peak_scale + self.peak_buffer

        print('Limit:', peak)
        return peak

    def __get_volume(self, value):
        volume = (value - self.threshold) * \
            self.volume_scale / (self.peak - self.threshold)
        if volume < self.volume_lowest:
            volume = self.volume_lowest
        elif volume > 1.0:
            volume = 1.0
        return volume

    def start(self):
        prev_time = 0
        tap_count = 0
        tap_strength = 0

        while True:
            if time.time() - prev_time < self.lag:
                continue

            value = self.acc.accleration[2]
            if value > self.threshold:
                if value > tap_strength:
                    tap_strength = value
                else:
                    volume = self.__get_volume(value)
                    self.mixer.playKick(volume)

                    tap_count += 1
                    print(f'{tap_count}: {tap_strength}, {volume}')
                    prev_time = time.time()
                    tap_strength = 0


if __name__ == '__main__':
    main()

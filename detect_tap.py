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
        self.tap_shock = 0.01
        self.tap_quiet = 0.05
        self.threshold = 2
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
        peak = max_val + self.peak_buffer

        print('Peak:', peak)
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
        tap_end_t = 0
        tap_start_t = 0
        tap_count = 0
        tap_strength = 0
        tap = False

        while True:
            value = self.acc.accleration[2]
            angle = self.acc.gyroscope[1]
            curr_t = time.time()

            if not tap:
                if curr_t - tap_end_t < self.tap_quiet:
                    continue
                if abs(value) > self.threshold and value < 0:
                    tap = True
                    tap_start_t = curr_t
                    tap_strength = max(abs(value), tap_strength)

            else:
                tap_strength = max(abs(value), tap_strength)

                if curr_t - tap_start_t >= self.tap_shock:
                    # play sound
                    volume = self.__get_volume(tap_strength)
                    self.mixer.playKick(volume)

                    tap_count += 1
                    print(f'{tap_count}: {tap_strength}, {volume}')

                    tap = False
                    tap_end_t = curr_t
                    tap_strength = 0


if __name__ == '__main__':
    main()

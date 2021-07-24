import time

import yaml
from yaml.loader import SafeLoader

from helpers.adc_reader import AdcReader
from helpers.mixer import Mixer


def main():
    ctrl = DetectHit()
    ctrl.start()

class DetectHit:
    def __init__(self):
        self.mixer = Mixer()
        self.adc = AdcReader()
        self.__load_config()

        input('Press Enter to start calibration.')
        self.__calibrate()

    def __load_config(self):
        self.lag = 50
        self.threshold_scale = 1.1
        self.threshold_buffer = 50
        self.peak_scale = 1.1
        self.peak_buffer = 100
        self.volume_lowest = 0.1
        self.volume_scale = 1.2
        self.cal_time = 5
        # with open('config.yml') as file:
        #     config = yaml.load(file, Loader=SafeLoader)

    def __calibrate(self):
        self.threshold = self.__get_threshold()
        self.peak = self.__get_peak()

    def __get_threshold(self):
        print('Calibrating threshold...')
        print('Please leave the sensor idle.')

        max_val = 0
        t_end = time.time() + self.cal_time
        while time.time() < t_end:
            max_val = max(max_val, self.adc.chan.value)
        threshold = max_val * self.threshold_scale + self.threshold_buffer

        print('Threshold:', threshold)
        return threshold

    def __get_peak(self):
        print('Calibrating peak...')
        print('Please hit with hardest strength.')

        max_val = 0
        t_end = time.time() + self.cal_time
        while time.time() < t_end:
            max_val = max(max_val, self.adc.chan.value)
        peak = max_val * self.peak_scale + self.peak_buffer

        print('Limit:', peak)
        return peak

    def start(self):
        prev_time = 0
        time = 0
        hit_count = 0
        hit_strength = 0

        while True:
            # reset time if too large
            if time > 999999:
                time = 0
            else:
                time += 1

            value = self.adc.chan.value
            if value > self.threshold:
                hit_strength = max(hit_strength, value)

                if time - prev_time > self.lag:  # is a hit
                    # play sound
                    volume = (value - self.threshold) * \
                        self.volume_scale / (self.peak - self.threshold)
                    if volume < self.volume_lowest:
                        volume = self.volume_lowest
                    elif volume > 1.0:
                        volume = 1.0
                    self.mixer.playSnare(volume)

                    # update counts
                    hit_count += 1
                    print(f'{hit_count}: {hit_strength}, {volume}')
                    prev_time = time
                    hit_strength = 0


if __name__ == '__main__':
    main()

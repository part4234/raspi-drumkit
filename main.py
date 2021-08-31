import time

from helpers.acc_reader import AccReader
from helpers.adc_reader import AdcReader
from helpers.mixer import Mixer


def main():
    ctrl = Controller()
    ctrl.start()


class Controller:
    def __init__(self):
        self.mixer = Mixer()
        self.acc = AccReader()
        self.adc = AdcReader()
        self.__load_config()

        input('Press Enter to start calibration.')
        self.__calibrate_hit()
        self.__calibrate_tap()


    def __load_config(self):
        self.tap_shock = 0.01
        self.tap_quiet = 0.01
        self.tap_peak_buffer = 0.2

        self.hit_lag = 0.01
        self.hit_threshold_scale = 1.1
        self.hit_threshold_buffer = 50
        self.hit_peak_scale = 1.1
        self.hit_peak_buffer = 100

        self.volume_lowest = 0.1
        self.cal_time = 5


    def __calibrate_hit(self):
        self.hit_threshold = self.__get_hit_threshold()
        self.hit_peak = self.__get_hit_peak()


    def __calibrate_tap(self):
        self.tap_threshold = 2
        self.tap_peak = self.__get_tap_peak()


    def __get_hit_threshold(self):
        print('Please leave the sensor idle.')

        max_val = 0
        t_end = time.time() + self.cal_time
        while time.time() < t_end:
            max_val = max(max_val, self.adc.chan.value)
        threshold = max_val * self.hit_threshold_scale + self.hit_threshold_buffer

        print('Hit threshold:', threshold)
        return threshold


    def __get_hit_peak(self):
        print('Keep hitting.')

        max_vals = [0, 0, 0, 0]
        t_end = time.time() + self.cal_time

        while time.time() < t_end:
            val = self.adc.chan.value
            if val < self.hit_threshold:
                continue
            for i, max_val in enumerate(max_vals):
                if val > max_val:
                    max_vals[i] = val
                    break

        peak = self.__get_avg(max_vals[1:]) * self.hit_peak_scale + self.hit_peak_buffer

        print('Hit peak:', peak)
        return peak


    def __get_tap_peak(self):
        print('Keep tapping.')

        max_vals = [0, 0, 0, 0]
        t_end = time.time() + self.cal_time

        while time.time() < t_end:
            val = abs(self.acc.accleration[2])
            if val < self.tap_threshold:
                continue
            for i, max_val in enumerate(max_vals):
                if val > max_val:
                    max_vals[i] = val
                    break

        peak = self.__get_avg(max_vals[1:]) + self.tap_peak_buffer

        print('Tap peak:', peak)
        return peak


    def start(self):
        self.__init_counters()
        while True:
            self.curr_t = time.time()
            self.__detect_tap(self.acc.accleration[2])
            self.__detect_hit(self.adc.chan.value)


    def __init_counters(self):
        self.curr_t = 0;

        self.hit_prev_t = 0
        self.hit_count = 0
        self.hit_strength = 0

        self.tap_end_t = 0
        self.tap_start_t = 0
        self.tap_count = 0
        self.tap_strength = 0
        self.tap = False


    def __detect_tap(self, value):
        if not self.tap:
            if self.curr_t - self.tap_end_t < self.tap_quiet:
                return
            if abs(value) > self.tap_threshold and value < 0:
                self.tap = True
                self.tap_start_t = self.curr_t
                self.tap_strength = max(abs(value), self.tap_strength)

        else:
            self.tap_strength = max(abs(value), self.tap_strength)

            if self.curr_t - self.tap_start_t >= self.tap_shock:
                self.tap_count += 1
                volume = self.__get_volume(self.tap_strength, self.tap_peak, self.tap_threshold)
                # print(f'Tap {self.tap_count}: {self.tap_strength}, {volume}')
                self.mixer.playKick(volume)

                self.tap = False
                self.tap_end_t = self.curr_t
                self.tap_strength = 0


    def __detect_hit(self, value):
        if value > self.hit_threshold:
            self.hit_strength = max(self.hit_strength, value)

            if self.curr_t - self.hit_prev_t > self.hit_lag:
                volume = self.__get_volume(self.hit_strength, self.hit_peak, self.hit_threshold)
                self.hit_count += 1
                # print(f'Hit {self.hit_count}: {self.hit_strength}, {volume}')
                self.mixer.playSnare(volume)

                self.hit_prev_t = self.curr_t
                self.hit_strength = 0


    def __get_volume(self, value, peak, threshold):
        volume = (value - threshold) / (peak - threshold)
        if volume < self.volume_lowest:
            volume = self.volume_lowest
        elif volume > 1.0:
            volume = 1.0
        return volume


    def __get_avg(self, array):
        return sum(array) / len(array)


if __name__ == '__main__':
    main()

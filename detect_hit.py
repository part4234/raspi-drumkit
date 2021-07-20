from helpers.adc_reader import AdcReader
from helpers.mixer import Mixer
import time


def main():
    # init
    mixer = Mixer()
    adc = AdcReader()

    # settings
    lag = 50
    threshold_scale = 1.1
    threshold_buffer = 50
    peak_scale = 1.1
    peak_buffer = 100
    volume_lowest = 0.1
    volume_scale = 1.2
    cal_time = 5

    # calibration
    input('Press Enter to start calibration.')
    threshold = get_threshold(adc, threshold_scale, threshold_buffer, cal_time)
    peak = get_peak(adc, peak_scale, peak_buffer, cal_time)

    # init counts
    prev_count = 0
    count = 0
    hit_count = 0
    hit_strength = 0

    while True:
        if count > 999999:
            count = 0
        else:
            count += 1

        value = adc.chan.value
        if value > threshold:
            hit_strength = max(hit_strength, value)

            if count - prev_count > lag:  # is a hit
                # play sound
                volume = (value - threshold) * volume_scale / (peak - threshold)
                if volume < volume_lowest:
                    volume = volume_lowest
                elif volume > 1.0:
                    volume = 1.0
                mixer.playSnare(volume)

                # update counts
                hit_count += 1
                print(f'{hit_count}: {hit_strength}, {volume}')
                prev_count = count
                hit_strength = 0


def get_threshold(adc: AdcReader, scale, buffer, cal_time=5):
    print('Calibrating threshold...')
    print('Please leave the sensor idle.')

    max_val = 0
    t_end = time.time() + cal_time
    while time.time() < t_end:
        max_val = max(max_val, adc.chan.value)
    threshold = max_val * scale + buffer

    print('Threshold:', threshold)
    return threshold


def get_peak(adc: AdcReader, scale, buffer, cal_time=5):
    print('Calibrating peak...')
    print('Please hit with hardest strength.')

    max_val = 0
    t_end = time.time() + cal_time
    while time.time() < t_end:
        max_val = max(max_val, adc.chan.value)
    peak = max_val * scale + buffer

    print('Limit:', peak)
    return peak


if __name__ == '__main__':
    main()

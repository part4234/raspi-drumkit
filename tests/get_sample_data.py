import csv
import time
import sys

from helpers.adc_reader import AdcReader


def main(filename='data.csv'):
    input('Press Enter to start logging...')
    data = []
    adc = AdcReader()
    t_end = time.time() + 10

    while time.time() < t_end:
        data.append([adc.chan.value, adc.chan.voltage])

    write_csv(f'../data/{filename}', data)


def write_csv(path, data):
    print(f'Start writing to {path}')
    with open(path, mode='w') as file:
        writer = csv.writer(file, delimiter=",")
        header = ['value', 'voltage']
        writer.writerow(header)
        writer.writerows(data)
    print('Finish writing.')


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main(sys.argv[0])
    else:
        main()

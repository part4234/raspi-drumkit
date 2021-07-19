import csv
import time

from read_adc import ReadAdc


def main():
  input('Press Enter to start logging...')
  data = []
  adc = ReadAdc()
  t_end = time.time() + 10

  while time.time() < t_end:
    data.append([adc.chan.value, adc.chan.voltage])
  
  write_csv('./data/data.csv', data)

def write_csv(path, data):
  print(f'Start writing to {path}')
  with open(path, mode='w') as file:
    writer = csv.writer(file, delimiter=",")
    header = ['value', 'voltage']
    writer.writerow(header)
    writer.writerows(data)
  print('Finish writing.')

if __name__ == "__main__":
  main()

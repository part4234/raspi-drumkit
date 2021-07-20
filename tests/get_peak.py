import csv
from helpers.peak_detect import RealTimePeakDetect
from helpers.plot import plot

def main():
  lag = 25 # 30, 20 (too small)
  threshold = 6 # 10, 5
  influence = 0

  val_alg = RealTimePeakDetect(lag, threshold, influence)
  volt_alg = RealTimePeakDetect(lag, threshold, influence)

  data = read_csv()
  for val in data[0]:
    val_alg.thresholding_algo(val)
  for val in data[1]:
    volt_alg.thresholding_algo(val)

  plot(data[0], val_alg)

def read_csv():
  print('Start reading data...')
  values = []
  voltages = []

  with open('./data/data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count = 0
    for row in csv_reader:
      if line_count > 0:
        values.append(float(row[0]))
        voltages.append(float(row[1]))
      line_count += 1
    print(f'Read {line_count} lines.')
  
  return (values, voltages)

if __name__ == '__main__':
  main()
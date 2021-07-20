import time

from helpers.mixer import Mixer


def main():
  mixer = Mixer()
  for i in range(5):
    mixer.playSnare()
    time.sleep(1)

if __name__ == '__main__':
  main()

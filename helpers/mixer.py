from pygame import mixer

path = '/home/pi/Documents/Project/audio/'
sample = 'beep.wav'
low_acoustic_snare = 'low-acoustic-snare-sound.wav'

class Mixer:
  def __init__(self):
    print('[Mixer] init')
    mixer.init()
    # Load sounds
    print('[Mixer] load sounds')
    self.sample = mixer.Sound(path + sample)
    self.snare = mixer.Sound(path + low_acoustic_snare)

  def playSample(self, volume=0.5):
    print('[Mixer] sample', volume)
    self.sample.set_volume(volume)
    self.sample.play()

  def playSnare(self, volume=0.5):
    print('[Mixer] snare', volume)
    self.snare.set_volume(volume)
    self.snare.play()

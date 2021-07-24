from os import system
from pygame import mixer

PATH = '/home/pi/Documents/Project/audio/'
SAMPLE = 'beep.wav'
LOW_SNARE = 'low-acoustic-snare-sound.wav'
JAZZ_KICK = 'jazz-kickdrum.wav'


class Mixer:
    def __init__(self):
        print('[Mixer] init')
        mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
        self.loadSound()
        print('[Mixer] done')

    def loadSound(self):
        self.sample = mixer.Sound(PATH + SAMPLE)
        self.snare = mixer.Sound(PATH + LOW_SNARE)
        self.kick = mixer.Sound(PATH + JAZZ_KICK)

    def playSample(self, volume=0.5):
        # print('[Mixer] sample', volume)
        self.sample.set_volume(volume)
        self.sample.play()

    def playSnare(self, volume=0.5):
        # print('[Mixer] snare', volume)
        self.snare.set_volume(volume)
        self.snare.play()

    def playKick(self, volume=0.5):
        # print('[Mixer] kick', volume)
        self.kick.set_volume(volume)
        self.kick.play()
        

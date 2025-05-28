import time
import pygame.mixer as mixer

class Audio:
    def __init__(self, ext = "wav"):
        super()
        mixer.init()
        self.sounds = dict()
        self.ext = ext
    
    def create(self, sound):
        soundfile = f"./sounds/{sound}.{self.ext}"
        print(f"Creating sound {soundfile}")
        self.sounds[sound] = mixer.Sound(soundfile)

    def play(self, sound):
        if sound not in self.sounds:
            self.create(sound)
        self.sounds[sound].play()
        print("Sound played")
    
    def stop(self, sound, warn=False):
        if sound not in self.sounds:
            if warn: print(f"Sound {sound} did not exist in dict")
            return
        self.sounds[sound].stop()

audio = Audio()
audio.create("100")

def test():

    input()
    audio.play("100")
    t = time.time()
    print("playing")
    input()
    print(time.time() - t)

    return

while True:
    test()
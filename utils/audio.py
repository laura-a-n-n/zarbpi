import pygame.mixer as mixer
from pygame.time import wait
from config.main import settings

class Audio:
    def __init__(self, ext="wav"):
        super()
        mixer.init()
        self.sounds = dict()
        self.ext = ext
        self.current_song = 0
        self.music_playing = False

    def create(self, sound):
        soundfile = f"{settings['sounds_path']}/{sound}.{self.ext}"
        print(f"Creating sound {soundfile}")
        sound_object = mixer.Sound(soundfile)
        self.sounds[sound] = sound_object
        return sound_object

    def play(self, sound, with_music=True, volume=None):
        if with_music:
            self.music(True)
        sound_object = None
        if sound not in self.sounds:
            sound_object = self.create(sound)
        else:
            sound_object = self.sounds[sound]
        if volume is not None:
            sound_object.set_volume(volume)
        else:
            sound_object.set_volume(1)
        print("Sound playing...")
        return sound_object.play()
    
    def music(self, should_play: bool):
        music = str(settings["bg_music_start"] + self.current_song)
        if music not in self.sounds:
            self.create(music)
        if should_play and not self.music_playing:
            self.sounds[music].play(fade_ms=settings["fade_time"])
            wait(settings["fade_time"])
        elif not should_play:
            self.stop(music, fade_ms=settings["fade_time"])
            self.current_song += 1
            self.current_song %= settings["num_bg_music"]
        self.music_playing = should_play

    def stop(self, sound, fade_ms=0, warn=False):
        if sound not in self.sounds:
            if warn: print(f"Sound {sound} did not exist in dict")
            return
        if fade_ms > 0:
            self.sounds[sound].fadeout(fade_ms)
        else:
            self.sounds[sound].stop()
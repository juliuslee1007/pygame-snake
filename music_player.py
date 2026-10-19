import pygame

class Music_Player:
    def __init__(self, mixer):
        self.mixer = mixer
        mixer.music.load("assets/snakebgm.mp3")
        mixer.music.play(-1)
        self.paused = False
        self.running = True
        self.eat_sound = self.mixer.Sound("assets/apple_eat.wav")
        self.eat_sound.set_volume(0.8)

    def eat_food(self):
        self.eat_sound.play()
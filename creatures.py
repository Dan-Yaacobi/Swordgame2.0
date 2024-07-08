import pygame
import random
import math

class Creature():
    def __init__(self,name, hp, power,coins,bg_color, image_name):
        self.name = name
        self.hp = hp
        self.power = power
        self.coins = coins
        self.bg_color = bg_color
        self.image_name = image_name

    def return_image(self):
        return self.image
    
    def return_bg_color(self):
        return self.bg_color
    
    def return_hp(self):
        return self.hp
    
    def hit(self,dmg):
        new_val = getattr(self,'hp') - dmg
        setattr(self,'hp', new_val)
        
    def drop(self):
        return self.coins

    def return_power(self):
        return self.power
    
    def return_image_name(self):
        return self.image_name
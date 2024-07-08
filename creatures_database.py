import os
from creatures import Creature
import pygame

current_dir = os.path.dirname(__file__)

goblin_hp = 150
goblin_attack = 5
goblin_value = 10

goblin1_bg_color = (61,118,92)
goblin1 = Creature("Goblin",goblin_hp,goblin_attack,goblin_value,goblin1_bg_color,"goblin1.png")

goblin2_bg_color = (105,144,94)
goblin2 = Creature("Goblin",goblin_hp,goblin_attack,goblin_value,goblin2_bg_color,"goblin2.png")

goblin3_bg_color = (88,157,116)
goblin3 = Creature("Goblin",goblin_hp,goblin_attack,goblin_value,goblin3_bg_color,"goblin3.png")

goblin4_bg_color = (159,174,135)
goblin4 = Creature("Goblin",goblin_hp,goblin_attack,goblin_value,goblin4_bg_color,"goblin4.png")

goblin5_bg_color = (145,125,107)
goblin5 = Creature("Goblin",goblin_hp,goblin_attack,goblin_value,goblin5_bg_color,"goblin5.png")

goblins = [goblin1,goblin2,goblin3,goblin4,goblin5]

goblin_wizard_bg_color = (78,99,126)

goblin_wizard = Creature("Goblin Wizard", 100, 1, 150,goblin_wizard_bg_color,"goblin_necromancer.png")

goblin_undead_bg_color = (75,74,105)
goblin_undead = Creature("Goblin Undead",20,2,1,goblin_undead_bg_color,"goblin_undead.jpg")

#(108,133,138)
goblin_jesus_bg_color = (149,162,110)
goblin_jesus = Creature("Goblin Jesus", 0,0,0,goblin_jesus_bg_color,"goblin jesus.png")
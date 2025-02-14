import pygame
from sword import Sword, Shield, Health_Potion
import os
import copy
import pygame_widgets as pw
from pygame_widgets.button import Button
from saveGame import saving
from loadGame import loadgame
from creatures_database import goblins,goblin_wizard,goblin_undead,goblin_jesus
import random
import datetime
from colors import lavender,purple,teal,light_torquoise,goblin_muck,white,goblin_green,black,light_gray,green,nature_green,blue,darker_blue
from colors import tan,gold,orange,red,light_orange,brown
import colors
import forestgenerator
from forestgenerator import RegularNode,ComplexNode
import sys
import time
import math

################### Given an image name such as "image.png" and its background color, returns the image without the bg ###################
def remove_background(image_name,bg_color,amount = 0.06):
    image = pygame.image.load(os.path.join(current_dir, image_name)).convert()
    image_pa = pygame.PixelArray(image)
    pygame.PixelArray.replace(image_pa,bg_color,white,amount)
    image.set_colorkey(white)
    del(image_pa)
    return image

pygame.init()
pygame.mixer.init()
width = 1024
height = 1024
screen = pygame.display.set_mode((width,height))
current_dir = os.path.dirname(__file__)
sys.setrecursionlimit(10000)

###################### Uploading all visual assets ######################
full_health_image = remove_background(fr"healthbar\full_health.png",colors.healthbar_bg)
health_75_image = remove_background(fr"healthbar\75_health.png",colors.healthbar_bg)
half_health_image = remove_background(fr"healthbar\half_health.png",colors.healthbar_bg)
health_25_image = remove_background(fr"healthbar\25_health.png",colors.healthbar_bg)
health_40_image = remove_background(fr"healthbar\40_health.png",colors.healthbar_bg)
health_60_image = remove_background(fr"healthbar\60_health.png",colors.healthbar_bg)
health_90_image = remove_background(fr"healthbar\90_health.png",colors.healthbar_bg)
health_10_image = remove_background(fr"healthbar\10_health.png",colors.healthbar_bg)

inventory_image = remove_background("inventory.png",colors.inventory_bg)
goldsack_image = remove_background("goldsack.png",colors.goldsack_bg,0.1)
background_image =  pygame.image.load(os.path.join(current_dir, "Background.jpeg"))
graveyard_image = pygame.image.load(os.path.join(current_dir, "goblin_graveyard.jpg")) 
graveyard_image_rect = graveyard_image.get_rect()

attack_button_image = pygame.image.load(os.path.join(current_dir, "attack_button.png"))

forest_left_image = pygame.image.load(os.path.join(current_dir, "left_button.png")) 
forest_right_image = pygame.image.load(os.path.join(current_dir, "right_button.png")) 
forward_image = pygame.image.load(os.path.join(current_dir, "forward_button.png")) 
forest_previous_image = pygame.image.load(os.path.join(current_dir, "previous_button.png"))

town_image = pygame.image.load(os.path.join(current_dir, "town.jpeg"))
town_image_rect = (0,0)
shop_image = pygame.image.load(os.path.join(current_dir, "shop.jpg"))
shop_image_rect = shop_image.get_rect()

forest_entrance_image = pygame.image.load(os.path.join(current_dir, fr"forest_roads\forest_entrance.jpeg"))
forest_entrance_rect = forest_entrance_image.get_rect()

fatigued_image = pygame.image.load(os.path.join(current_dir,'fatigued.jpg'))
zombie1_right_image = remove_background(os.path.join(current_dir,fr"zombies_right\zombie1.png"),colors.zombie_bg)
zombie2_right_image = remove_background(os.path.join(current_dir,fr"zombies_right\zombie2.png"),colors.zombie_bg)
zombie3_right_image = remove_background(os.path.join(current_dir,fr"zombies_right\zombie3.png"),colors.zombie_bg)
zombie4_right_image = remove_background(os.path.join(current_dir,fr"zombies_right\zombie4.png"),colors.zombie_bg)
zombie5_right_image = remove_background(os.path.join(current_dir,fr"zombies_right\zombie5.png"),colors.zombie_bg)
zombie6_right_image = remove_background(os.path.join(current_dir,fr"zombies_right\zombie6.png"),colors.zombie_bg)
zombie7_right_image = remove_background(os.path.join(current_dir,fr"zombies_right\zombie7.png"),colors.zombie_bg)

zombie1_left_image = remove_background(os.path.join(current_dir,fr"zombies_left\zombie1.png"),colors.zombie_bg)
zombie2_left_image = remove_background(os.path.join(current_dir,fr"zombies_left\zombie2.png"),colors.zombie_bg)
zombie3_left_image = remove_background(os.path.join(current_dir,fr"zombies_left\zombie3.png"),colors.zombie_bg)
zombie4_left_image = remove_background(os.path.join(current_dir,fr"zombies_left\zombie4.png"),colors.zombie_bg)
zombie5_left_image = remove_background(os.path.join(current_dir,fr"zombies_left\zombie5.png"),colors.zombie_bg)
zombie6_left_image = remove_background(os.path.join(current_dir,fr"zombies_left\zombie6.png"),colors.zombie_bg)
zombie7_left_image = remove_background(os.path.join(current_dir,fr"zombies_left\zombie7.png"),colors.zombie_bg)

zombie_images = [zombie1_right_image,zombie2_right_image,zombie3_right_image,zombie4_right_image,zombie5_right_image,zombie6_right_image,zombie7_right_image,
                 zombie1_left_image,zombie2_left_image,zombie3_left_image,zombie4_left_image,zombie5_left_image,zombie6_left_image,zombie7_left_image,]
for image in zombie_images:
    image = pygame.transform.smoothscale(image,(150,150))
goblin_wizard_image = remove_background(goblin_wizard.return_image_name(),goblin_wizard.return_bg_color())
necromancer_room_image = pygame.image.load(os.path.join(current_dir, "necromancer_room.jpg"))
goblin_wizard_final_image = remove_background("goblin_necro_final.png",colors.goblin_necro_final_bg)
black_hole_image = remove_background("black hole.png",colors.black_hole_bg)
#black_hole_cursor = pygame.transform.scale(black_hole_image,(32,32))
cursed_skull_image = remove_background("cursed skull.png", colors.cursed_skull_bg)

fairy_forest_image = pygame.image.load(os.path.join(current_dir, fr"forest_roads\fairy_forest.jpeg"))
fairy_forest_rect = fairy_forest_image.get_rect()

iron_ore_image = remove_background("iron ore.png",colors.iron_ore_bg)
iron_ore_token = remove_background("iron ore token.png",colors.iron_ore_bg)
gold_ore_image = remove_background("gold ore.png",colors.iron_ore_bg)
gold_ore_token = remove_background("gold ore token.png",colors.iron_ore_bg)

mushroom1_image = remove_background(fr"mushrooms\mushroom1.png",colors.mushroom1_bg)
mushroom2_image = remove_background(fr"mushrooms\mushroom2.png",colors.mushroom2_bg)
mushroom3_image = remove_background(fr"mushrooms\mushroom3.png",colors.mushroom3_bg)
mushroom4_image = remove_background(fr"mushrooms\mushroom4.png",colors.mushroom4_bg)
mushroom5_image = remove_background(fr"mushrooms\mushroom5.png",colors.mushroom5_bg)
mushroom_token = remove_background(fr"mushrooms\mushroom_token.png",colors.mushrooms_bg)

magic_frog_image = remove_background("magic frog.png",colors.magic_frog_bg)

goblin_Fairy_image = remove_background("goblin_fairy.png", colors.goblin_fairy_bg)

font = pygame.font.Font('freesansbold.ttf', 32)
small_font = pygame.font.Font('freesansbold.ttf', 25)
bloody_font = pygame.font.Font(os.path.join(current_dir,"Bloody Frozen.ttf"),35)
big_bloody_font = pygame.font.Font(os.path.join(current_dir,"Bloody Frozen.ttf"),45)
cinzel_font = pygame.font.Font(os.path.join(current_dir,"Cinzel.otf"),23)
dagger_image = remove_background("dagger.png", colors.dagger_bg)
felball_image = remove_background("felball.png",colors.felball_bg)

cursor_image = remove_background("curser.png",colors.curser_bg,0.04)
cursor_image_rect = cursor_image.get_rect()
cursor = pygame.cursors.Cursor((0,0),cursor_image)
carrot_inv_image = remove_background("carrot.png",colors.inv_carrot_bg)
unicorn_inv_image = remove_background("unicorn.png",colors.inv_unicorn_bg)
money_image = remove_background("money.png",colors.money_bg)
wooden_frame_image = pygame.image.load(os.path.join(current_dir, "wooden frame.png")) 
inventory_bg_image = pygame.image.load(os.path.join(current_dir, "inventory_bg.jpg"))
wooden_frame2_image = pygame.image.load(os.path.join(current_dir, "wooden frame2.png"))

dead_image = pygame.image.load(os.path.join(current_dir, "dead.jpg"))
scroll_image = remove_background('scroll.jpg',black)

goblin_jesus_image = remove_background(goblin_jesus.return_image_name(),goblin_jesus.return_bg_color(),0.08)

goblin1_sound = pygame.mixer.Sound(os.path.join(current_dir,fr"soundeffects\goblin1.mp3"))
goblin_sounds = [goblin1_sound]
############################ Swords ############################
def create_swords():
    global swords_database,shields_database

    copper_sword_image = remove_background(fr"swords\coppersword.jpeg",colors.copper_bg)
    copper_sword = Sword("Copper Sword",5,"Sword",colors.copper,copper_sword_image)

    iron_sword_image = remove_background(fr"swords\ironsword.jpg",colors.iron_sword_bg)
    iron_sword = Sword("Iron Sword",30,"Sword",colors.iron,iron_sword_image)

    gold_sword_image = remove_background(fr"swords\goldsword.jpg",colors.gold_bg)
    gold_sword = Sword("Gold Sword",55,"Sword",colors.gold,gold_sword_image)

    fire_sword_image = remove_background(fr"swords\fire_sword.jpeg",colors.fire_sword_bg)
    fire_sword = Sword("Fire Sword",999,"Sword",colors.fire_sword,fire_sword_image)

    unicorn_sword_image = remove_background(fr"swords\unicorn_sword.jpg",colors.unicorn_bg)
    unicorn_sword = Sword("Unicorn Sword",999,"Sword",colors.unicorn,unicorn_sword_image)

    living_sword_image = remove_background(fr"swords\living_sword.jpg",colors.living_sword_bg)
    living_sword = Sword("Living Sword", 999, "Sword",colors.nature_green, living_sword_image)
    ############################ Shields ############################
    gold_shield_image = remove_background(fr"shields\gold_shield.png",colors.gold_shield_bg,0.1)
    gold_shield = Shield("Gold Shield","Shield",colors.gold,gold_shield_image,5,50,500)

    mushroom_shield_image = remove_background(fr"shields\mushroom_shield.jpg",colors.mushroom_shield_bg)
    mushroom_shield = Shield("Mushy Shield","Shield",colors.mushroom_shield_name,mushroom_shield_image,10,100,1000)

    ############################ Item's lists ############################
    swords_database = [copper_sword,iron_sword,gold_sword,fire_sword,unicorn_sword,living_sword]
    shields_database = [gold_shield,mushroom_shield]

health_potion_image = remove_background("health_potion.png",colors.health_potion_bg)
health_potion = Health_Potion("Health Potion",20,"Potion",red,health_potion_image)

holy_charm_image = remove_background("holy charm.png",colors.holy_charm_bg)
evil_ring_image = remove_background("evil ring.png",colors.evil_ring_bg,0.05)

create_swords()
# Given an item, returns its Image #
def find_sword(sword):
    for i in range(len(swords_database)):
        if swords_database[i].return_name() == sword.return_name():
            return swords_database[i].return_image()

def find_shield(shield):
    for i in range(len(shields_database)):
        if shields_database[i].return_name() == shield.return_name():
            return shields_database[i].return_image()


def find_item_image(item):
    if item.return_type() == "sword":
        find_sword(item)
    if item.return_type() == "shield":
        find_shield(item)

def item_db(item_type):
    if item_type == "sword":
        return swords_database
    if item_type == "shield":
        return shields_database






















graveyard_music = os.path.join(current_dir,"graveyard_bgm.mp3")
forest_music = os.path.join(current_dir,"Into the Woods.mp3")
castle_music = os.path.join(current_dir,"final_boss.mp3")
monastery_music = os.path.join(current_dir,"monastery.mp3")
hollow_tree_music = os.path.join(current_dir,"hollow tree.mp3")
TOWN_MUSIC = os.path.join(current_dir,"Into the Wilderness.mp3")

upgrade_sound = pygame.mixer.Sound(os.path.join(current_dir,fr"soundeffects\upgrade_sound.mp3"))

undead1_sound = pygame.mixer.Sound(os.path.join(current_dir,fr"soundeffects\undead1.mp3"))
undead2_sound = pygame.mixer.Sound(os.path.join(current_dir,fr"soundeffects\undead2.mp3"))
undead3_sound = pygame.mixer.Sound(os.path.join(current_dir,fr"soundeffects\undead3.mp3"))
undead4_sound = pygame.mixer.Sound(os.path.join(current_dir,fr"soundeffects\undead4.mp3"))
undead5_sound = pygame.mixer.Sound(os.path.join(current_dir,fr"soundeffects\undead5.mp3"))
undead6_sound = pygame.mixer.Sound(os.path.join(current_dir,fr"soundeffects\undead6.mp3"))
undead7_sound = pygame.mixer.Sound(os.path.join(current_dir,fr"soundeffects\undead7.mp3"))
undead8_sound = pygame.mixer.Sound(os.path.join(current_dir,fr"soundeffects\undead8.mp3"))
undead9_sound = pygame.mixer.Sound(os.path.join(current_dir,fr"soundeffects\undead9.mp3"))

undead_sounds = [undead1_sound,undead2_sound,undead3_sound,undead4_sound,undead5_sound,undead6_sound,undead7_sound,undead8_sound,undead9_sound]


exit_button = Button(
    screen, 900, 100, 100, 50, text='Exit',
    fontSize=20, margin=20,
    inactiveColour=gold,
    hoverColour=(150,0,0),
    pressedColour=orange, radius=20,
    onClick = lambda: quit())

new_game_button = Button(
    screen, 600, 300, 300, 150, text='New Game',
    fontSize=50, margin=20,
    inactiveColour= tan,
    hoverColour=(150,0,0),
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.change_screen(new_game_scroll_menu))

load_button = Button(
    screen, 150, 300, 300, 150, text='Load Game',
    fontSize=50, margin=20,
    inactiveColour= tan,
    hoverColour=(150,0,0),
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.load_game())

new_game_buttons = [new_game_button,load_button,exit_button]

shop_button = Button(
    screen, 20, 600, 150, 75, text='Shop',
    fontSize=30, margin=20,
    inactiveColour= tan,
    hoverColour=(150,0,0),
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.shop())

upgrade_button = Button(
    screen, 880, 600, 150, 75, text='Upgrade',
    fontSize=30, margin=20,
    inactiveColour=tan,
    hoverColour=(150,0,0),
    pressedColour=orange, radius=20,
    onClick = lambda: Screen.current_screen.change_screen(upgrade_menu))

fight_button = Button(
    screen, 450, 500, 150, 75, text='Adventure',
    fontSize=30, margin=20,
    inactiveColour= tan,
    hoverColour=(150,0,0),
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.change_screen(forest_entrance))

save_button = Button(
    screen, 800, 100, 100, 50, text='Save',
    fontSize = 20, margin = 20,
    inactiveColour= gold,
    hoverColour=(150,0,0),
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.save_game())

inventory_button = Button(
    screen, 900, 800, 100, 50,
    fontSize = 20, margin = 20,
    inactiveColour= gold,
    image = inventory_image,
    hoverColour=(150,0,0),
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.open_inventory())

inventory_close_button = Button(
    screen, 900, 800, 100, 50,
    fontSize = 20, margin = 20,
    inactiveColour= gold,
    image = inventory_image,
    hoverColour=(150,0,0),
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.close_inventory())

heal_button = Button(
    screen, 650, 700, 150, 75, text='Heal',
    fontSize=30, margin=20,
    inactiveColour= nature_green,
    hoverColour = gold,
    pressedColour = green, radius=20,
    onClick = lambda: Screen.current_screen.heal())

main_menu_buttons = [shop_button,upgrade_button,fight_button,save_button,heal_button,inventory_button,exit_button]

scroll_next_button = Button(
    screen, 650, 750, 100, 50, text='Next',
    fontSize=20, margin=20,
    inactiveColour = tan,
    hoverColour=(150,0,0),
    pressedColour=(0, 255, 0), radius=20,
    onClick = lambda: Screen.current_screen.scroll_next())

finish_read_scroll = Button(
    screen, 450, 750, 100, 50, text='Ok',
    fontSize=20, margin=20,
    inactiveColour = tan,
    hoverColour=(150,0,0),
    pressedColour=(0, 255, 0), radius=20,
    onClick = lambda: Screen.current_screen.finish_scroll()) 

new_game_menu_screen_buttons = [scroll_next_button,finish_read_scroll]

holy_charm_button = Button(
    screen, 470,700, 50,50,
    image = holy_charm_image,
    inactiveColour = gold,
    pressedColour = lavender, radius=20,
    onClick = lambda: Screen.current_screen.use_holy_charm())

inventory_buttons = [inventory_close_button,holy_charm_button]

buy_sword_button = Button(
    screen, 300, 550, 100, 50, text='Buy',
    fontSize=20, margin=20,
    inactiveColour=gold,
    hoverColour=(150,0,0),
    pressedColour=orange, radius=20,
    onClick = lambda: Screen.current_screen.buy_sword())

buy_shield_button = Button(
    screen, 300, 550, 100, 50, text='Buy',
    fontSize=20, margin=20,
    inactiveColour=gold,
    hoverColour=(150,0,0),
    pressedColour=orange, radius=20,
    onClick = lambda: Screen.current_screen.buy_shield())


next_button = Button(
    screen, 700, 400, 100, 50, text='Next',
    fontSize=20, margin=20,
    inactiveColour=gold,
    hoverColour=(150,0,0),
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.next_item())

previous_button = Button(
    screen, 100, 400, 100, 50, text='Previous',
    fontSize=20, margin=20,
    inactiveColour=gold,
    hoverColour = (150,0,0),
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.prev_item())

swords_shop_button = Button(
    screen, 600, 400, 200, 100, text='Swords',
    fontSize=50, margin=20,
    inactiveColour=gold,
    hoverColour = (150,0,0),
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.change_screen(sword_buying_menu))

shields_shop_button = Button(
    screen, 200, 400, 200, 100, text='Shields',
    fontSize=50, margin=20,
    inactiveColour=gold,
    hoverColour = (150,0,0),
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.change_screen(shield_buying_menu))

back_shop_button = Button(
    screen, 220, 100, 100, 50, text='Back',
    fontSize=20, margin=20,
    inactiveColour=gold,
    hoverColour=(150,0,0),
    pressedColour=orange, radius=20,
    onClick = lambda: Screen.current_screen.change_screen(Screen.previous_screen))

shop_selling_button = Button( 
    screen, 600, 400, 200, 100, text='Sell',
    fontSize=50, margin=20,
    inactiveColour = gold,
    hoverColour=(150,0,0),
    pressedColour=(0, 255, 0), radius=20,
    onClick = lambda: Screen.current_screen.change_screen(sell_menu))

shop_buying_button = Button(
    screen, 200, 400, 200, 100, text='Buy',
    fontSize=50, margin=20,
    inactiveColour = gold,
    hoverColour=(150,0,0),
    pressedColour=(0, 255, 0), radius=20,
    onClick = lambda: Screen.current_screen.change_screen(shop_sub_menu))

return_to_menu_button = Button(
    screen, 100, 100, 100, 50, text='Menu',
    fontSize=20, margin=20,
    inactiveColour=gold,
    hoverColour=(150,0,0),
    pressedColour=orange, radius=20,
    onClick = lambda: Screen.current_screen.change_screen(main_menu))

shop_menu_buttons1 = [return_to_menu_button,shop_buying_button,shop_selling_button]
shop_menu_buttons2 = [return_to_menu_button,back_shop_button,swords_shop_button,shields_shop_button]
buying_menu_buttons = [return_to_menu_button,back_shop_button,next_button,previous_button,buy_sword_button,buy_shield_button]

upgrade_sword_button = Button(
    screen, 370, 550, 100, 50, text='Upgrade',
    fontSize=20, margin=20,
    inactiveColour=darker_blue,
    hoverColour=(150,0,0),
    pressedColour=orange, radius=20,
    onClick = lambda: Screen.current_screen.upgrade_sword())

upgrade_screen_buttons = [return_to_menu_button,upgrade_sword_button]

sell_sword_button = Button(
    screen, 120, 550, 100, 50, text='Sell',
    fontSize=20, margin=20,
    inactiveColour = gold,
    hoverColour=(150,0,0),
    pressedColour=(0, 255, 0), radius=20,
    onClick = lambda: Screen.current_screen.sell_sword())

sell_shield_button = Button(
    screen, 780, 550, 100, 50, text='Sell',
    fontSize=20, margin=20,
    inactiveColour = gold,
    hoverColour=(150,0,0),
    pressedColour=(0, 255, 0), radius=20,
    onClick = lambda: Screen.current_screen.sell_shield())

sell_screen_buttons = [return_to_menu_button,back_shop_button,sell_sword_button,sell_shield_button]

start_fight_button = Button(
    screen, 370, 650, 300, 150, text='Start',
    fontSize=50, margin=20,
    inactiveColour= tan,
    hoverColour = gold,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.change_screen(gy_wave1))

adventure_buttons = [return_to_menu_button, start_fight_button]

forest_forward_to_GY = Button(
    screen, 480,250,30,30,
    pressedColour = orange, 
    image = forward_image,
    onClick = lambda: Screen.current_screen.forward_to_GY())

forest_forward = Button(
    screen, 480,250,30,30,
    pressedColour = orange, 
    image = forward_image,
    onClick = lambda: Screen.current_screen.forward())

forest_right = Button(
    screen, 800, 500, 70, 52,
    pressedColour = orange, 
    image = forest_right_image,
    onClick = lambda: Screen.current_screen.right())

forest_left = Button(
    screen, 100, 500, 70, 52,
    image =forest_left_image,
    pressedColour = orange,
    onClick = lambda: Screen.current_screen.left()) 

forest_prev = Button(
    screen, 480, 850, 30,30,
    image = forest_previous_image,
    pressedColour = orange,
    onClick = lambda: Screen.current_screen.prev()) 

iron_ore_button = Button(
    screen, 300,700, 50,50,
    image = iron_ore_image,
    inactiveColour = light_gray,
    pressedColour = lavender, radius=20,
    onClick = lambda: Screen.current_screen.collect_iron_ore())

gold_ore_button = Button(
    screen, 300,700, 50,50,
    image = gold_ore_image,
    inactiveColour = light_gray,
    pressedColour = lavender, radius=20,
    onClick = lambda: Screen.current_screen.collect_gold_ore())

mushroom1_button = Button(
    screen, 300,700, 50,50,
    image = mushroom1_image,
    inactiveColour = nature_green,
    pressedColour = lavender, radius=20,
    onClick = lambda: Screen.current_screen.collect_mushroom(mushroom1_button))

mushroom2_button = Button(
    screen, 300,700, 50,50,
    image = mushroom1_image,
    inactiveColour = nature_green,
    pressedColour = lavender, radius=20,
    onClick = lambda: Screen.current_screen.collect_mushroom(mushroom2_button))

mushroom3_button = Button(
    screen, 300,700, 50,50,
    image = mushroom1_image,
    inactiveColour = nature_green,
    pressedColour = lavender, radius=20,
    onClick = lambda: Screen.current_screen.collect_mushroom(mushroom3_button))

mushroom4_button = Button(
    screen, 300,700, 50,50,
    image = mushroom1_image,
    inactiveColour = nature_green,
    pressedColour = lavender, radius=20,
    onClick = lambda: Screen.current_screen.collect_mushroom(mushroom4_button))

mushroom5_button = Button(
    screen, 300,700, 50,50,
    image = mushroom1_image,
    inactiveColour = nature_green,
    pressedColour = lavender, radius=20,
    onClick = lambda: Screen.current_screen.collect_mushroom(mushroom5_button))

mushroom_buttons = [mushroom1_button,mushroom2_button,mushroom3_button,mushroom4_button,mushroom5_button]
forest_map_buttons = [exit_button,inventory_button,forest_forward,forest_right,forest_left,forest_prev]

question1_button = Button(
    screen, 600, 650, 100, 50, text='Castle?',
    fontSize=30, margin=20,
    inactiveColour = gold,
    hoverColour=(150,0,0),
    pressedColour=(0, 255, 0), radius=20,
    onClick = lambda: Screen.current_screen.castle_text())

question2_button = Button(
    screen, 450, 650, 100, 50, text='Help?',
    fontSize=30, margin=20,
    inactiveColour = gold,
    hoverColour=(150,0,0),
    pressedColour=(0, 255, 0), radius=20,
    onClick = lambda: Screen.current_screen.quest_text())

question3_button =  Button(
    screen, 300, 650, 100, 50, text="You?",
    fontSize=30, margin=20,
    inactiveColour = gold,
    hoverColour=(150,0,0),
    pressedColour=(0, 255, 0), radius=20,
    onClick = lambda: Screen.current_screen.you_text())

church_buttons = [question1_button,question2_button,question3_button,forest_prev]

enter_monastery_button = Button(
    screen, 480, 560, 100, 50, text='Enter',
    fontSize=30, margin=20,
    inactiveColour= white,
    hoverColour = gold,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.change_screen(church_map)) 

enter_monastery_done_button = Button(
    screen, 480, 560, 100, 50, text='Enter',
    fontSize=30, margin=20,
    inactiveColour= white,
    hoverColour = gold,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.change_screen(church_map_done)) 

magic_frog_button = Button(
    screen, 450, 500, 50, 50,
    image = magic_frog_image,
    pressedColour=(0, 255, 0), radius=20,
    onClick = lambda: Screen.current_screen.collect_magic_frog()) 

pick_holy_charm_button = Button(
    screen, 470,700, 50,50,
    image = holy_charm_image,
    inactiveColour = gold,
    pressedColour = lavender, radius=20,
    onClick = lambda: Screen.current_screen.pick_holy_charm(pick_holy_charm_button))

attack_button = Button(
    screen, 400,400, 50,50,
    image = attack_button_image,
    pressedColour = lavender, radius=20,
    onClick = lambda: Screen.current_screen.attack())

gold_sack_button = Button(screen,450,450,50,50,
    image = goldsack_image,
    hoverColour = white,
    inactiveColour = gold,
    pressedColour = gold, radius=20, margain = 50,
    onClick = lambda: Screen.current_screen.pick_gold_sack(gold_sack_button))

goblin_fight_buttons = [attack_button,exit_button]
z_b_width = 75
z_b_length = 75

goblin_zombie_right_button1 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie1_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_right_button1))

goblin_zombie_right_button2 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie2_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_right_button2))

goblin_zombie_right_button3 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie3_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_right_button3))

goblin_zombie_right_button4 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie4_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_right_button4))

goblin_zombie_right_button5 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie5_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_right_button5))

goblin_zombie_right_button6 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie6_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_right_button6))

goblin_zombie_right_button7 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie7_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_right_button7))

goblin_zombie_right_button8 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie1_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_right_button8))

goblin_zombie_right_button9 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie2_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_right_button9))

goblin_zombie_right_button10 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie3_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_right_button10))

goblin_zombie_right_button11 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie4_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_right_button11))

goblin_zombie_right_button12 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie5_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_right_button12))

goblin_zombie_right_button13 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie6_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_right_button13))

goblin_zombie_right_button14 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie7_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_right_button14))

goblin_zombie_right_button15 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie7_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_right_button15))

goblin_zombie_left_button1 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie1_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_left_button1))

goblin_zombie_left_button2 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie2_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_left_button2))

goblin_zombie_left_button3 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie3_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_left_button3))

goblin_zombie_left_button4 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie4_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_left_button4))

goblin_zombie_left_button5 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie5_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_left_button5))

goblin_zombie_left_button6 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie6_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_left_button6))

goblin_zombie_left_button7 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie7_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_left_button7))

goblin_zombie_left_button8 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie1_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_left_button8))

goblin_zombie_left_button9 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie2_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_left_button9))

goblin_zombie_left_button10 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie3_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_left_button10))

goblin_zombie_left_button11 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie4_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_left_button11))

goblin_zombie_left_button12 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie5_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_left_button12))

goblin_zombie_left_button13 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie6_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_left_button13))

goblin_zombie_left_button14 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie7_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_left_button14))

goblin_zombie_left_button15 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie7_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: Screen.current_screen.click_zombie(goblin_zombie_left_button15))

# each element in index i contains a list of three items. the first item is an indexed button, the second item is a boolean indicating button enabled/disabled, 
# third element is boolean indicating if zombie moving forward or backwards (False => moving forward)
zombies_right_buttons = [[goblin_zombie_right_button1,False,False],[goblin_zombie_right_button2,False,False],[goblin_zombie_right_button3,False,False],[goblin_zombie_right_button4,False,False],
                         [goblin_zombie_right_button5,False,False],[goblin_zombie_right_button6,False,False],[goblin_zombie_right_button7,False,False],[goblin_zombie_right_button8,False,False],
                         [goblin_zombie_right_button9,False,False],[goblin_zombie_right_button10,False,False],[goblin_zombie_right_button11,False,False],[goblin_zombie_right_button12,False,False],
                         [goblin_zombie_right_button13,False,False],[goblin_zombie_right_button14,False,False],[goblin_zombie_right_button15,False,False]]

zombies_left_buttons = [[goblin_zombie_left_button1,False,False],[goblin_zombie_left_button2,False,False],[goblin_zombie_left_button3,False,False],[goblin_zombie_left_button4,False,False],
                         [goblin_zombie_left_button5,False,False],[goblin_zombie_left_button6,False,False],[goblin_zombie_left_button7,False,False],[goblin_zombie_left_button8,False,False],
                         [goblin_zombie_left_button9,False,False],[goblin_zombie_left_button10,False,False],[goblin_zombie_left_button11,False,False],[goblin_zombie_left_button12,False,False],
                         [goblin_zombie_left_button13,False,False],[goblin_zombie_left_button14,False,False],[goblin_zombie_left_button15,False,False]]
ALL_ZOMBIES_BUTTONS = [zombie[0] for zombie in zombies_right_buttons] + [zombie[0] for zombie in zombies_left_buttons]

class Screen:
    #Class Static Variables
    running = True
    current_screen = None
    inventory = [0,0,0,0,1,0] #0 = Magic frog, #1 = mushroom, #2 = iron ore, #3 = gold ore, #4 = Holy Charm #5 = Evil ring
    money = 50
    current_hp = 100
    max_hp = 100
    BASE_HP = 100
    current_sword = None
    current_shield = None
    start_new_game = True
    current_bgm = None
    previous_screen = None
    current_map = None
    frog_quest_accepted = False
    frog_quest_completed = False
    ALL_BUTTONS = [new_game_button,load_button,exit_button,shop_button,upgrade_button,
                   fight_button,save_button,heal_button,inventory_button,scroll_next_button,finish_read_scroll,
                   holy_charm_button,inventory_close_button,return_to_menu_button,shop_buying_button,
                   shop_selling_button,back_shop_button,shields_shop_button,swords_shop_button,previous_button,
                   next_button,sell_shield_button,sell_sword_button,buy_sword_button,buy_shield_button,upgrade_sword_button,start_fight_button,
                   forest_forward,forest_right,forest_left,forest_prev,mushroom1_button,mushroom2_button,mushroom3_button,mushroom4_button,mushroom5_button,
                   gold_ore_button,iron_ore_button,question1_button,question2_button,question3_button,enter_monastery_button,magic_frog_button,
                   pick_holy_charm_button,enter_monastery_done_button,gold_sack_button,attack_button,forest_forward_to_GY] + ALL_ZOMBIES_BUTTONS


    def __init__(self,bgm,bg,buttons_enabled,dynamic_buttons):
        '''Images_array needs to be a matrix,[[pygame surface1,(x1,y1)],[pygame surface2,(x2,y2)]...]'''
        self.bgm = bgm
        self.bg = bg
        self.buttons_enabled = buttons_enabled
        self.dynamic_buttons = dynamic_buttons # False = all buttons appear all the time, True = buttons appear under certian conditions
        
    def change_screen(self, new_screen):
        Screen.previous_screen = Screen.current_screen
        Screen.current_screen = new_screen

    def play_bgm(self):
        if Screen.current_screen.bgm != None:
            if Screen.current_bgm != self.bgm:
                pygame.mixer.music.unload()
                pygame.mixer.music.load(self.bgm)
                pygame.mixer.music.play(-1)
                Screen.current_bgm = self.bgm
        
    def display_bg(self):
        screen.blit(self.bg,(0,0))
    
    def action(self):
        self.display_bg()
        self.play_bgm()
        self.enable_buttons()
        self.disable_buttons()
    
    def find_buttons_to_disable(self):
        buttons_to_disable = []
        for button in Screen.ALL_BUTTONS:
            if button not in self.buttons_enabled:
                buttons_to_disable.append(button)
        return buttons_to_disable
    
    def enable_specific_buttons(self,buttons):
        '''Buttons must be an array of buttons (even if it only contains one button)'''
        for button in buttons:
            button.enable()
            button.show()

    def disable_specific_buttons(self,buttons):
        '''Buttons must be an array of buttons (even if it only contains one button)'''
        for button in buttons:
            button.disable()
            button.hide()

    def enable_buttons(self):
        self.enable_specific_buttons(self.buttons_enabled)

    def disable_buttons(self):
        buttons_to_disable = self.find_buttons_to_disable()
        if len(buttons_to_disable) > 0:
            self.disable_specific_buttons(buttons_to_disable)
    
    def disable_buttons_enable_buttons(self,en_buttons,dis_buttons):
        '''en_buttons = array of buttons to enable, dis_buttons = array of buttons to disable'''
        self.disable_specific_buttons(dis_buttons)
        self.enable_specific_buttons(en_buttons)

    def open_inventory(self):
        self.change_screen(inventory_screen)

    def show_health(self):
        current_health_pcntg = (Screen.current_hp/Screen.max_hp)*100
        if current_health_pcntg == 100:
            screen.blit(full_health_image,(370,100))
        elif current_health_pcntg < 100 and current_health_pcntg >= 90:
            screen.blit(health_90_image,(370,100))
        elif current_health_pcntg < 90 and current_health_pcntg >= 75:
            screen.blit(health_75_image,(370,100))
        elif current_health_pcntg < 75 and current_health_pcntg >= 60:
            screen.blit(health_60_image,(370,100))
        elif current_health_pcntg < 60 and current_health_pcntg >= 50:
            screen.blit(half_health_image,(370,100))
        elif current_health_pcntg < 50 and current_health_pcntg >= 40:
            screen.blit(health_40_image,(370,100))
        elif current_health_pcntg < 40 and current_health_pcntg >= 25:
            screen.blit(health_25_image,(370,100))
        else:
            screen.blit(health_10_image,(370,100))
        hp_text = font.render(str(Screen.current_hp) + "/" + str(Screen.max_hp),True,black,white)
        hp_text.set_colorkey(white)
        screen.blit(hp_text, (490,133))

    def use_holy_charm(self):
        self.change_screen(main_menu)
        Screen.current_map = None
        forest_map.disabled_buttons = False

class Shop(Screen):
    current_viewing_item = None
    current_viewing_item_index = 0
    current_item = None
    MUSHY_SHIELD_COST = 50
    GOLD_SHIELD_COST = 20
    IRON_ORE_COST = 5
    GOLD_ORE_COST = 10
    def __init__(self,bgm,bg,buttons_enabled,dynamic_buttons,item_type):
        super().__init__(bgm,bg,buttons_enabled,dynamic_buttons)
        self.item_type = item_type

    def change_screen(self, new_screen):
        Screen.previous_screen = shop_menu
        Screen.current_screen = new_screen

    def action(self):
        self.display_bg()
        self.disable_buttons()
        self.enable_buttons()
        if self.item_type == Sword:
            self.current_item = swords_database
            self.disable_buttons_enable_buttons([buy_sword_button],[buy_shield_button])
        elif self.item_type == Shield:
            self.current_item = shields_database
            self.disable_buttons_enable_buttons([buy_shield_button],[buy_sword_button])
        self.current_viewing_item = self.current_item[self.current_viewing_item_index]
        screen.blit(wooden_frame_image,(150,150))
        screen.blit(self.current_viewing_item.return_image(),(240,250))
        name_text = font.render(self.current_viewing_item.return_name(), True,self.current_viewing_item.return_name_color(),None)
        screen.blit(name_text,(270,490))
        hp_text = font.render("+" + str(self.current_viewing_item.hp()) + " HP", True,black,None)
        screen.blit(hp_text,(500,400))
        money_text = font.render("Money:    " + str(Screen.money),True,white,brown)
        screen.blit(money_text,(380,650))
        screen.blit(money_image,(495,648))
        if self.item_type == Sword:
            if self.current_viewing_item.return_name() == "Iron Sword":
                if Screen.inventory[2] < self.IRON_ORE_COST:
                        iron_price_text = small_font.render(str(self.IRON_ORE_COST),True,red,None)
                else:
                    iron_price_text = small_font.render(str(self.IRON_ORE_COST),True,white,None)
                text = iron_price_text
                token = iron_ore_token
                screen.blit(text,(550,583))
                screen.blit(token,(508,573))
            elif self.current_viewing_item.return_name() == "Gold Sword":
                if Screen.inventory[3] < self.GOLD_ORE_COST:
                    gold_price_text = small_font.render(str(self.GOLD_ORE_COST),True,red,None)
                else:
                    gold_price_text = small_font.render(str(self.GOLD_ORE_COST),True,white,None)
                text = gold_price_text
                token = gold_ore_token
                screen.blit(text,(550,583))
                screen.blit(token,(508,573))
        elif self.item_type == Shield:
            if self.current_viewing_item.return_name() == "Mushy Shield":
                token = mushroom_token
                cost = self.MUSHY_SHIELD_COST
                inventory_index = 1
            elif self.current_viewing_item.return_name() == "Gold Shield":
                token = gold_ore_token
                cost = self.GOLD_SHIELD_COST
                inventory_index = 3
            screen.blit(token,(508,573))
            if Screen.inventory[inventory_index] < cost:
                price_text = small_font.render(str(cost),True,red,None)
            if Screen.inventory[inventory_index] >= cost:
                price_text = small_font.render(str(cost),True,white,None)
            screen.blit(price_text,(550,583))            
        if self.item_type == Sword:
            if (Screen.money < self.current_viewing_item.value()) or Screen.current_sword != None:
                price_text = font.render("Price:    " + str(self.current_viewing_item.value()),True,red,None)
                screen.blit(price_text,(420,540))
                screen.blit(money_image,(510,537))
            else:      
                price_text = font.render("Price:     " + str(self.current_viewing_item.value()),True,white,None)
                screen.blit(price_text,(420,540))
                screen.blit(money_image,(510,537))
        elif self.item_type == Shield:
            if (Screen.money < self.current_viewing_item.value()) or Screen.current_shield != None:
                price_text = font.render("Price:    " + str(self.current_viewing_item.value()),True,red,None)
                screen.blit(price_text,(420,540))
                screen.blit(money_image,(510,537))
            else:      
                price_text = font.render("Price:     " + str(self.current_viewing_item.value()),True,white,None)
                screen.blit(price_text,(420,540))
                screen.blit(money_image,(510,537))

    def buy_sword(self):
        bought_sword_flag = False
        if Screen.current_sword == None:
            if self.current_viewing_item.return_name() == "Iron Sword":
                if Screen.inventory[2] >= self.IRON_ORE_COST and Screen.money >= self.current_viewing_item.value():
                    Screen.inventory[2] -= self.IRON_ORE_COST
                    bought_sword_flag = True
            elif self.current_viewing_item.return_name() == "Gold Sword":
                if Screen.inventory[3] >= self.GOLD_ORE_COST and Screen.money >= self.current_viewing_item.value():
                    Screen.inventory[3] -= self.GOLD_ORE_COST
                    bought_sword_flag = True
            elif Screen.money >= self.current_viewing_item.value():
                bought_sword_flag = True
            if bought_sword_flag:
                Screen.current_sword = copy.copy(self.current_viewing_item)
                add_hp = 0
                if Screen.current_shield != None:
                    add_hp = Screen.current_shield.hp()
                Screen.max_hp = Screen.BASE_HP + Screen.current_sword.hp() + add_hp
                Screen.money -= Screen.current_sword.value()
                Screen.current_hp = Screen.max_hp

    def buy_shield(self):
        bought_shield_flag = False
        if Screen.current_shield == None:
            if self.current_viewing_item.return_name() == "Mushy Shield":
                if Screen.inventory[1] >= self.MUSHY_SHIELD_COST:
                    Screen.current_shield = copy.copy(self.current_viewing_item)
                    Screen.inventory[1] -= self.MUSHY_SHIELD_COST
                    bought_shield_flag = True

            elif self.current_viewing_item.return_name() == "Gold Shield":
                if Screen.inventory[3] >= self.GOLD_SHIELD_COST:
                    Screen.current_shield = copy.copy(self.current_viewing_item)
                    Screen.inventory[3] -= self.GOLD_SHIELD_COST
                    bought_shield_flag = True
            if bought_shield_flag == True:
                add_hp = 0
                if Screen.current_sword != None:
                    add_hp = Screen.current_sword.hp()
                Screen.max_hp = Screen.BASE_HP + Screen.current_shield.hp() + add_hp
                Screen.current_hp = Screen.max_hp
    def next_item(self):
        if self.current_viewing_item_index < len(self.current_item) - 1:
            self.current_viewing_item_index += 1
    def prev_item(self):
        if self.current_viewing_item_index > 0:
            self.current_viewing_item_index -= 1

class SellMenu(Screen):
    def action(self):
        self.display_bg()
        self.disable_buttons()
        self.enable_buttons()
        money_text = font.render("Money:    " + str(Screen.money),True,white,brown)
        screen.blit(money_text,(380,650))
        screen.blit(money_image,(495,648))
        if Screen.current_sword != None:
            screen.blit(Screen.current_sword.return_image(),(100,200))
            name_text = small_font.render(Screen.current_sword.return_name(), True,Screen.current_sword.return_name_color(),blue)
            screen.blit(name_text,(100,450))
            sword_price_text = font.render("Value: " + str(Screen.current_sword.value()),True,gold,blue)
            screen.blit(sword_price_text,(120,500))
        else:
            self.disable_specific_buttons([sell_sword_button])
        if Screen.current_shield != None:
            screen.blit(Screen.current_shield.return_image(),(700,200))
            shield_name_text = small_font.render(Screen.current_shield.return_name(), True,Screen.current_shield.return_name_color(),blue)
            screen.blit(shield_name_text,(750,450))
            shield_price_text = font.render("Value: " + str(Screen.current_shield.value()),True,gold,blue)
            screen.blit(shield_price_text,(750,500))
        else:
            self.disable_specific_buttons([sell_shield_button])

    def sell_sword(self):
        Screen.money += Screen.current_sword.value()
        Screen.max_hp -= Screen.current_sword.hp()
        Screen.current_hp = Screen.max_hp
        Screen.current_sword = None

    def sell_shield(self):
        Screen.money += Screen.current_shield.value()
        Screen.max_hp -= Screen.current_shield.hp()
        Screen.current_hp = Screen.max_hp
        Screen.current_shield = None

class UpgradeMenu(Screen):
    def action(self):
        if Screen.current_sword != None:
            self.display_bg()
            self.disable_buttons()
            self.enable_buttons()
            screen.blit(Screen.current_sword.return_image(),(250,200))
            name_text = font.render(Screen.current_sword.return_name(), True,white,blue)
            screen.blit(name_text,(270,450))
            power_text = font.render("Power: " + str(Screen.current_sword.return_power()),True,white,blue)
            screen.blit(power_text,(530,300))
            level_text = font.render("level: " + str(Screen.current_sword.return_level()),True,white,blue)
            screen.blit(level_text,(530,250))
            price_text = font.render("Value: " + str(Screen.current_sword.value()),True,gold,blue)
            screen.blit(price_text,(530,450))
            money_text = font.render("Money:    " + str(Screen.money),False,gold,blue)
            screen.blit(money_text,(365,650))
            screen.blit(money_image,(482,647))
            if Screen.money < Screen.current_sword.level:
                money_color = red
            else:
                money_color = white
            cost_text = font.render("Cost:    "+ str(Screen.current_sword.level),True,money_color,blue)
            screen.blit(cost_text,(485,560))
            screen.blit(money_image,(567,557))
        else:
            Screen.current_screen.change_screen(main_menu)
    def upgrade_sword(self):
        if Screen.money >= Screen.current_sword.return_level():
            amount = Screen.current_sword.upgrade()
            if amount > 0:
                upgrade_sound.play()
            Screen.money -=Screen.current_sword.return_level()

class NewGame(Screen):
    def load_game(self):
        Screen.money, Screen.current_hp, Screen.max_hp, swordname, swordpower,shieldname, Screen.inventory = loadgame()
        if swordname != None:
            for i in range(len(swords_database)):
                if swords_database[i].return_name() == swordname:
                    Screen.current_sword = copy.copy(swords_database[i])
                    Screen.current_sword.set_power(swordpower)
        if shieldname != None:
            for i in range(len(shields_database)):
                if shields_database[i].return_name() == shieldname:
                    Screen.current_shield = shields_database[i]
        self.change_screen(main_menu)
        

class MainMenu(Screen):
    #in the main while loop, keep activating this function only if current_hp < max_hp
    next_time = datetime.datetime.now()

    def action(self):
        self.display_bg()
        self.disable_buttons()
        self.enable_buttons()
        Screen.current_map = None
        heal_price = int(((Screen.max_hp - Screen.current_hp)/100)*20)
        heal_text = font.render("Cost: " + str(heal_price),True,black,nature_green)
        screen.blit(heal_text,(670,780))
        if Screen.current_hp < Screen.max_hp:
            heal_time_cd = 0.5
            if Screen.inventory[5] == 1:
                heal_time_cd = 0.1
            delta = datetime.timedelta(seconds = heal_time_cd)
            period = datetime.datetime.now()
            if period >= self.next_time+delta:
                self.next_time += delta
                Screen.current_hp += 1
    def heal(self):
            heal_price = int(((Screen.max_hp - Screen.current_hp)/100)*20)
            if heal_price <= Screen.money:
                Screen.money -= heal_price
                Screen.current_hp = Screen.max_hp
                heal_price = 0

    def save_game(self):
        saving(Screen.money,Screen.current_hp,Screen.max_hp, Screen.current_sword,Screen.current_shield,Screen.inventory)

    def shop(self):
        self.disable_buttons_enable_buttons(shop_menu_buttons1,self.buttons_enabled)
        self.change_screen(shop_menu)

class Inventory(Screen):
    def open_inventory(self):
        screen.blit(inventory_bg_image,(0,0))
        screen.blit(wooden_frame2_image,(295,770))
        screen.blit(wooden_frame2_image,(355,770))
        screen.blit(wooden_frame2_image,(415,770))
        screen.blit(mushroom_token,(310,780))
        mushroom_amount = small_font.render(str(Screen.inventory[1]),False, white,None)
        screen.blit(mushroom_amount,(318,825))

        screen.blit(iron_ore_token,(365,780))
        iron_ore_amount = small_font.render(str(Screen.inventory[2]),False, white,None)
        screen.blit(iron_ore_amount,(378,825))

        screen.blit(gold_ore_token,(425,777))
        gold_ore_amount = small_font.render(str(Screen.inventory[3]),False, white,None)
        screen.blit(gold_ore_amount,(438,825))

        money_text = small_font.render("Money: " + str(Screen.money),False,gold,None)
        screen.blit(money_text,(420,280))
        screen.blit(money_image,(380,270))
        
        if Screen.current_sword != None:
            screen.blit(Screen.current_sword.return_image(),(100,200))
            name_text = small_font.render(Screen.current_sword.return_name(), True,Screen.current_sword.return_name_color(),None)
            screen.blit(name_text,(100,450))
            power_text = small_font.render("Power: " + str(Screen.current_sword.return_power()),True,black,None)
            screen.blit(power_text,(100,500))
            hp_text = small_font.render("+" + str(Screen.current_sword.hp()) + " HP",True,red,None)
            screen.blit(hp_text,(100,530))

        if Screen.current_shield != None:
            screen.blit(Screen.current_shield.return_image(),(700,200))
            shield_name_text = small_font.render(Screen.current_shield.return_name(), True,gold,blue)
            screen.blit(shield_name_text,(750,450))
            defence_text = small_font.render("Defence: " + str(Screen.current_shield.defence()), True,gold,blue)
            screen.blit(defence_text,(750,500))
            shield_hp_text = small_font.render("+" + str(Screen.current_shield.hp()) + " HP" ,False,black,red)
            screen.blit(shield_hp_text,(750,530))
        self.check_holy_charm()
        if Screen.inventory[5] == 1:
            screen.blit(evil_ring_image,(250,580))

    def check_holy_charm(self):
        self.enable_buttons()
        self.disable_buttons()
        if Screen.inventory[4] == 0:
            self.disable_specific_buttons([holy_charm_button])
        

            
    def close_inventory(self):
        Screen.previous_screen.disabled_buttons = False
        self.change_screen(Screen.previous_screen)


class NewGame_Scroll(Screen):
    premise = ["The goblin king has become corrupt,", "and is destroying every village," ,"leaving only corpses behind.",
            "We are the last village still standing.",
            "You must find the king and KILL HIM.","",
            "His wizards have cursed the forest,", "so it keeps changing.",
            "And his forces are always scouting.","", "Good luck","You will need it..."]
    
    quest1 = ["An evil magic protects the castle.", "The only one who can help you is", "Mob Barly.",
                "Unfortunatly he took acid..." ,"Now he never leaves the church.",
                "Find him,","he might be able to help you."]
    
    def action(self):
        next_button = self.buttons_enabled[0]
        ok_button = self.buttons_enabled[1]
        self.display_bg()
        self.disable_buttons()
        self.enable_buttons()
        self.disable_specific_buttons([finish_read_scroll])
        while next_button.isEnabled() or ok_button.isEnabled():
            main_loop()
            screen.blit(scroll_image,(150,120))
            if next_button.isEnabled():
                for i in range(len(self.premise)):
                    info = small_font.render(self.premise[i],True,black,white).convert()
                    info.set_colorkey(white)
                    screen.blit(info,(280,300+i*30))
            elif ok_button.isEnabled():
                for i in range(len(self.quest1)):
                    info = small_font.render(self.quest1[i],True,black,white).convert()
                    info.set_colorkey(white)
                    screen.blit(info,(280,300+i*30))

    def scroll_next(self):
        self.disable_buttons_enable_buttons([finish_read_scroll],[scroll_next_button])

    def finish_scroll(self):
        self.disable_specific_buttons([finish_read_scroll])
        self.change_screen(main_menu)

class Adventure(Screen):
    def action(self):
        self.display_bg()
        self.enable_buttons()
        self.disable_buttons()
        if Screen.current_map == None:
            Screen.current_map = forestgenerator.generate().head

class AdventureMap(Screen):
    def display_bg(self):
        screen.blit(Screen.current_map.image,(0,0))

    def play_bgm(self):
        node_type = Screen.current_map.node_type
        if node_type == 'regular':
            music = forest_music
        elif node_type.find('graveyard') >= 0:
            music = graveyard_music
        elif node_type.find('castle') >=0:
            if node_type == 'end castle':
                music = castle_music
            else:
                music = forest_music
        elif node_type.find('monastery') >= 0:
            if node_type == 'end monastery' or node_type == 'monastery room':
                music = monastery_music
            else:
                music = forest_music
        elif node_type.find('hollow tree') >= 0:
                music = hollow_tree_music
        else:
            music = forest_music
        if Screen.current_screen.bgm != None:
            if Screen.current_bgm != music:
                pygame.mixer.music.unload()
                pygame.mixer.music.load(music)
                pygame.mixer.music.play(-1)
                Screen.current_bgm = music
    def prev(self):
        Screen.current_map = Screen.current_map.prev

    def find_linear_func(self,x1,y1,x2,y2):
        delta_x = x1-x2
        if x1 == x2:
            return 0,0
        slope = (y1-y2)/delta_x
        b = y1-slope*x1
        return slope,b
    def dead(self):
        return
class ForestMap(AdventureMap):
    tried_to_spawn = False
    disabled_buttons = False
    MUSHROOM_SPAWN_CHANCE = 15
    IRON_ORE_SPAWN_CHANCE = 10
    GOLD_ORE_SPAWN_CHANCE = 12
    FROG_SPAWN_CHANCE = 1
    goblin_spawn_chance = 0
    gold_sack_enabled = [False,0]
    def action(self):
        if Screen.current_sword != None: 
            self.display_bg()
            self.play_bgm()
            self.enable_buttons()
            if not self.disabled_buttons:
                self.disable_buttons()
                self.disabled_buttons = True
                self.goblin_spawn_chance = random.random()
            mushroom_flag = False
            ################# Correct Buttons #################
            if self.gold_sack_enabled[0]:
                self.enable_specific_buttons([gold_sack_button])
            if type(Screen.current_map) == ComplexNode:
                self.disable_specific_buttons([forest_forward])
            else:
                if Screen.current_map.next == None:
                    self.disable_specific_buttons([forest_forward])
                self.disable_specific_buttons([forest_left,forest_right])
            if Screen.current_map.prev == None:
                self.disable_specific_buttons([forest_prev])
            if Screen.current_map.node_type == 'graveyard entrance':
                if Screen.inventory[4] == 0: #Holy charm obtained
                    cant_enter_text = bloody_font.render('Dark forces are blocking your path', True, red,None)
                    screen.blit(cant_enter_text,(250,430))
                    self.disable_specific_buttons([forest_forward])
                else:
                    self.enable_specific_buttons([forest_forward_to_GY])
            if Screen.current_map.node_type == 'end monastery':
                if Screen.inventory[0] == 1 and Screen.frog_quest_completed:
                    self.disable_buttons_enable_buttons([enter_monastery_done_button],[forest_forward])
                else:
                    self.disable_buttons_enable_buttons([enter_monastery_button],[forest_forward])
            if Screen.current_map.node_type == 'regular' and type(Screen.current_map) == RegularNode:
                mushroom_flag = True
                if self.goblin_spawn_chance < 0 and not Screen.current_map.combat:
                    Screen.current_map.combat = True
                    self.change_screen(goblin_fight)
            ################# Spawning somthing #################
            if self.tried_to_spawn == False and type(Screen.current_map) == RegularNode and Screen.current_map.node_type == 'regular':
                spawned_somthing = False
                if not Screen.current_map.spawned_somthing:
                    if Screen.frog_quest_accepted and Screen.inventory[0] == 0:
                        self.spawn_magic_frog()
                        self.tried_to_spawn = True
                    if mushroom_flag:
                        spawned_somthing = self.random_mushroom()
                    if Screen.current_sword.return_name() == "Copper Sword" and not spawned_somthing:
                        spawned_somthing = self.spawn_iron_ore()
                    elif Screen.current_sword.return_level() > 3 and not spawned_somthing:
                        spawned_somthing = self.spawn_gold_ore()
                if spawned_somthing:
                    Screen.current_map.spawned_somthing = False
                self.tried_to_spawn = True

    def forward(self):
        Screen.current_map = Screen.current_map.next
        self.tried_to_spawn = False
        self.disabled_buttons = False
    def forward_to_GY(self):
        Screen.current_map = Screen.current_map.next
        self.change_screen(gy_wave1)
    def prev(self):
        Screen.current_map = Screen.current_map.prev
        self.tried_to_spawn = False
        self.disabled_buttons = False

    def left(self):
        Screen.current_map = Screen.current_map.left
        self.tried_to_spawn = False
        self.disabled_buttons = False

    def right(self):
        Screen.current_map = Screen.current_map.right
        self.tried_to_spawn = False
        self.disabled_buttons = False

    def spawn_iron_ore(self):
        appear = random.randrange(self.IRON_ORE_SPAWN_CHANCE)
        success = False
        if appear == 0:
            self.enable_specific_buttons([iron_ore_button])
            iron_ore_button.setX(random.choice([random.randrange(100,200),random.randrange(700,800)]))
            iron_ore_button.setY(random.randrange(600,800))
            success = True
        return success
    
    def pick_gold_sack(self,button):
        self.disable_specific_buttons([button])
        Screen.money += self.gold_sack_enabled[1]
        self.gold_sack_enabled = [False,0]

    def collect_iron_ore(self):
        self.disable_specific_buttons([iron_ore_button])
        Screen.inventory[2] += 1

    def spawn_gold_ore(self):
        appear = random.randrange(self.GOLD_ORE_SPAWN_CHANCE)
        success = False
        if appear == 0:
            self.enable_specific_buttons([gold_ore_button])
            gold_ore_button.setX(random.choice([random.randrange(100,200),random.randrange(700,800)]))
            gold_ore_button.setY(random.randrange(600,800))
            success = True
        return success

    def collect_gold_ore(self):
        self.disable_specific_buttons([gold_ore_button])
        Screen.inventory[2] += 1

    def random_mushroom(self):
        appear = random.randrange(self.MUSHROOM_SPAWN_CHANCE)
        success = False
        if appear == 0:
            mushroom_i = random.randrange(len(mushroom_buttons))
            self.enable_specific_buttons([mushroom_buttons[mushroom_i]])
            success = True
        return success
    
    def collect_mushroom(self,button):
        Screen.inventory[1] += 1
        self.disable_specific_buttons([button])

    def spawn_magic_frog(self):
        appear = random.randrange(self.FROG_SPAWN_CHANCE)
        if appear >= 0:
            self.enable_specific_buttons([magic_frog_button])
            magic_frog_button.setX(random.randrange(100,800))
            magic_frog_button.setY(random.randrange(100,800))
            next_time = datetime.datetime.now()
            while magic_frog_button.isEnabled():
                self.display_bg()
                self.disable_specific_buttons([forest_forward,forest_prev])
                delta = datetime.timedelta(seconds = 0.4)
                period = datetime.datetime.now()
                if period >= next_time+delta:
                    next_time += delta
                    magic_frog_button.setX(random.randrange(100,800))
                    magic_frog_button.setY(random.randrange(100,800))
                main_loop()

    def collect_magic_frog(self):
        self.disable_specific_buttons([magic_frog_button])
        Screen.inventory[0] = 1

class Church(AdventureMap):
    def __init__(self,bgm,bg,buttons_enabled,dynamic_buttons,jesus_sleeps):
        super().__init__(bgm,bg,buttons_enabled,dynamic_buttons)
        self.jesus_sleeps = jesus_sleeps
    current_text = None
    picked_holy_charm = False
    
    jesus_text1 = ["The castle is protected by a dark magic",
                    "it can be disabled", 
                    "but only using an artifact from the Evil Necromancer"]
    jesus_text2 = ["There is a very rare magic frog in the forest", 
                    "Bring it to me, and i will help you."]
    jesus_text3 = ["My name is Mob Barly.",
                    "After many years of serving the king as his bard,",
                    "I decided to run away and set up my own church.",
                    "Unfortunately he cut off one of my toes before I escaped."]
    jesus_text4 =["You found it!","Take this holy charm, it will protect you in the graveyard",
                "Also, you can use it to go back home",
                "...",
                "I am going to lick this frog now."]
    jesus_text5 = ["Zzz..."]
    jesus_text6 = ["Have you found it yet?"]
    
    def action(self):
        if Screen.current_map.node_type == 'end monastery':
            Screen.current_map = Screen.current_map.next
            self.current_text = None
        self.display_bg()
        self.play_bgm()
        screen.blit(goblin_jesus_image,(410,320))
        if self.jesus_sleeps:
            self.disable_specific_buttons(Screen.ALL_BUTTONS)
            self.enable_specific_buttons([forest_prev])
            for i in range(len(self.jesus_text5)):
                text = cinzel_font.render(self.jesus_text5[i],True,black,white)
                screen.blit(text,(140,250+i*30))
        else:
            if Screen.current_map.node_type == 'end monastery':
                Screen.current_map = Screen.current_map.next
            self.disable_buttons()
            self.enable_buttons()
            if Screen.inventory[0] == 1:
                self.current_text = self.jesus_text4
                if not self.picked_holy_charm:
                    self.enable_specific_buttons([pick_holy_charm_button])
                    for button in self.buttons_enabled:
                        if button != forest_prev:
                            self.buttons_enabled.remove(button)
            if self.current_text != None:
                for i in range(len(self.current_text)):
                    text = cinzel_font.render(self.current_text[i],True,black,white)
                    screen.blit(text,(140,250+i*30))


    def castle_text(self):
        self.current_text = self.jesus_text1
    def quest_text(self):
        if not Screen.frog_quest_accepted:
            self.current_text = self.jesus_text2
            Screen.frog_quest_accepted = True
        else:
            self.current_text = self.jesus_text6
    def you_text(self):
        self.current_text = self.jesus_text3
    def prev(self):
        Screen.current_map = Screen.current_map.prev
        self.change_screen(forest_map)
        forest_map.disabled_buttons = False

    def pick_holy_charm(self,button):
        Screen.inventory[4] = 1
        self.picked_holy_charm = True
        self.disable_specific_buttons([button])
        Screen.frog_quest_completed = True

class GoblinFight(AdventureMap):
    '''Need to set sound_played and goblin_chosen to false everytime we switch to fight'''
    sound_played = False
    goblin_chosen = False
    current_enemy = None
    goblin_killed = False
    damage_dealt = []
    goblin_image = None
    hit_flag = False
    y_i = 0
    next_time = datetime.datetime.now()
    direction_x = random.choice([True,False])
    direction_y = random.choice([True,False])
    #use same bg and bgm as previous map
    #fight the goblin, once its dead go back to previous map
    def action(self):
        self.display_bg()

        if not self.goblin_chosen:
            goblin = random.choice(goblins)
            self.goblin_image = remove_background(goblin.return_image_name(),goblin.return_bg_color())
            self.current_enemy = copy.copy(goblin)
            self.goblin_chosen = True
            self.current_enemy.hp *= Screen.current_sword.return_level()
            self.current_enemy.power *= Screen.current_sword.return_level()
            self.y_i = 0
            self.play_bgm()
            self.enable_buttons()
            self.disable_buttons()
        start_dagger_x = 370
        start_dagger_y = 400
        self.show_health()
        attack_button_move_count_x = 0
        attack_button_move_count_y = 0
        #self.enable_specific_buttons(attack_button)

        if not self.sound_played:
            goblinsound = random.choice(goblin_sounds)
            goblinsound.play()
            self.sound_played = True

        if not self.goblin_killed and Screen.current_hp > 0:
            ########## All the visual assets ##########
            hp_text = font.render("Hp: " + str(self.current_enemy.return_hp()),True,black,teal)
            screen.blit(hp_text,(450,310))
            screen.blit(self.goblin_image, (370,370))

            ########## Dagger attacking health animation ##########
            if self.hit_flag == True and Screen.current_hp > 0:
                if start_dagger_y + self.y_i > 130 :
                    screen.blit(dagger_image,(start_dagger_x, start_dagger_y + self.y_i))
                    self.y_i -= 1
                else:
                    self.y_i = 0
                    self.hit_flag = False
                    if self.current_enemy != None:
                        if Screen.current_shield != None:
                            if self.current_enemy.return_power() - Screen.current_shield.defence() > 0:
                                Screen.current_hp -= self.current_enemy.return_power() - Screen.current_shield.defence()
                            else:
                                Screen.current_hp -= 1
                        else:
                            Screen.current_hp -=self.current_enemy.return_power()
                        
                        if Screen.current_hp < 0:
                            Screen.current_hp = 0
            ########## showing damage dealt ##########
            if len(self.damage_dealt) > 0:
                for dmg in self.damage_dealt:
                    dmg_text = font.render("-"+str(dmg[0]),True,red,None)
                    if dmg[1][1] >= 280:
                        dmg[1] = (dmg[1][0],dmg[1][1] + 1)
                        screen.blit(dmg_text,dmg[1])
                    else:
                        self.damage_dealt.remove(dmg)

            ########## goblin attacks you every 1 seconds ##########
            delta = datetime.timedelta(seconds = 1)
            period = datetime.datetime.now()
            if period >= self.next_time:
                self.next_time += delta
                self.hit_flag = True
            max_x = 700
            min_x = 300
            max_y = 700
            min_y = 300
            amount_to_move = 0.5
            if attack_button.getX() > max_x:
                attack_button.moveX(-amount_to_move)
                self.direction_x = random.choice([True,False])
            elif attack_button.getX() < min_x:
                attack_button.moveX(+amount_to_move)
                self.direction_x = random.choice([True,False])
            elif attack_button_move_count_x >= 100:
                self.direction_x = random.choice([True,False])
                attack_button_move_count_x = 0
            else:
                if self.direction_x:
                    attack_button.moveX(+amount_to_move)
                    attack_button_move_count_x += 1
                else:
                    attack_button.moveX(-amount_to_move)
                    attack_button_move_count_x += 1

            if attack_button.getY()>max_y:
                attack_button.moveY(-amount_to_move)
                self.direction_y = random.choice([True,False])
            elif attack_button.getY()<min_y:
                attack_button.moveY(+amount_to_move)
                self.direction_y = random.choice([True,False])
            elif attack_button_move_count_y >= 100:
                self.direction_y = random.choice([True,False])
                attack_button_move_count_y = 0
            else:
                if  self.direction_y:
                    attack_button.moveY(+amount_to_move)
                    attack_button_move_count_y += 1
                else:
                    attack_button.moveY(-amount_to_move)
                    attack_button_move_count_y += 1
        else:
            if Screen.current_hp == 0:
                self.dead()
            elif self.goblin_killed:
                self.change_screen(Screen.previous_screen)
                self.reset_variables()

    def reset_variables(self):
        self.sound_played = False
        self.goblin_chosen = False
        self.current_enemy = None
        self.goblin_killed = False
        self.damage_dealt = []
        self.goblin_image = None
        self.hit_flag = False

    def attack(self):
        damage = random.randrange(math.floor(Screen.current_sword.return_power()/2),Screen.current_sword.return_power()*2)
        if self.current_enemy.return_hp() - damage <= 0:
            self.current_enemy.hit(self.current_enemy.return_hp()) 
            self.goblin_killed = True
        else:
            self.current_enemy.hit(damage)
        self.damage_dealt.append([damage,(random.randrange(480,520),random.randrange(330,370))])


    def change_screen(self,new_screen):
        if new_screen != None:
            if type(new_screen) == ForestMap:
                new_screen.gold_sack_enabled = [True,int(self.current_enemy.drop())]
                new_screen.disabled_buttons = False
                Screen.previous_screen = Screen.current_screen
                Screen.current_screen = new_screen
class Graveyard(AdventureMap):
    def __init__(self,bgm,bg,buttons_enabled,dynamic_buttons,graveyard_index):
        super().__init__(bgm,bg,buttons_enabled,dynamic_buttons)
        self.graveyard_index = graveyard_index
    zombies_counter = 0
    zombie_summon_timer = 0
    left_zombies = []
    right_zombies = []
    left_zombies_moving = []
    right_zombies_moving = []
    summoned_zombie = False
    zombies_initiated = False
    next_time = datetime.datetime.now()
    wave_done = [False,False,False,False]
    def action(self):
        self.display_bg()
        self.play_bgm()
        self.show_health()
        if not self.zombies_initiated:
            self.init_zombies()
            self.zombies_initiated = True
        if self.zombies_counter > 0 and Screen.current_hp > 0 and self.wave_done[self.graveyard_index] == 0:
            kill_count_remaining = big_bloody_font.render(str(self.zombies_counter),True,colors.true_red,None)
            screen.blit(kill_count_remaining,(500,800))
            delta = datetime.timedelta(seconds = self.zombie_summon_timer)
            period = datetime.datetime.now()
            if period >= self.next_time:
                self.next_time += delta
                side = random.choice(["left","right"])
                self.summoned_zombie = True
            if self.summoned_zombie: 
                self.summoned_zombie = False
                if side == "left":
                    zombie = self.left_zombies.pop(random.randrange(len(self.left_zombies))) #each element in zombie moving is a zombie contains [[button,boolean],m,b]
                    self.left_zombies_moving.append(zombie)
                else:
                    zombie = self.right_zombies.pop(random.randrange(len(self.right_zombies)))
                    self.right_zombies_moving.append(zombie)

            for r_zombie in self.right_zombies_moving:
                if r_zombie[0][0].isEnabled() == False and r_zombie[0][1] == False:
                    r_zombie[0][0].enable()
                    r_zombie[0][0].show()
                    undead_sound = random.choice(undead_sounds)
                    undead_sound.play()
                elif r_zombie[0][1] == True:
                    r_zombie[0][1] = False
                    r_zombie[0][0].setX(r_zombie[3])
                    r_zombie[0][0].setY(r_zombie[4])
                    self.right_zombies.append(r_zombie)
                    self.right_zombies_moving.remove(r_zombie)
                elif r_zombie[0][0].getY() >= 130:
                        if r_zombie[0][2] == False: # zombie[0][2] == False means we are moving forward
                            r_zombie[0][0].moveX(-self.graveyard_index/2)
                            new_x1 = r_zombie[0][0].getX()
                            r_zombie[0][0].setY(r_zombie[1]*new_x1 + r_zombie[2])
                        else:
                            r_zombie[0][0].moveX(1)
                            new_x1 = r_zombie[0][0].getX()
                            r_zombie[0][0].setY(r_zombie[1]*new_x1 + r_zombie[2])
                            if r_zombie[0][0].getY() >= 300:
                                r_zombie[0][2] = False
                elif r_zombie[0][0].isEnabled():
                    Screen.current_hp -= 1
                    r_zombie[0][2] = True
                    r_zombie[0][0].moveX(1)
                    new_x1 = r_zombie[0][0].getX()
                    r_zombie[0][0].setY(r_zombie[1]*new_x1 + r_zombie[2])

            for l_zombie in self.left_zombies_moving:
                if l_zombie[0][0].isEnabled() == False and l_zombie[0][1] == False:
                    l_zombie[0][0].enable()
                    l_zombie[0][0].show()
                    undead_sound = random.choice(undead_sounds)
                    undead_sound.play()
                elif l_zombie[0][1] == True:
                    l_zombie[0][1] = False
                    l_zombie[0][0].setX(l_zombie[3])
                    l_zombie[0][0].setY(l_zombie[4])
                    self.left_zombies.append(l_zombie)
                    self.left_zombies_moving.remove(l_zombie)
                elif l_zombie[0][0].getY() >= 130:
                        if l_zombie[0][2] == False: # zombie[0][2] == False means we are moving forward
                            l_zombie[0][0].moveX(self.graveyard_index/3)
                            new_x1 = l_zombie[0][0].getX()
                            l_zombie[0][0].setY(l_zombie[1]*new_x1 + l_zombie[2])
                        else:
                            l_zombie[0][0].moveX(-1)
                            new_x1 = l_zombie[0][0].getX()
                            l_zombie[0][0].setY(l_zombie[1]*new_x1 + l_zombie[2])
                            if l_zombie[0][0].getY() >= 300:
                                l_zombie[0][2] = False
                elif l_zombie[0][0].isEnabled():
                    Screen.current_hp -= 1
                    l_zombie[0][2] = True
                    l_zombie[0][0].moveX(-1)
                    new_x1 = l_zombie[0][0].getX()
                    l_zombie[0][0].setY(l_zombie[1]*new_x1 + l_zombie[2])
        elif Screen.current_hp <= 0:
            self.dead()
        else:
            self.wave_done[self.graveyard_index] = 1
            self.disable_buttons_enable_buttons([forest_forward,forest_prev,inventory_button,exit_button],ALL_ZOMBIES_BUTTONS)

    def forward(self):
        if self.graveyard_index < 3:
            Screen.current_map = Screen.current_map.next
            self.zombies_initiated = False
            self.graveyard_index += 1
            self.init_zombies()

    def click_zombie(self,zombie_button):
        self.disable_specific_buttons([zombie_button])
        self.zombies_counter -= 1
        self.kill_zombie_in_list(zombie_button)

    def kill_zombie_in_list(self,zombie_button):
        found = False
        for zombie in zombies_left_buttons:
            if zombie[0] == zombie_button:
                zombie[1] = True
                found = True
        if not found:
            for zombie in zombies_right_buttons:
                if zombie[0] == zombie_button:
                    zombie[1] = True

    def init_zombies(self):
        y2 = 130
        x2 = x3 = 0
        for left_zombie in zombies_left_buttons:
            x3 = random.randrange(370,470)
            left_zombie[0].setX(random.randrange(5,100))
            left_zombie[0].setY(random.randrange(650,850))
            x1 = left_zombie[0].getX()
            y1 = left_zombie[0].getY()
            m,b = self.find_linear_func(x1,y1,x3,y2)
            self.left_zombies.append([left_zombie,m,b,x1,y1])
        for right_zombie in zombies_right_buttons:
            x2 = random.randrange(470,570)
            right_zombie[0].setX(random.randrange(800,950))
            right_zombie[0].setY(random.randrange(650,850))
            x1 = right_zombie[0].getX()
            y1 = right_zombie[0].getY()
            m,b = self.find_linear_func(x1,y1,x2,y2)
            self.right_zombies.append([right_zombie,m,b,x1,y1])
        self.zombies_counter = 10*self.graveyard_index
        self.zombie_summon_timer = 3/self.graveyard_index
        self.disable_buttons()

def main_loop():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            quit()
    pygame.event.clear()
    pw.update(events)
    pygame.display.update()  

new_game = NewGame(TOWN_MUSIC,town_image,new_game_buttons,False)
main_menu = MainMenu(TOWN_MUSIC,town_image,main_menu_buttons,False)
new_game_scroll_menu = NewGame_Scroll(TOWN_MUSIC,town_image,[scroll_next_button,finish_read_scroll],True)
inventory_screen = Inventory(None,inventory_bg_image,inventory_buttons,True)
shop_menu = Screen(None,shop_image,shop_menu_buttons1,True)
shop_sub_menu = Screen(None,shop_image,shop_menu_buttons2,True)
sword_buying_menu = Shop(None,shop_image,buying_menu_buttons,True,Sword)
shield_buying_menu = Shop(None,shop_image,buying_menu_buttons,True,Shield)
upgrade_menu = UpgradeMenu(None,background_image,upgrade_screen_buttons,True)
sell_menu = SellMenu(None,shop_image,sell_screen_buttons,True)
forest_entrance = Adventure(None,forest_entrance_image,adventure_buttons,False)
forest_map = ForestMap(forest_music,None,forest_map_buttons,True)
church_map = Church(monastery_music,None,church_buttons,False,False)
church_map_done = Church(monastery_music,None,church_buttons,False,True)
goblin_fight = GoblinFight(None,None,[attack_button],False)
gy_wave1 = Graveyard(graveyard_music,None,[],True,1)


def main():
    run = Screen.running
    pygame.mouse.set_cursor(cursor)
    Screen.current_screen = new_game

    while(run):
        main_loop()
        the_screen = Screen.current_screen
        if the_screen == inventory_screen:
            the_screen.open_inventory()
        else:
            the_screen.action()
        if the_screen != new_game_scroll_menu and the_screen != new_game:
            the_screen.show_health()

        
        #if Screen.start_new_game:
            #the_screen = new_game

main()


########################## Buttons ##########################

'''
scroll_next_button = Button(
    screen, 650, 750, 100, 50, text='Next',
    fontSize=20, margin=20,
    inactiveColour = tan,
    hoverColour=(150,0,0),
    pressedColour=(0, 255, 0), radius=20,
    onClick = lambda: _new_game())

finish_read_scroll = Button(
    screen, 450, 750, 100, 50, text='Ok',
    fontSize=20, margin=20,
    inactiveColour = tan,
    hoverColour=(150,0,0),
    pressedColour=(0, 255, 0), radius=20,
    onClick = lambda: _main_menu())

magic_frog_button = Button(
    screen, 450, 500, 50, 50,
    image = magic_frog_image,
    pressedColour=(0, 255, 0), radius=20,
    onClick = lambda: magic_frog()) 

buy_button = Button(
    screen, 300, 550, 100, 50, text='Buy',
    fontSize=20, margin=20,
    inactiveColour=gold,
    hoverColour=(150,0,0),
    pressedColour=orange, radius=20,
    onClick = lambda: buy())

upgrade_sword_button = Button(
    screen, 370, 550, 100, 50, text='Upgrade',
    fontSize=20, margin=20,
    inactiveColour=darker_blue,
    hoverColour=(150,0,0),
    pressedColour=orange, radius=20,
    onClick = lambda: upgrade_sword())
    
sell_sword_button = Button(
    screen, 270, 550, 100, 50, text='Sell',
    fontSize=20, margin=20,
    inactiveColour = gold,
    hoverColour=(150,0,0),
    pressedColour=(0, 255, 0), radius=20,
    onClick = lambda: sell_sword())

sell_shield_button = Button(
    screen, 470, 550, 100, 50, text='Sell',
    fontSize=20, margin=20,
    inactiveColour = gold,
    hoverColour=(150,0,0),
    pressedColour=(0, 255, 0), radius=20,
    onClick = lambda: sell_shield())





next_button = Button(
    screen, 700, 400, 100, 50, text='Next',
    fontSize=20, margin=20,
    inactiveColour=gold,
    hoverColour=(150,0,0),
    pressedColour = orange, radius=20,
    onClick = lambda: next_sword())

previous_button = Button(
    screen, 100, 400, 100, 50, text='Previous',
    fontSize=20, margin=20,
    inactiveColour=gold,
    hoverColour = (150,0,0),
    pressedColour = orange, radius=20,
    onClick = lambda: previous_sword())

swords_shop_button = Button(
    screen, 600, 400, 200, 100, text='Swords',
    fontSize=50, margin=20,
    inactiveColour=gold,
    hoverColour = (150,0,0),
    pressedColour = orange, radius=20,
    onClick = lambda: shop("sword"))

shields_shop_button = Button(
    screen, 200, 400, 200, 100, text='Shields',
    fontSize=50, margin=20,
    inactiveColour=gold,
    hoverColour = (150,0,0),
    pressedColour = orange, radius=20,
    onClick = lambda: shop("shield"))

back_shop_button = Button(
    screen, 220, 100, 100, 50, text='Back',
    fontSize=20, margin=20,
    inactiveColour=gold,
    hoverColour=(150,0,0),
    pressedColour=orange, radius=20,
    onClick = lambda: shop_buy_sell_menu())

shop_selling_button = Button(
    screen, 600, 400, 200, 100, text='Sell',
    fontSize=50, margin=20,
    inactiveColour = gold,
    hoverColour=(150,0,0),
    pressedColour=(0, 255, 0), radius=20,
    onClick = lambda: sell_window())

shop_buying_button = Button(
    screen, 200, 400, 200, 100, text='Buy',
    fontSize=50, margin=20,
    inactiveColour = gold,
    hoverColour=(150,0,0),
    pressedColour=(0, 255, 0), radius=20,
    onClick = lambda: shop_menu())

back_to_buy_sell_button = Button(
    screen, 220, 100, 100, 50, text='Back',
    fontSize=20, margin=20,
    inactiveColour=gold,
    hoverColour=(150,0,0),
    pressedColour=orange, radius=20,
    onClick = lambda: shop_buy_sell_menu())

return_to_menu_button = Button(
    screen, 100, 100, 100, 50, text='Menu',
    fontSize=20, margin=20,
    inactiveColour=gold,
    hoverColour=(150,0,0),
    pressedColour=orange, radius=20,
    onClick = lambda: main_menu())

################### Goblin Jesus chat buttons ###################
question1_button = Button(
    screen, 600, 650, 100, 50, text='Castle?',
    fontSize=30, margin=20,
    inactiveColour = gold,
    hoverColour=(150,0,0),
    pressedColour=(0, 255, 0), radius=20,
    onClick = lambda: question(jesus_text1))

question2_button = Button(
    screen, 450, 650, 100, 50, text='Help?',
    fontSize=30, margin=20,
    inactiveColour = gold,
    hoverColour=(150,0,0),
    pressedColour=(0, 255, 0), radius=20,
    onClick = lambda: question(jesus_text2,True))

question3_button =  Button(
    screen, 300, 650, 100, 50, text="You?",
    fontSize=30, margin=20,
    inactiveColour = gold,
    hoverColour=(150,0,0),
    pressedColour=(0, 255, 0), radius=20,
    onClick = lambda: question(jesus_text3))

questions = [question1_button,question2_button,question3_button]
def disable_questions():
    for i in range(len(questions)):
        questions[i].disable()
        questions[i].hide()



player_inventory_button_adventure = Button(
    screen, 900, 800, 100, 50,
    fontSize = 20, margin = 20,
    inactiveColour= gold,
    image = inventory_image,
    hoverColour=(150,0,0),
    pressedColour = orange, radius=20,
    onClick = lambda: open_inventory())

back_to_adventure_button = Button(
    screen, 900, 800, 100, 50,
    fontSize = 20, margin = 20,
    inactiveColour= gold,
    image = inventory_image,
    hoverColour=(150,0,0),
    pressedColour = orange, radius=20,
    onClick = lambda: forest_map(current_map,False))
x_rand_pos = 300
y_rand_pos = 700

attack_button1 = Button(
    screen, random.randrange(x_rand_pos,y_rand_pos), random.randrange(x_rand_pos,y_rand_pos), 50,50,
    image = attack_button_image,
    pressedColour = lavender, radius=20,
    onClick = lambda: attack())

attack_button2= Button(
    screen, random.randrange(x_rand_pos,y_rand_pos), random.randrange(x_rand_pos,y_rand_pos), 50,50,
    image = attack_button_image,
    pressedColour = lavender, radius=20,
    onClick = lambda: attack())

attack_button3= Button(
    screen, random.randrange(x_rand_pos,y_rand_pos), random.randrange(x_rand_pos,y_rand_pos), 50,50,
    image = attack_button_image,
    pressedColour = lavender, radius=20,
    onClick = lambda: attack())

attack_button4= Button(
    screen, random.randrange(x_rand_pos,y_rand_pos), random.randrange(x_rand_pos,y_rand_pos), 50,50,
    image = attack_button_image,
    pressedColour = lavender, radius=20,
    onClick = lambda: attack())

attack_button5= Button(
    screen, random.randrange(x_rand_pos,y_rand_pos), random.randrange(x_rand_pos,y_rand_pos), 50,50,
    image = attack_button_image,
    pressedColour = lavender, radius=20,
    onClick = lambda: attack())

attack_buttons_array = [attack_button1,attack_button2,attack_button3,attack_button4,attack_button5]



start_fight_button = Button(
    screen, 370, 650, 300, 150, text='Start',
    fontSize=50, margin=20,
    inactiveColour= tan,
    hoverColour = gold,
    pressedColour = orange, radius=20,
    onClick = lambda: start_fight())

enter_catacomb_button = Button(
    screen, 460, 340, 100, 50, text='Enter',
    fontSize=30, margin=20,
    inactiveColour= white,
    hoverColour = gold,
    pressedColour = orange, radius=20,
    onClick = lambda: graveyard_fight()) 

def undead_goblin_kill(button):
    global goblin_undead_exist,undead_kills
    if goblin_undead_exist[0] == True:
        goblin_undead_exist[0]= False
    elif goblin_undead_exist[1] == True:
        goblin_undead_exist[1]= False
    button.disable()
    button.hide()
    undead_kills += 1

goblin_undead_image = remove_background(goblin_undead.image_name,goblin_undead.return_bg_color())

cursed_skull_button = Button(
    screen,300,450,50,50,
    image = cursed_skull_image,
    pressedColour = orange, radius=20,
    onClick = lambda: None)

black_hole_button = Button(
    screen,100,400,100,100,
    image = black_hole_image,
    pressedColour = orange, radius=20,
    onClick = lambda: black_hole_click())

undead_goblin_button1 = Button(
    screen,random.randrange(100,200), random.randrange(500,800),50,50,
    image = goblin_undead_image,
    pressedColour = orange, radius=20,
    onClick = lambda: undead_goblin_kill(undead_goblin_button1))

undead_goblin_button2 = Button(
    screen,random.randrange(500,800), random.randrange(500,800),50,50,
    image = goblin_undead_image,
    pressedColour = orange, radius=20,
    onClick = lambda: undead_goblin_kill(undead_goblin_button2))

attack_wizard_button = Button(
    screen, 500,750, 50,50,
    image = attack_button_image,
    pressedColour = lavender, radius=20,
    onClick = lambda: attack())

def reset_combat():
    global kill_count
    for i in range(len(kill_count)):
        kill_count[i] = 0

reset_combat_button = Button(
    screen, 700, 100, 100, 50, text='reset',
    fontSize = 20, margin = 20,
    inactiveColour= gold,
    hoverColour=(150,0,0),
    pressedColour = orange, radius=20,
    onClick = lambda: reset_combat())

goldsack_button = Button(screen,450,450,50,50,
    image = goldsack_image,
    hoverColour = white,
    inactiveColour = gold,
    pressedColour = gold, radius=20, margain = 50,
    onClick = lambda: gold_sack_dis())

iron_ore_button = Button(
    screen, 300,700, 50,50,
    image = iron_ore_image,
    inactiveColour = light_gray,
    pressedColour = lavender, radius=20,
    onClick = lambda: collect_iron_ore())

gold_ore_button = Button(
    screen, 300,700, 50,50,
    image = gold_ore_image,
    inactiveColour = light_gray,
    pressedColour = lavender, radius=20,
    onClick = lambda: collect_gold_ore())


enter_hollow_tree_button = Button(
    screen, 680, 580, 100, 50, text='Enter',
    fontSize=30, margin=20,
    inactiveColour= white,
    hoverColour = gold,
    pressedColour = orange, radius=20,
    onClick = lambda: forward_map()) 

forest_forward = Button(
    screen, 480,250,30,30,
    pressedColour = orange, 
    image = forward_image,
    onClick = lambda: forward_map())

forest_right = Button(
    screen, 800, 500, 70, 52,
    pressedColour = orange, 
    image = forest_right_image,
    onClick = lambda: right_map())

forest_left = Button(
    screen, 100, 500, 70, 52,
    image =forest_left_image,
    pressedColour = orange,
    onClick = lambda: left_map()) 

forest_prev = Button(
    screen, 480, 850, 30,30,
    image = forest_previous_image,
    pressedColour = orange,
    onClick = lambda: previous_map()) 

talk_to_fairy_button = Button(
    screen, 475, 620, 100, 50, text='Talk',
    fontSize = 20, margin = 20,
    inactiveColour= green,
    hoverColour = gold,
    pressedColour = goblin_green, radius=20,
    onClick = lambda: talk_to_fairy())

enter_monastery_button = Button(
    screen, 480, 560, 100, 50, text='Enter',
    fontSize=30, margin=20,
    inactiveColour= white,
    hoverColour = gold,
    pressedColour = orange, radius=20,
    onClick = lambda: forward_map()) 

mushroom1_button = Button(
    screen, 300,700, 50,50,
    image = mushroom1_image,
    inactiveColour = nature_green,
    pressedColour = lavender, radius=20,
    onClick = lambda: mushroom_clicked(mushroom1_button))

mushroom2_button = Button(
    screen, 350,600, 50,50,
    image = mushroom2_image,
    inactiveColour = nature_green,
    pressedColour = lavender, radius=20,
    onClick = lambda: mushroom_clicked(mushroom2_button))

mushroom3_button = Button(
    screen, 320,800, 50,50,
    image = mushroom3_image,
    inactiveColour = nature_green,
    pressedColour = lavender, radius=20,
    onClick = lambda: mushroom_clicked(mushroom3_button))

mushroom4_button = Button(
    screen, 633,700, 50,50,
    image = mushroom4_image,
    inactiveColour = nature_green,
    pressedColour = lavender, radius=20,
    onClick = lambda: mushroom_clicked(mushroom4_button))

mushroom5_button = Button(
    screen, 700,700, 50,50,
    image = mushroom5_image,
    inactiveColour = nature_green,
    pressedColour = lavender, radius=20,
    onClick = lambda: mushroom_clicked(mushroom5_button))

mushroom_buttons = [mushroom1_button,mushroom2_button,mushroom3_button,mushroom4_button,mushroom5_button]

holy_charm_button = Button(
    screen, 470,700, 50,50,
    image = holy_charm_image,
    inactiveColour = gold,
    pressedColour = lavender, radius=20,
    onClick = lambda: holy_charm())

holy_charm_activate_button = Button(
    screen, 650,650, 50,50,
    image = holy_charm_image,
    inactiveColour = gold,
    hoverColour = light_gray,
    pressedColour = orange, radius=20,
    onClick = lambda: main_menu())

evil_ring_button = Button(
    screen, 600,480, 50,50,
    image = evil_ring_image,
    inactiveColour = black,
    hoverColour = purple,
    pressedColour = lavender, radius=20,
    onClick = lambda: pick_evil_ring())

z_b_width = 50
z_b_length = 50

goblin_zombie_right_button1 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie1_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_right_button1))

goblin_zombie_right_button2 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie2_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_right_button2))

goblin_zombie_right_button3 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie3_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_right_button3))

goblin_zombie_right_button4 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie4_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_right_button4))

goblin_zombie_right_button5 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie5_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_right_button5))

goblin_zombie_right_button6 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie6_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_right_button6))

goblin_zombie_right_button7 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie7_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_right_button7))

goblin_zombie_right_button8 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie1_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_right_button8))

goblin_zombie_right_button9 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie2_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_right_button9))

goblin_zombie_right_button10 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie3_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_right_button10))

goblin_zombie_right_button11 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie4_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_right_button11))

goblin_zombie_right_button12 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie5_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_right_button12))

goblin_zombie_right_button13 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie6_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_right_button13))

goblin_zombie_right_button14 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie7_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_right_button14))

goblin_zombie_right_button15 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie7_right_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_right_button15))

goblin_zombie_left_button1 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie1_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_left_button1))

goblin_zombie_left_button2 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie2_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_left_button2))

goblin_zombie_left_button3 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie3_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_left_button3))

goblin_zombie_left_button4 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie4_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_left_button4))

goblin_zombie_left_button5 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie5_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_left_button5))

goblin_zombie_left_button6 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie6_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_left_button6))

goblin_zombie_left_button7 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie7_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_left_button7))

goblin_zombie_left_button8 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie1_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_left_button8))

goblin_zombie_left_button9 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie2_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_left_button9))

goblin_zombie_left_button10 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie3_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_left_button10))

goblin_zombie_left_button11 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie4_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_left_button11))

goblin_zombie_left_button12 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie5_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_left_button12))

goblin_zombie_left_button13 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie6_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_left_button13))

goblin_zombie_left_button14 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie7_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_left_button14))

goblin_zombie_left_button15 = Button(
    screen,100,100,z_b_width,z_b_length,
    image = zombie7_left_image,
    pressedColour = orange, radius=20,
    onClick = lambda: click_zombie(goblin_zombie_left_button15))

# each element in index i contains a list of three items. the first item is an indexed button, the second item is a boolean indicating button enabled/disabled, 
# third element is boolean indicating if zombie moving forward or backwards (False => moving forward)
zombies_right_buttons = [[goblin_zombie_right_button1,False,False],[goblin_zombie_right_button2,False,False],[goblin_zombie_right_button3,False,False],[goblin_zombie_right_button4,False,False],
                         [goblin_zombie_right_button5,False,False],[goblin_zombie_right_button6,False,False],[goblin_zombie_right_button7,False,False],[goblin_zombie_right_button8,False,False],
                         [goblin_zombie_right_button9,False,False],[goblin_zombie_right_button10,False,False],[goblin_zombie_right_button11,False,False],[goblin_zombie_right_button12,False,False],
                         [goblin_zombie_right_button13,False,False],[goblin_zombie_right_button14,False,False],[goblin_zombie_right_button15,False,False]]

zombies_left_buttons = [[goblin_zombie_left_button1,False,False],[goblin_zombie_left_button2,False,False],[goblin_zombie_left_button3,False,False],[goblin_zombie_left_button4,False,False],
                         [goblin_zombie_left_button5,False,False],[goblin_zombie_left_button6,False,False],[goblin_zombie_left_button7,False,False],[goblin_zombie_left_button8,False,False],
                         [goblin_zombie_left_button9,False,False],[goblin_zombie_left_button10,False,False],[goblin_zombie_left_button11,False,False],[goblin_zombie_left_button12,False,False],
                         [goblin_zombie_left_button13,False,False],[goblin_zombie_left_button14,False,False],[goblin_zombie_left_button15,False,False]]
########################## Buttons ##########################
            

'''

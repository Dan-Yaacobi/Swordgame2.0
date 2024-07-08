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

upgrade_sound = pygame.mixer.Sound(os.path.join(current_dir,fr"soundeffects\upgrade_sound.mp3"))

goblin1_sound = pygame.mixer.Sound(os.path.join(current_dir,fr"soundeffects\goblin1.mp3"))

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

########## Town and Shop global variables ##########
money = 50
current_hp = 100
max_hp = 100
BASE_HP = 100
current_sword = None
current_shield = None
current_shop_item = None #"Sword" or "Shield"
current_viewing_item = None
current_viewing_item_index = 0
current_viewing_item_db = None
heal_price = 0
swords_database = []
shields_database = []
buying = False
reading_scroll = True
reading_scroll2 = True
MUSHY_SHIELD_COST = 15
GOLD_SHIELD_COST = 10
IRON_ORE_COST = 5
GOLD_ORE_COST = 10
goblin_jesus_quest_accepted = False
magic_frog_obtained = False
goblin_jesus_sleeping = False
jesus_talking = True
in_menu = True
in_upgrading_menu = False
in_buy_sell_menu = False

current_menu_screen = 'menu'
######### Inventory assets and global variables #########
carrot_inv_image = remove_background("carrot.png",colors.inv_carrot_bg)
unicorn_inv_image = remove_background("unicorn.png",colors.inv_unicorn_bg)
money_image = remove_background("money.png",colors.money_bg)
wooden_frame_image = pygame.image.load(os.path.join(current_dir, "wooden frame.png")) 
inventory_bg_image = pygame.image.load(os.path.join(current_dir, "inventory_bg.jpg"))
wooden_frame2_image = pygame.image.load(os.path.join(current_dir, "wooden frame2.png"))
inventory = [0,0,0,0,1,0] #0 = nothing yet, #1 = mushroom, #2 = iron ore, #3 = gold ore, #4 = Holy Charm #5 = Evil ring
inventory_pngs = [carrot_inv_image,unicorn_inv_image]
inventory_open = False
######## Forest generating global variables ########
goblin_undead_exist = [False,False]
undead_kills = 0
black_hole_can_spawn = True
goldsack_clicked_flag = False
current_enemy = None 
kill_index = 0
kill_count = [0,0]
start = False
fighting = False
forest_maps_to_goblin = 0
damage_dealt = 0
damage_dealt_flag = False
forks = 0
talked_to_fairy = False
the_forest = None
current_map = None
current_map_index = 0
current_map_type = None
current_music_type = 'regular'
dead_image = pygame.image.load(os.path.join(current_dir, "dead.jpg"))
chat_bubble = remove_background('chat bubble.png',(0,242,254),0.2)
scroll_image = remove_background('scroll.jpg',black)
jesus_clicked = False
black_hole_clicked = 0
zombies_counter = 0
graveyard_index = 0
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

###################### Health bar visuals ######################
full_health_image = remove_background(fr"healthbar\full_health.png",colors.healthbar_bg)
health_75_image = remove_background(fr"healthbar\75_health.png",colors.healthbar_bg)
half_health_image = remove_background(fr"healthbar\half_health.png",colors.healthbar_bg)
health_25_image = remove_background(fr"healthbar\25_health.png",colors.healthbar_bg)
health_40_image = remove_background(fr"healthbar\40_health.png",colors.healthbar_bg)
health_60_image = remove_background(fr"healthbar\60_health.png",colors.healthbar_bg)
health_90_image = remove_background(fr"healthbar\90_health.png",colors.healthbar_bg)
health_10_image = remove_background(fr"healthbar\10_health.png",colors.healthbar_bg)

inventory_image = remove_background("inventory.png",colors.inventory_bg)
goldsack_image = remove_background("goldsack.png",colors.goldsack_bg)
background_image =  pygame.image.load(os.path.join(current_dir, "Background.jpeg"))
background_rect = background_image.get_rect()
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
def main_loop():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            quit()
    pygame.event.clear()
    pw.update(events)
    pygame.display.update()


def main_menu(first_time_music_flag = False):
    global fighting,heal_price,inventory_open,jesus_talking,graveyard_index,current_hp,in_menu,zombies_counter,in_upgrading_menu,in_buy_sell_menu,current_menu_screen
    in_menu = True
    in_buy_sell_menu = False
    in_upgrading_menu = False
    print(f"in menu {in_menu}")
    zombies_counter = 0
    graveyard_index = 0
    jesus_talking = True
    inventory_open = False
    fighting = False
    pygame.mouse.set_cursor(cursor)
    if first_time_music_flag == False:
        pygame.mixer.music.unload()
        pygame.mixer.music.load(os.path.join(current_dir,"Into the Wilderness.mp3"))
        pygame.mixer.music.play(-1)
    end_fight()
    disable_zombies()
    disable_evil_ring_button()
    disable_holy_charm_activate_button()
    disable_ore_buttons()
    disable_holy_charm_button()
    disable_cursed_skull_button()
    disable_black_hole_button()
    disable_questions()
    disable_back_to_adventure_button()
    disable_enter_hollow_tree_button()
    disable_enter_catacomb_button()
    sell_buttons_disable()
    disable_previous_button()
    disable_forward_button()
    back_shop_button_disable()
    back_to_buy_sell_button_disable()
    disable_mushrooms()
    talk_to_fairy_button_disable()
    not_choosing_buy_or_sell_buttons()
    not_browsing_shop_items_buttons()
    disable_arrow_buttons()
    disable_gold_sack_button()
    dis_start_button()
    menu_button_disable()
    disable_inventory_not_menu()
    not_upgrading()
    not_attacking()
    not_shopping()
    new_game_button.disable()
    new_game_button.hide()
    load_button.disable()
    load_button.hide()
    premise = ["The goblin king has become corrupt,", "and is destroying every village," ,"leaving only corpses behind.",
                "We are the last village still standing.",
                "You must find the king and KILL HIM.","",
                "His wizards have cursed the forest,", "so it keeps changing.",
                "And his forces are always scouting.","", "Good luck","You will need it..."]
    
    quest1 = ["An evil magic protects the castle.", "The only one who can help you is", "Mob Barly.",
                "Unfortunatly he took acid..." ,"Now he never leaves the church.",
                "Find him,","he might be able to help you."]
    while(reading_scroll2):
        disable_reading_button()
        enable_scroll_next_button()
        main_loop()
        screen.blit(scroll_image,(150,120))
        for i in range(len(premise)):
            info = small_font.render(premise[i],True,black,white).convert()
            info.set_colorkey(white)
            screen.blit(info,(280,300+i*30))

    while(reading_scroll):
        enable_reading_button()
        main_loop()
        disable_scroll_next_button()
        screen.blit(scroll_image,(150,120))
        for i in range(len(quest1)):
            info = small_font.render(quest1[i],True,black,white).convert()
            info.set_colorkey(white)
            screen.blit(info,(280,300+i*30))

    disable_reading_button()
    shop_button.show()
    shop_button.enable()
    upgrade_button.show()
    upgrade_button.enable()
    fight_button.enable()
    fight_button.show()
    save_button.enable()
    save_button.show()
    heal_button.enable()
    heal_button.show()
    player_stats_button.enable()
    player_stats_button.show()
    reset_combat_button.enable()
    reset_combat_button.show()

    next_time = datetime.datetime.now()
    heal_time_cd = 0.5
    if inventory[5] == 1:
        heal_time_cd = 0.1
    while(current_menu_screen == 'menu'):
        screen.blit(town_image, town_image_rect)
        show_health()
        heal_price = heal(True)
        heal_text = font.render("Cost: " + str(heal_price),True,black,nature_green)
        screen.blit(heal_text,(670,780))
        ############## Heals +1 health every second while in town ##############
        delta = datetime.timedelta(seconds = heal_time_cd)
        period = datetime.datetime.now()
        if period >= next_time:
            next_time += delta
            if current_hp < max_hp:
                current_hp += 1
        main_loop()
    
    return
def exit_main_menu_to_shop():
    global fighting 
    fighting = False
    screen.blit(shop_image,shop_image_rect)
    menu_button()
    not_upgrading()
    not_in_menu()
    not_attacking()
    not_shopping()
    browsing_shop_items_buttons()

def exit_main_menu_to_upgrade_screen():
    global fighting 
    fighting = False
    screen.blit(background_image, background_rect)

    menu_button()
    upgrading()
    not_in_menu()
    not_attacking()
    not_shopping()

def new_game():
    screen.blit(town_image, town_image_rect)

    pygame.mixer.music.load(os.path.join(current_dir,"Into the Wilderness.mp3"))
    pygame.mixer.music.play(-1)

    new_game_button.enable()
    new_game_button.show()
    new_game_button.moveX(200)
    save_button.disable()
    save_button.hide()
    disable_zombies()
    disable_evil_ring_button()
    disable_holy_charm_activate_button()
    disable_holy_charm_button()
    disable_ore_buttons()
    disable_cursed_skull_button()
    disable_black_hole_button()
    disable_back_to_adventure_button()
    disable_inventory_not_menu()
    disable_questions()
    disable_frog_button()
    disable_scroll_next_button()
    disable_reading_button()
    disable_enter_hollow_tree_button()
    disable_enter_monastery_button()
    disable_enter_catacomb_button()
    sell_buttons_disable()
    back_to_buy_sell_button_disable()
    not_choosing_buy_or_sell_buttons()
    disable_previous_button()
    disable_mushrooms()
    disable_forward_button()
    back_shop_button_disable()
    talk_to_fairy_button_disable()
    not_browsing_shop_items_buttons()
    disable_arrow_buttons()
    disable_gold_sack_button()
    menu_button_disable()
    not_upgrading()
    not_in_menu()  
    not_shopping()
    not_attacking()


    t_end = time.time() + 60
    amount = 0.5
    button = new_game_button
    while time.time() < t_end and in_menu:
        screen.blit(town_image, town_image_rect)
        direction = random.choice([True,False])
        forward = random.choice([True,False])
        if direction:
            if forward and button.getX()<800:
                button.moveX(amount)
            elif button.getX() > 100:
                button.moveX(-amount)
        else:
            if forward and button.getY()<800:
                button.moveY(amount)
            elif button.getY() > 100:
                button.moveY(-amount)
        #screen.blit(pygame.transform.scale(magic_frog_image,(i,i)),(100,100))
        #i+= 1
        main_loop()

    while(running):
        main_loop()

def savegame():
    saving(money,current_hp,max_hp, current_sword,current_shield,inventory)

def load():
    global money, current_hp, current_sword,current_shield,inventory,max_hp,reading_scroll,reading_scroll2
    reading_scroll = False
    reading_scroll2 = False
    money, current_hp, max_hp, swordname, swordpower,shieldname,inventory = loadgame()
    if swordname != None:
        for i in range(len(swords_database)):
            if swords_database[i].return_name() == swordname:
                current_sword = copy.copy(swords_database[i])
                current_sword.set_power(swordpower)
    if shieldname != None:
        for i in range(len(shields_database)):
            if shields_database[i].return_name() == shieldname:
                current_shield = shields_database[i]
    main_menu(True)

def show_health():
    global current_hp, max_hp
    current_health_pcntg = (current_hp/max_hp)*100
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
    hp_text = font.render(str(current_hp) + "/" + str(max_hp),True,black,white)
    hp_text.set_colorkey(white)
    screen.blit(hp_text, (490,133))
    

####################### Hiding & Disabling / Showing & Enabling Buttons #######################

def not_attacking(flag = True):
    for i in range(len(attack_buttons_array)):
        attack_buttons_array[i].disable()
        attack_buttons_array[i].hide()
    if flag == True:
        no_zombies()
    not_attacking_wizard()
    
def not_in_menu():
    reset_combat_button.disable()
    reset_combat_button.hide() 
    player_stats_button.disable()
    player_stats_button.hide()
    shop_button.hide()
    shop_button.disable()
    upgrade_button.hide()
    upgrade_button.disable()
    fight_button.disable()
    fight_button.hide()

    heal_button.disable()
    heal_button.hide()
    dis_start_button()

def back_shop_button_disable():
    back_shop_button.disable()
    back_shop_button.hide()

def back_shop_button_enable():
    back_shop_button.enable()
    back_shop_button.show()

def not_shopping():
    buy_button.disable()
    buy_button.hide()
    next_button.disable()
    next_button.hide()
    previous_button.disable()
    previous_button.hide()

def shopping():
    not_browsing_shop_items_buttons()
    back_shop_button_enable()
    buy_button.enable()
    buy_button.show()
    next_button.enable()
    next_button.show()
    previous_button.enable()
    previous_button.show()

def browsing_shop_items_buttons():
    swords_shop_button.enable()
    swords_shop_button.show()
    shields_shop_button.enable()
    shields_shop_button.show()

def not_browsing_shop_items_buttons():
    swords_shop_button.disable()
    swords_shop_button.hide()
    shields_shop_button.disable()
    shields_shop_button.hide()

def choose_buy_or_sell_buttons():
    shop_buying_button.enable()
    shop_buying_button.show()
    shop_selling_button.enable()
    shop_selling_button.show()

def not_choosing_buy_or_sell_buttons():
    shop_buying_button.disable()
    shop_buying_button.hide()
    shop_selling_button.disable()
    shop_selling_button.hide()

def back_to_buy_sell_button_enable():
    back_to_buy_sell_button.enable()
    back_to_buy_sell_button.show()

def back_to_buy_sell_button_disable():
    back_to_buy_sell_button.disable()
    back_to_buy_sell_button.hide()
    
def sell_buttons_disable():
    sell_shield_button_disable()
    sell_sword_button_disable()

def sell_shield_button_disable():
    sell_shield_button.disable()
    sell_shield_button.hide()

def sell_shield_button_enable():
    sell_shield_button.enable()
    sell_shield_button.show()

def sell_sword_button_disable():
    sell_sword_button.disable()
    sell_sword_button.hide()

def sell_sword_button_enable():
    sell_sword_button.enable()
    sell_sword_button.show()

def not_upgrading():
    upgrade_sword_button.disable()
    upgrade_sword_button.hide()

def upgrading():
    upgrade_sword_button.enable()
    upgrade_sword_button.show()

def menu_button():
    return_to_menu_button.enable()
    return_to_menu_button.show()

def menu_button_disable():
    return_to_menu_button.disable()
    return_to_menu_button.hide()

def enable_attack_i(i):
    for j in range(len(attack_buttons_array)):
        if i == j:
            attack_buttons_array[j].enable()
            attack_buttons_array[j].show()
        else:
            attack_buttons_array[j].disable()
            attack_buttons_array[j].hide() 
    return attack_buttons_array[j] 

def disable_zombies():
    for zombie in zombies_left_buttons:
        zombie[0].disable()
        zombie[0].hide()
    for zombie in zombies_right_buttons:
        zombie[0].disable()
        zombie[0].hide()

def fighting_buttons():
    not_in_menu()
    not_shopping()
    not_upgrading
    menu_button_disable()
    main_loop()

def disable_ore_buttons():
    iron_ore_button.disable()
    iron_ore_button.hide()
    gold_ore_button.disable()
    gold_ore_button.hide()

def disable_holy_charm_button():
    holy_charm_button.disable()
    holy_charm_button.hide()
def disable_holy_charm_activate_button():
    holy_charm_activate_button.disable()
    holy_charm_activate_button.hide()
def disable_frog_button():
    magic_frog_button.disable()
    magic_frog_button.hide()
    
def enable_frog_button():
    magic_frog_button.enable()
    magic_frog_button.show()

def disable_reading_button():
    finish_read_scroll.disable()
    finish_read_scroll.hide()

def enable_reading_button():
    finish_read_scroll.enable()
    finish_read_scroll.show()

def disable_scroll_next_button():
    scroll_next_button.disable()
    scroll_next_button.hide()
    
def enable_scroll_next_button():
    scroll_next_button.enable()
    scroll_next_button.show()
    
def dis_start_button():
    start_fight_button.disable()
    start_fight_button.hide()

def disable_enter_catacomb_button():
    enter_catacomb_button.disable()
    enter_catacomb_button.hide()

def enable_enter_catacomb_button():
    enter_catacomb_button.enable()
    enter_catacomb_button.show()

def disable_enter_monastery_button():
    enter_monastery_button.disable()
    enter_monastery_button.hide()

def enable_enter_monastery_button():
    enter_monastery_button.enable()
    enter_monastery_button.show()

def disable_enter_hollow_tree_button():
    enter_hollow_tree_button.disable()
    enter_hollow_tree_button.hide()
    
def enable_enter_hollow_tree_button():
    enter_hollow_tree_button.enable()
    enter_hollow_tree_button.show()

def disable_inventory_not_menu():
    player_inventory_button_adventure.disable()
    player_inventory_button_adventure.hide()

def enable_inventory_not_menu():
    player_inventory_button_adventure.enable()
    player_inventory_button_adventure.show()

def disable_back_to_adventure_button():
    back_to_adventure_button.disable()
    back_to_adventure_button.hide()

def enable_back_to_adventure_button():
    back_to_adventure_button.enable()
    back_to_adventure_button.show()

def summon_undead_goblins1():
    undead_goblin_button1.enable()
    undead_goblin_button1.show()
    new_x = random.randrange(500,800)
    new_y = random.randrange(700,900)
    undead_goblin_button1.setX(new_x)
    undead_goblin_button1.setY(new_y)
    return undead_goblin_button1

def summon_undead_goblins2():
    undead_goblin_button2.enable()
    undead_goblin_button2.show()
    new_x = random.randrange(100,300)
    new_y = random.randrange(700,900)
    undead_goblin_button2.setX(new_x)
    undead_goblin_button2.setY(new_y)
    return undead_goblin_button2

def not_attacking_wizard():
    attack_wizard_button.disable()
    attack_wizard_button.hide()

def attacking_wizard():
    attack_wizard_button.enable()
    attack_wizard_button.show()
    return attack_wizard_button

def disable_black_hole_button():
    black_hole_button.disable()
    black_hole_button.hide()

def enable_black_hole_button(x,y):
    black_hole_button.enable()
    black_hole_button.show()
    black_hole_button.setX(x)
    black_hole_button.setY(y)

def disable_cursed_skull_button():
    cursed_skull_button.disable()
    cursed_skull_button.hide()

def enable_cursed_skull_button():
    cursed_skull_button.enable()
    cursed_skull_button.show()

def no_zombies():
    undead_goblin_button2.disable()
    undead_goblin_button2.hide()
    undead_goblin_button1.disable()
    undead_goblin_button1.hide()

def disable_gold_sack_button():
    goldsack_button.disable()
    goldsack_button.hide()

def disable_arrow_buttons():
    forest_right.disable()
    forest_right.hide()
    forest_left.disable()
    forest_left.hide()

def disable_forward_button():
    forest_forward.disable()
    forest_forward.hide()

def enable_forward_button():
    forest_forward.enable()
    forest_forward.show()

def disable_previous_button():
    forest_prev.disable()
    forest_prev.hide()

def enable_previous_button():
    forest_prev.enable()
    forest_prev.show()

def enable_arrow_buttons():
    forest_right.enable()
    forest_right.show()
    forest_left.enable()
    forest_left.show()

def talk_to_fairy_button_disable():
    talk_to_fairy_button.disable()
    talk_to_fairy_button.hide()

def disable_mushrooms():
    for i in range(len(mushroom_buttons)):
        mushroom_buttons[i].disable()
        mushroom_buttons[i].hide()
    return
def disable_evil_ring_button():
    evil_ring_button.disable()
    evil_ring_button.hide()
    
def enable_evil_ring_button():
    evil_ring_button.enable()
    evil_ring_button.show()
####################### Functions that activate everything #######################
def finish_read():
    global reading_scroll 
    reading_scroll = False
def next_scroll():
    global reading_scroll2
    reading_scroll2 = False

def dead():
    disable_gold_sack_button()
    disable_previous_button()
    disable_forward_button()
    no_zombies()
    not_attacking()
    disable_cursed_skull_button()
    screen.blit(dead_image,(0,0))   
    main_loop()
    time.sleep(3)
    main_menu()

def start_fight():
    global start,the_forest,fighting
    fighting = True
    the_forest = forestgenerator.generate()
    start = True

def end_fight():
    global start
    start = False

def gold_sack(flag):
    if flag == True:
        goldsack_button.enable()
        goldsack_button.show()
        global money,current_enemy
        money += int(current_enemy.drop()/current_sword.return_level())
        current_enemy = None
    return False

def gold_sack_dis():
    global goldsack_clicked_flag
    goldsack_clicked_flag = True
    disable_gold_sack_button()

def adventure():
    if current_sword != None:
        global goldsack_clicked_flag, kill_count,start,forest_maps_to_goblin,current_map,current_map_index,in_menu
        in_menu = False
        goldsack_clicked_flag = False
        current_map_index = 0
        fighting_buttons()
        while(start == False):
            start_fight_button.enable()
            start_fight_button.show()
            screen.blit(forest_entrance_image,forest_entrance_rect)
            main_loop()

        dis_start_button()
        current_map = the_forest
        #graveyard_fight()
        forest_map(the_forest.head)

def forward_map():
    global current_map_index
    current_map_index +=1
    forest_map(current_map.next)

def right_map():
    global current_map_index
    current_map_index +=1
    forest_map(current_map.right)

def left_map():
    global current_map_index
    current_map_index +=1
    forest_map(current_map.left)

def previous_map():
    global current_map_index
    current_map_index +=1
    forest_map(current_map.prev)

def music_for_type(node_type):
    global current_music_type
    graveyard_music = os.path.join(current_dir,"graveyard_bgm.mp3")
    forest_music = os.path.join(current_dir,"Into the Woods.mp3")
    castle_music = os.path.join(current_dir,"final_boss.mp3")
    monastery_music = os.path.join(current_dir,"monastery.mp3")
    hollow_tree_music = os.path.join(current_dir,"hollow tree.mp3")
    bgms = {'graveyard': graveyard_music,'regular': forest_music,'castle':forest_music,'end castle': castle_music,'end monastery': monastery_music,'end hollow tree': hollow_tree_music}
    if node_type.find('graveyard') >= 0:
        node_type = 'graveyard'
    current_music_type = node_type
    return bgms[node_type]

def forest_map(forest_map,mushroom_flag = True):
    global current_map,current_map_index,kill_count,current_map_type,current_music_type,inventory_open,jesus_talking,graveyard_index
    inventory_open = False
    max_steps = 100
    spawned_somthing = False
    if graveyard_index == 0 or graveyard_index >3:
         graveyard_index = 1
    disable_holy_charm_activate_button()
    disable_back_to_adventure_button()
    disable_enter_hollow_tree_button()
    disable_enter_catacomb_button()
    disable_enter_monastery_button()
    enable_inventory_not_menu()
    disable_ore_buttons()
    current_map = forest_map
    node_type = current_map.node_type
    ################## Deciding the music depending on the map type ##################
    music = 'regular'
    if current_map_index == 0:
        pygame.mixer.music.unload()
        pygame.mixer.music.load(music_for_type(music))
        pygame.mixer.music.play(-1)
    else:
        if node_type == 'regular':
            music = 'regular'
        elif node_type.find('graveyard') >= 0:
            music = 'graveyard'
        elif node_type.find('castle') >=0:
            if node_type == 'end castle':
                music = 'end castle'
            else:
                music = 'regular'
        elif node_type.find('monastery') >= 0:
            if node_type == 'end monastery' or node_type == 'monastery room':
                music = 'end monastery'
            else:
                music = 'regular'
        elif node_type.find('hollow tree') >= 0:
                music = 'end hollow tree' 
        else:
            music = 'regular'

    if type(forest_map) == RegularNode:
        if current_music_type != music:
            pygame.mixer.music.unload()
            pygame.mixer.music.load(music_for_type(music))
            pygame.mixer.music.play(-1)
    current_map_type = forest_map.node_type
    current_map.number = current_map_index
    disable_questions()
    disable_mushrooms()
    if type(current_map) == RegularNode and current_map.node_type == 'regular':
        if goblin_jesus_quest_accepted:
            spawn_magic_frog()
        if not current_map.spawned_somthing:
            if mushroom_flag:
                spawned_somthing = random_mushroom()
            if current_sword.return_name() == "Copper Sword" and not spawned_somthing:
                spawned_somthing = spawn_iron_ore()
            elif current_sword.return_level() >= 3 and not spawned_somthing:
                spawned_somthing = spawn_gold_ore()
        if spawned_somthing:
            current_map.spawned_somthing = True
    regular_goblin_fight_chance = random.random()
    while(running and fighting):
        if current_map_index > max_steps:
            disable_forward_button()
            disable_arrow_buttons()
            disable_previous_button()
            break
        else:
            screen.blit(current_map.image,(0,0))
            show_health()
            fatigue_text = small_font.render("steps left: " + f"{max_steps - current_map_index + 1}",False,black,None)
            screen.blit(fatigue_text,(465,175))
            enable_previous_button()

            if type(current_map) != ComplexNode:
                disable_arrow_buttons()
                if current_map.next == None:
                    disable_forward_button()
                if current_map.node_type == 'inside hollow tree':
                    enable_forward_button()
            if current_map.node_type == 'graveyard catacomb':
                enable_enter_catacomb_button()
                disable_forward_button()
            if current_map.node_type == 'graveyard':
                if not current_map.combat:
                    disable_forward_button()
                    disable_previous_button()
                    undead_waves(graveyard_index)
                    graveyard_index += 1
                    current_map.combat = True
                else:
                    enable_forward_button()
            elif current_map.node_type == 'graveyard entrance':
                if inventory[4] == 1: #Holy charm obtained
                    enable_forward_button()
                else:
                    cant_enter_text = bloody_font.render('Dark forces are blocking your path', True, red,None)
                    screen.blit(cant_enter_text,(250,430))
            elif current_map.node_type == 'end monastery':
                disable_forward_button()
                enable_enter_monastery_button()
            elif current_map.node_type == 'end hollow tree':
                enable_enter_hollow_tree_button()
                disable_forward_button()
            elif current_map.node_type == 'monastery room':
                goblin_jesus_image = remove_background(goblin_jesus.return_image_name(),goblin_jesus.return_bg_color(),0.08)
                screen.blit(goblin_jesus_image,(410,320))
                if magic_frog_obtained == True:
                    if goblin_jesus_sleeping == False:
                        question(jesus_text4)
                    else:
                        question(jesus_text5)
                else:
                    for i in range(len(questions)):
                        questions[i].enable()
                        questions[i].show()
            elif current_map == the_forest.head:
                disable_previous_button()
                enable_forward_button()
            elif type(current_map) == RegularNode and current_map.node_type == 'regular':
                if current_map.next != None: # regular goblin fight will not appear at any special maps (at the ends)
                    if current_map.combat == False: # each map can only have one combat event
                        if regular_goblin_fight_chance <= 0: # chance to summon a goblin
                            current_map.combat = True
                            kill_count[0]=0
                            fight_goblins(current_map.image,(0,0))
                        else:
                            enable_forward_button()
                    else:
                        enable_forward_button()
                else:
                    disable_forward_button()
            elif type(current_map) == ComplexNode:
                enable_arrow_buttons()
                disable_forward_button()
        main_loop()
    print(f"in forest {in_menu}")
    if current_map.number == current_map_index and not in_menu:
        jesus_talking = False
        screen.blit(fatigued_image,(0,0))
        pygame.mixer.music.fadeout(3000)
        disable_mushrooms()
        disable_inventory_not_menu()
        menu_button()


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

def click_zombie(zombie_button):
    global zombies_counter
    zombie_button.disable()
    zombie_button.hide()
    zombies_counter -= 1
    kill_zombie_in_list(zombie_button)

def kill_zombie_in_list(zombie_button):
    found = False
    for zombie in zombies_left_buttons:
        if zombie[0] == zombie_button:
            zombie[1] = True
            found = True
    if not found:
        for zombie in zombies_right_buttons:
            if zombie[0] == zombie_button:
                zombie[1] = True

def reset_zombie_deaths():
    for zombie in zombies_left_buttons:
        zombie[1] = False
    for zombie in zombies_right_buttons:
        zombie[1] = False
    
def undead_waves(graveyard_index):
    global zombies_counter,current_hp
    zombies_counter = 15*graveyard_index
    zombie_summon_timer = 2/graveyard_index
    left_zombies = []
    right_zombies = []
    left_zombies_moving = []
    right_zombies_moving = []
    summoned_zombie = False
    reset_zombie_deaths()
    x2 = 370
    y2 = 130
    x3 = 470
    for left_zombie in zombies_left_buttons:
        left_zombie[0].setX(random.randrange(50,200))
        left_zombie[0].setY(random.randrange(650,850))
        x1 = left_zombie[0].getX()
        y1 = left_zombie[0].getY()
        m,b = find_linear_func(x1,y1,x3,y2)
        left_zombies.append([left_zombie,m,b,x1,y1])
    for right_zombie in zombies_right_buttons:
        right_zombie[0].setX(random.randrange(650,850))
        right_zombie[0].setY(random.randrange(650,850))
        x1 = right_zombie[0].getX()
        y1 = right_zombie[0].getY()
        m,b = find_linear_func(x1,y1,x2,y2)
        right_zombies.append([right_zombie,m,b,x1,y1])
    next_time = datetime.datetime.now()
    while zombies_counter > 0:
        if current_hp <= 0:
            break
        screen.blit(current_map.image,(0,0))
        show_health()
        kill_count_remaining = big_bloody_font.render(str(zombies_counter),True,colors.true_red,None)
        screen.blit(kill_count_remaining,(500,800))
        delta = datetime.timedelta(seconds = zombie_summon_timer)
        period = datetime.datetime.now()
        if period >= next_time:
            next_time += delta
            side = random.choice(["left","right"])
            summoned_zombie = True
        if summoned_zombie: 
            summoned_zombie = False
            if side == "left":
                zombie = left_zombies.pop(random.randrange(len(left_zombies))) #each element in zombie moving is a zombie contains [[button,boolean],m,b]
                left_zombies_moving.append(zombie)
            else:
                zombie = right_zombies.pop(random.randrange(len(right_zombies)))
                right_zombies_moving.append(zombie)

        for r_zombie in right_zombies_moving:
            if r_zombie[0][0].isEnabled() == False and r_zombie[0][1] == False:
                r_zombie[0][0].enable()
                r_zombie[0][0].show()
                undead_sound = random.choice(undead_sounds)
                undead_sound.play()
            elif r_zombie[0][1] == True:
                r_zombie[0][1] = False
                r_zombie[0][0].setX(r_zombie[3])
                r_zombie[0][0].setY(r_zombie[4])
                right_zombies.append(r_zombie)
                right_zombies_moving.remove(r_zombie)
            elif r_zombie[0][0].getY() >= 130:
                    if r_zombie[0][2] == False: # zombie[0][2] == False means we are moving forward
                        r_zombie[0][0].moveX(-max((random.random()*(graveyard_index)/2),1))
                        new_x1 = r_zombie[0][0].getX()
                        r_zombie[0][0].setY(r_zombie[1]*new_x1 + r_zombie[2])
                    else:
                        r_zombie[0][0].moveX(1)
                        new_x1 = r_zombie[0][0].getX()
                        r_zombie[0][0].setY(r_zombie[1]*new_x1 + r_zombie[2])
                        if r_zombie[0][0].getY() >= 230:
                            r_zombie[0][2] = False
            elif r_zombie[0][0].isEnabled():
                current_hp -= 1
                r_zombie[0][2] = True
                r_zombie[0][0].moveX(1)
                new_x1 = r_zombie[0][0].getX()
                r_zombie[0][0].setY(r_zombie[1]*new_x1 + r_zombie[2])

        for l_zombie in left_zombies_moving:
            if l_zombie[0][0].isEnabled() == False and l_zombie[0][1] == False:
                l_zombie[0][0].enable()
                l_zombie[0][0].show()
                undead_sound = random.choice(undead_sounds)
                undead_sound.play()
            elif l_zombie[0][1] == True:
                l_zombie[0][1] = False
                l_zombie[0][0].setX(l_zombie[3])
                l_zombie[0][0].setY(l_zombie[4])
                left_zombies.append(l_zombie)
                left_zombies_moving.remove(l_zombie)
            elif l_zombie[0][0].getY() >= 130:
                    if l_zombie[0][2] == False: # zombie[0][2] == False means we are moving forward
                        l_zombie[0][0].moveX(max((random.random()*(graveyard_index)/2),1))
                        new_x1 = l_zombie[0][0].getX()
                        l_zombie[0][0].setY(l_zombie[1]*new_x1 + l_zombie[2])
                    else:
                        l_zombie[0][0].moveX(-1)
                        new_x1 = l_zombie[0][0].getX()
                        l_zombie[0][0].setY(l_zombie[1]*new_x1 + l_zombie[2])
                        if l_zombie[0][0].getY() >= 230:
                            l_zombie[0][2] = False
            elif l_zombie[0][0].isEnabled():
                current_hp -= 1
                l_zombie[0][2] = True
                l_zombie[0][0].moveX(-1)
                new_x1 = l_zombie[0][0].getX()
                l_zombie[0][0].setY(l_zombie[1]*new_x1 + l_zombie[2])

        main_loop()
    disable_zombies()
    if current_hp <= 0:
        dead()
    return

def question(jesus_text, frog = False):
    global goblin_jesus_sleeping,jesus_talking,inventory
    screen.blit(current_map.image,(0,0))
    goblin_jesus_image = remove_background(goblin_jesus.return_image_name(),goblin_jesus.return_bg_color(),0.08)
    screen.blit(goblin_jesus_image,(410,320))
    print("here")
    if jesus_text == jesus_text4:
        goblin_jesus_sleeping = True
        holy_charm_button.enable()
        holy_charm_button.show()
    while jesus_talking:
        for i in range(len(jesus_text)):
            text = cinzel_font.render(jesus_text[i],True,black,white)
            screen.blit(text,(140,250+i*30))
        if frog:
            global goblin_jesus_quest_accepted
            goblin_jesus_quest_accepted = True
        main_loop()

def holy_charm(use_the_charm = False):
    if not use_the_charm:
        global inventory
        inventory[4] = 1
        disable_holy_charm_button()
    else:
        main_menu()

def spawn_iron_ore():
    appear = random.randrange(10)
    success = False
    if appear == 0:
        iron_ore_button.enable()
        iron_ore_button.show()
        iron_ore_button.setX(random.choice([random.randrange(100,200),random.randrange(700,800)]))
        iron_ore_button.setY(random.randrange(600,800))
        success = True
    return success

def collect_iron_ore():
    global inventory
    iron_ore_button.disable()
    iron_ore_button.hide()
    inventory[2] += 1

def spawn_gold_ore():
    appear = random.randrange(15)
    success = False
    if appear == 0:
        gold_ore_button.enable()
        gold_ore_button.show()
        gold_ore_button.setX(random.choice([random.randrange(100,200),random.randrange(700,800)]))
        gold_ore_button.setY(random.randrange(600,800))
        success = True
    return success

def collect_gold_ore():
    global inventory
    gold_ore_button.disable()
    gold_ore_button.hide()
    inventory[2] += 1

def random_mushroom():
    appear = random.randrange(12)
    success = False
    if appear == 0:
        mushroom_i = random.randrange(len(mushroom_buttons))
        mushroom_buttons[mushroom_i].enable()
        mushroom_buttons[mushroom_i].show()
        success = True
    return success

def magic_frog():
    global magic_frog_obtained
    magic_frog_obtained = True
    disable_frog_button()

def spawn_magic_frog():
    appear = random.randrange(10)
    if appear <= 10:
        amount = 5
        button = magic_frog_button
        while magic_frog_obtained == False:
            screen.blit(current_map.image,(0,0))
            disable_forward_button()
            disable_previous_button()
            enable_frog_button()
            direction = random.choice([True,False])
            forward = random.choice([True,False])
            if direction:
                if forward and button.getX()<800:
                    button.moveX(amount)
                elif button.getX() > 100:
                    button.moveX(-amount)
            else:
                if forward and button.getY()<800:
                    button.moveY(amount)
                elif button.getY() > 100:
                    button.moveY(-amount)
            main_loop()

        

def accapt_jesus_quest():
    global goblin_jesus_quest_accepted
    goblin_jesus_quest_accepted = True

def open_inventory(menu = False):
    global inventory_open
    inventory_open = True
    not_in_menu()
    not_shopping()
    not_upgrading()
    disable_mushrooms()
    disable_ore_buttons()
    disable_enter_catacomb_button()
    disable_enter_hollow_tree_button()
    disable_enter_monastery_button()
    if menu == True:
        menu_button()
    else:
        enable_back_to_adventure_button()
    not_attacking()
    disable_arrow_buttons()
    disable_previous_button()
    disable_forward_button()
    while(inventory_open):
        screen.blit(inventory_bg_image,(0,0))
        screen.blit(wooden_frame2_image,(295,770))
        screen.blit(wooden_frame2_image,(355,770))
        screen.blit(wooden_frame2_image,(415,770))

        screen.blit(mushroom_token,(310,780))
        mushroom_amount = small_font.render(str(inventory[1]),False, white,None)
        screen.blit(mushroom_amount,(318,825))

        screen.blit(iron_ore_token,(365,780))
        iron_ore_amount = small_font.render(str(inventory[2]),False, white,None)
        screen.blit(iron_ore_amount,(378,825))

        screen.blit(gold_ore_token,(425,777))
        gold_ore_amount = small_font.render(str(inventory[3]),False, white,None)
        screen.blit(gold_ore_amount,(438,825))

        money_text = small_font.render("Money: " + str(money),False,gold,blue).convert()
        money_text.set_colorkey(blue)
        screen.blit(money_text,(420,280))
        screen.blit(money_image,(380,270))

        hp_text = small_font.render("HP: " + str(current_hp) + "/" + str(max_hp) ,False,black,red)
        screen.blit(hp_text,(400,320))
        
        if current_sword != None:
            screen.blit(current_sword.return_image(),(100,200))
            name_text = small_font.render(current_sword.return_name(), True,current_sword.return_name_color(),None)
            screen.blit(name_text,(100,450))
            power_text = small_font.render("Power: " + str(current_sword.return_power()),True,black,None)
            screen.blit(power_text,(100,500))
            hp_text = small_font.render("+" + str(current_sword.hp()) + " HP",True,red,None)
            screen.blit(hp_text,(100,530))

        if current_shield != None:
            screen.blit(current_shield.return_image(),(700,200))
            shield_name_text = small_font.render(current_shield.return_name(), True,gold,blue)
            screen.blit(shield_name_text,(750,450))
            defence_text = small_font.render("Defence: " + str(current_shield.defence()), True,gold,blue)
            screen.blit(defence_text,(750,500))
            shield_hp_text = small_font.render("+" + str(current_shield.hp()) + " HP" ,False,black,red)
            screen.blit(shield_hp_text,(750,530))
        if inventory[4] == 1:
            holy_charm_activate_button.enable()
            holy_charm_activate_button.show()
        if inventory[5] == 1:
            screen.blit(evil_ring_image,(250,580))
        main_loop()
    return

def heal(menu_flag):
    global money, current_hp,heal_price
    heal_price = int(((max_hp - current_hp)/100)*20)
    if menu_flag == False:
        if heal_price <= money:
            money -= heal_price
            current_hp = max_hp
            heal_price = 0
    else:
        return heal_price

def attack():
    global kill_count,kill_index,current_enemy,damage_dealt,damage_dealt_flag,undead_kills
    damage = random.randrange(current_sword.return_power(),current_sword.return_power()*2)
    damage_dealt = damage
    damage_dealt_flag = True
    main_loop()
    if current_enemy.return_hp() - damage <=0:
        current_enemy.hit(current_enemy.return_hp()) 
        kill_count[kill_index] += 1
        damage_dealt_flag = False
        undead_kills = 0
        damage_dealt = 0
    else:
        current_enemy.hit(damage)

def treeman_fight():
    return

def treeman_boss_fight():
    return

def black_hole_click():
    global black_hole_can_spawn, black_hole_clicked
    black_hole_clicked += 1

def pick_evil_ring():
    global inventory
    inventory[5] = 1
    disable_evil_ring_button()
    return

def graveyard_fight():
    ########### Declaring all the needed variables ###########
    global fighting, current_enemy,current_hp,money,damage_dealt_flag,kill_count
    global kill_index,goblin_undead_exist, undead_kills,goldsack_clicked_flag,black_hole_can_spawn,black_hole_clicked
    goldsack_clicked_flag = False
    fighting = True
    kill_index = 1   
    undead_kills = 0
    time_flag = False
    next_time2 = datetime.datetime.now()
    undead_rnd_kills = random.randrange(2,4)
    current_enemy = copy.copy(goblin_wizard)
    wizard_max_hp = current_enemy.return_hp()
    hit_flag = False
    y_i = 0
    start_felball_x = 370
    start_felball_y = 500
    current_x2 = start_felball_x2 = 770
    current_y2 = start_felball_y2 = 500
    current_x3 = start_felball_x3 = 100
    current_y3 = start_felball_y3 = 500
    m1,b1 = find_linear_func(start_felball_x2,start_felball_y2,370,100) 
    m2,b2 = find_linear_func(start_felball_x3,start_felball_y3,370,100)
    goldsack_flag = True
    money_text = font.render("+"+str(int(current_enemy.drop()/current_sword.return_level())),True,gold,black).convert()
    wizard_attack_time = 1
    black_hole_right_x = 800
    black_hole_left_x = 100
    cursed_mouse = False
    undead1_moving_up = False
    undead2_moving_up = False
    side = random.choice([True,False])
    black_hole_spawn_chance = 500
    atk_button_move = random.choice([True,False])
    black_hole_spawned = False
    black_hole_power = 1
    black_hole_counter = 0
    black_hole_counter_max = 100
    phase3_fel_pools = False
    atk_button_move_speed = 1
    atk_button_locations= [(100,100),(700,700),(100,700),(700,100)]
    atk_button_move_chance = 300
    new_x = 0
    ########### Disabling buttons which aren't needed ###########
    menu_button_disable()
    not_attacking()
    disable_arrow_buttons()
    disable_enter_catacomb_button()
    disable_previous_button()
    player_stats_button.disable()
    player_stats_button.hide()
    disable_inventory_not_menu()
    ########### Main fighting loop ###########
    if kill_count[kill_index] == 1:
        while(running):
            main_loop()
            screen.blit(necromancer_room_image,(0,0))
            enable_previous_button()
            show_health()
            disable_cursed_skull_button()
            return
    else:
        while(running and fighting):
            main_loop()
            screen.blit(necromancer_room_image,(0,0))
            ########### felball animation ###########
            if not phase3_fel_pools:
                if hit_flag == True and current_hp > 0 and current_enemy != None:
                    if start_felball_y + y_i > 130 :
                        screen.blit(felball_image,(start_felball_x, start_felball_y + y_i))
                        y_i -= 2
                    else:
                        y_i = 0
                        hit_flag = False
                        current_hp -= current_enemy.return_power()
                        if current_hp < 0:
                            current_hp = 0
                    #if phase3_fel_pools:
            elif current_hp > 0 and current_enemy != None:
                if current_y2 >= 100:
                    current_y2 = m1*current_x2 + b1
                    screen.blit(felball_image,(current_x2,current_y2))
                    current_x2 -= 1
                else:
                    current_x2 = start_felball_x2
                    current_y2 = start_felball_y2
                    current_hp -= current_enemy.return_power()

                if current_y3 >= 100:
                    current_y3 = m2*current_x3 + b2
                    screen.blit(felball_image,(current_x3,current_y3))
                    current_x3 += 1
                else:
                    current_x3 = start_felball_x3
                    current_y3 = start_felball_y3
                    current_hp -= current_enemy.return_power()

            show_health()
            if current_hp > 0 and current_enemy != None and kill_count[kill_index] == 0:
                    ########### Showing all the visual assets ###########
                    # Goblin Wizard image #
                    if not phase3_fel_pools:
                        screen.blit(goblin_wizard_image, (300,550))
                    else:
                        screen.blit(goblin_wizard_final_image,(300,400))

                    ######## Goblin Wizard attack every x seconds ########
                    delta2 = datetime.timedelta(seconds = wizard_attack_time)
                    period2 = datetime.datetime.now()
                    if period2 >= next_time2:
                        next_time2 += delta2
                        hit_flag = True
                    ################ Phase 1 ####################
                    if not attack_wizard_button.isEnabled():
                        ########### summoning black hole #############3
                        if black_hole_can_spawn:
                            if random.randrange(black_hole_spawn_chance) == 0:
                                side = random.choice([True,False])
                                black_hole_can_spawn = False
                                black_hole = pygame.transform.scale(black_hole_image,(50,50))
                                size = black_hole.get_size()

                        if not black_hole_can_spawn:
                            mouse_x,mouse_y = pygame.mouse.get_pos()
                            if size[0] < 170 and size[1]<170:
                                black_hole = pygame.transform.scale(black_hole_image,(size[0]+1,size[1]+1))
                                if side:
                                    screen.blit(black_hole,(black_hole_right_x,400))
                                else:
                                    screen.blit(black_hole,(black_hole_left_x,400))
                                size = black_hole.get_size()
                            else:
                                y1 = 450

                                if side:
                                    #screen.blit(black_hole,(black_hole_right_x,400))
                                    if not black_hole_spawned :
                                        enable_black_hole_button(black_hole_right_x + 35,435)
                                        black_hole_spawned = True
                                    if black_hole_counter <= black_hole_counter_max and black_hole_counter >= 0:
                                        if mouse_x <= black_hole_right_x + 85:
                                            new_x = mouse_x + black_hole_power
                                        if mouse_y >= 500:
                                            mouse_y -= black_hole_power
                                        if mouse_y <=450:
                                            mouse_y += black_hole_power
                                        if mouse_x >= black_hole_right_x + 85:
                                            new_x = mouse_x - black_hole_power
                                        m,b = find_linear_func(mouse_x,mouse_y,black_hole_right_x + 100,y1)
                                        pygame.mouse.set_pos((new_x,m*new_x + b))
                                    black_hole_hp = bloody_font.render(str(black_hole_clicked),True,nature_green,None)
                                    screen.blit(black_hole_hp,(black_hole_right_x+20,560))
                                    
                                elif not side:
                                    #screen.blit(black_hole,(black_hole_left_x,400))
                                    if not black_hole_spawned:
                                        enable_black_hole_button(black_hole_left_x + 35,435)
                                        black_hole_spawned = True
                                    if black_hole_counter <= black_hole_counter_max and black_hole_counter >= 0:
                                        if mouse_x  >= black_hole_left_x + 100:
                                            new_x = mouse_x -black_hole_power
                                        if mouse_y >= 500:
                                            mouse_y -= black_hole_power
                                        if mouse_y <=450:
                                            mouse_y += black_hole_power
                                        if mouse_x <= black_hole_left_x:
                                            new_x = mouse_x + black_hole_power
                                        m,b = find_linear_func(mouse_x,mouse_y,black_hole_left_x,y1)
                                        pygame.mouse.set_pos((new_x, m*new_x + b))
                                    black_hole_hp = bloody_font.render(str(black_hole_clicked),True,nature_green,None)
                                    screen.blit(black_hole_hp,(black_hole_left_x,560))
                                if black_hole_counter == black_hole_counter_max:
                                    black_hole_counter = -100
                                    black_hole_power += 1
                                black_hole_counter += 1
                        if black_hole_clicked >= 5:
                            disable_black_hole_button()
                            screen.blit(necromancer_room_image,(0,0))
                            if not phase3_fel_pools:
                                screen.blit(goblin_wizard_image, (300,550))
                            else:
                                screen.blit(goblin_wizard_final_image,(300,400))
                            black_hole_can_spawn = True
                            black_hole_spawned = False
                            black_hole_clicked = 0
                            black_hole_counter = 0
                            black_hole_power = 1
                        ######## Summoning undeads untill you kill random amount between 2 to 6 of them ########
                        if undead_kills < 2*undead_rnd_kills:
                            if goblin_undead_exist[0] == False and goblin_undead_exist[1] == False:
                                undead1 = summon_undead_goblins1()
                                undead2 = summon_undead_goblins2()
                                goblin_undead_exist[0] = True
                                goblin_undead_exist[1] = True
                                not_attacking_wizard()
                                wizard_attack_time = 1
                                disable_cursed_skull_button()
                            if not undead1_moving_up:
                                undead1.moveY(0.5)
                                if undead1.getY() >= 1000:
                                    if undead1.getX() <= 100:
                                        undead1.moveX(random.choice([50,100,150]))
                                    elif undead1.getX() >= 900:
                                        undead1.moveX(random.choice([-50,-100,-150]))
                                    else:
                                        undead1.moveX(random.choice([-100,-50,50,100]))
                                    undead1_moving_up = True
                            else:
                                undead1.moveY(-1)
                                if undead1.getY() == 699:
                                    undead1_moving_up = False

                            if not undead2_moving_up:
                                undead2.moveY(0.5)
                                if undead2.getY() >= 1000:
                                    if undead2.getX() <= 100:
                                        undead2.moveX(random.choice([50,100,150]))
                                    elif undead2.getX() >= 900:
                                        undead2.moveX(random.choice([-50,-100,-150]))
                                    else:
                                        undead2.moveX(random.choice([-100,-50,50,100]))
                                    undead2_moving_up = True
                            else:
                                undead2.moveY(-1)
                                if undead2.getY() == 699:
                                    undead2_moving_up = False
                        else:
                            atk_button = attacking_wizard()
                            disable_black_hole_button()
                            no_zombies()
                    
                    ################ Phase 2 ####################
                    else:
                        ############### Phase 3 at 20% hp ################
                        if current_enemy.return_hp() <= 0.2*wizard_max_hp:
                            skull_move = 1.25
                            #change the goblin's image and damage
                            wizard_attack_time = 0.5
                            delta = datetime.timedelta(seconds = 10000)
                            atk_button_move_speed = 1.5
                            phase3_fel_pools = True
                            
                        else:
                            skull_move = 0.8
                            delta = datetime.timedelta(seconds = 10)
                            wizard_attack_time = 5
                        ######## His hp and an attack buttons appear ##########
                        hp_text = bloody_font.render("Hp: " + str(current_enemy.return_hp()),True,colors.true_red,black)
                        screen.blit(hp_text,(450,550))
                        atk_button_max_x = 650
                        atk_button_min_x = 350
                        if atk_button_move: #moving right
                            if atk_button.getX() <= atk_button_max_x:
                                atk_button.moveX(atk_button_move_speed)
                            else:
                                atk_button_move = not atk_button_move
                        else:
                            if atk_button.getX() >= atk_button_min_x:
                                atk_button.moveX(-atk_button_move_speed)
                            else:
                                atk_button_move = not atk_button_move
                        if phase3_fel_pools:
                            move_atk_button = random.randrange(atk_button_move_chance)
                            if move_atk_button == 0:
                                new_loc = random.choice(atk_button_locations)
                                atk_button.setX(new_loc[0])
                                atk_button.setY(new_loc[1])
                        ############# Skull chases your curser and stuns you if it reaches ####################
                        enable_cursed_skull_button()
                        skull_x = cursed_skull_button.getX()
                        skull_y = cursed_skull_button.getY()
                        mouse_x1,mouse_y1 = pygame.mouse.get_pos()
                        if mouse_x1 < skull_x:
                            cursed_skull_button.moveX(-skull_move)
                            if mouse_y1 > skull_y:
                                cursed_skull_button.moveY(skull_move)
                            else:
                                cursed_skull_button.moveY(-skull_move)
                        else:
                            cursed_skull_button.moveX(skull_move)
                            if mouse_y1 > skull_y:
                                cursed_skull_button.moveY(skull_move)
                            else:
                                cursed_skull_button.moveY(-skull_move)
                        skull_distance = 0.8
                        if (skull_x >= mouse_x1 -skull_distance and skull_x <= mouse_x1 +skull_distance) and (skull_y >= mouse_y1 -skull_distance and skull_y <= mouse_y1 +skull_distance) and cursed_mouse== False:
                            cursed_mouse = True
                            start_time2 = datetime.datetime.now()
                        if cursed_mouse:
                            pygame.mouse.set_pos(skull_x,skull_y)
                            check_time2 = datetime.datetime.now()
                            if check_time2 >= start_time2 + datetime.timedelta(seconds = 2):
                                cursed_mouse = False
                                cursed_skull_button.setX(skull_x + 100)
                                cursed_skull_button.setY(skull_y + 100)
                        ######## Checking whether n seconds have passed ########
                        if time_flag == False:
                            start_time = datetime.datetime.now()
                            time_flag = True
                        else:
                            check_time = datetime.datetime.now()
                            if check_time >= start_time + delta:
                                time_flag = False
                                undead_rnd_kills = random.randrange(2,4)
                                undead_kills = 0
                                not_attacking_wizard()
            else:
                if current_hp <= 0:
                    dead()
                elif kill_count[kill_index] == 1:
                    enable_previous_button()
                    disable_cursed_skull_button()
                    if inventory[5] == 0:
                        enable_evil_ring_button()
                if goldsack_clicked_flag == False:
                    if goldsack_flag == True:
                        goldsack_flag = gold_sack(goldsack_flag) 
                else:
                    money_text.set_colorkey(black)
                    screen.blit(money_text, (450,400))

                not_attacking() 
def find_linear_func(x1,y1,x2,y2):
    delta_x = x1-x2
    if x1 == x2:
        return 0,0
    slope = (y1-y2)/delta_x
    b = y1-slope*x1
    return slope,b

def find_circle_function(center_x,center_y,x1,y1):
    radius = math.sqrt (math.pow(x1-center_x,2) + math.pow(y1-center_y,2))
    return radius

def find_y_give_x_circle(center_x,center_y,radius,x1):
    y1 = math.sqrt(math.pow(radius,2) - math.pow(x1-center_x,2)) + center_y
    return y1

def fight_goblins(image,image_rect):
    global current_enemy,current_hp,money,damage_dealt_flag,kill_index, goldsack_clicked_flag
    if current_sword != None and current_hp > 0:
        not_attacking_wizard()
        no_zombies()
        disable_arrow_buttons()
        disable_previous_button()
        disable_forward_button()
        disable_gold_sack_button()
        player_stats_button.disable()
        player_stats_button.hide()
        disable_inventory_not_menu()
        kill_index = 0
        hit_flag = False
        next_time = datetime.datetime.now()
        fighting = True
        dmg_appear_count = 0
        goblin = random.choice(goblins)
        current_enemy = copy.copy(goblin)
        money_text = font.render("+"+str(int(current_enemy.drop()/current_sword.return_level())),True,gold,black).convert()
        damage_dealt_flag = False
        y_i = 0
        start_dagger_x = 370
        start_dagger_y = 400
        if kill_count[kill_index] == 1:
            while(running):
                main_loop()
                screen.blit(image,image_rect)
                show_health()
                return
        else:
            attack_button_move_count_x = 0
            attack_button_move_count_y = 0
            attack_button = attack_button1
            attack_button.enable()
            attack_button.show()
            direction_x = random.choice([True,False])
            direction_y = random.choice([True,False])
            goblin1_sound.play()
            current_enemy.hp *= current_sword.return_level()
            current_enemy.power *= current_sword.return_level()
            while(running and fighting):
                screen.blit(image, image_rect)

                ########## Dagger attacking health animation ##########
                if hit_flag == True and current_hp > 0:
                    if start_dagger_y + y_i > 130 :
                        screen.blit(dagger_image,(start_dagger_x, start_dagger_y + y_i))
                        y_i -= 3
                    else:
                        y_i = 0
                        hit_flag = False
                        if current_enemy != None:
                            if current_shield != None:
                                if current_enemy.return_power() - current_shield.defence() > 0:
                                    current_hp -= current_enemy.return_power() - current_shield.defence()
                                else:
                                    current_hp -= 1
                            else:
                                current_hp -= current_enemy.return_power()

                show_health()

                if current_enemy != None and kill_count[kill_index] == 0 and current_hp > 0:
                    goldsack_clicked_flag = False

                    ########## All the visual assets ##########

                    hp_text = font.render("Hp: " + str(current_enemy.return_hp()),True,black,teal)
                    screen.blit(hp_text,(450,310))

                    goblin_image = remove_background(goblin.return_image_name(),goblin.return_bg_color())
                    screen.blit(goblin_image, (370,370))

                    ########## showing damage dealt ##########
                    if (damage_dealt_flag == True or damage_dealt >= current_enemy.return_hp()) and dmg_appear_count <50 :
                        dmg_text = font.render("-"+str(damage_dealt),True,red,black)
                        dmg_text.set_colorkey(black)
                        screen.blit(dmg_text,(500,370))
                        dmg_appear_count+=1
                    else:
                        dmg_appear_count = 0
                        damage_dealt_flag = False
                    ########## goblin attacks you every 1 seconds ##########
                    delta = datetime.timedelta(seconds = 1)
                    period = datetime.datetime.now()
                    if period >= next_time:
                        next_time += delta
                        hit_flag = True
                    #attack_i = random.randrange(1,6)
                    max_x = 700
                    min_x = 300
                    max_y = 700
                    min_y = 300
                    amount_to_move = 2
                    main_loop()

                    if attack_button.getX() > max_x:
                        attack_button.moveX(-amount_to_move)
                        direction_x = random.choice([True,False])
                    elif attack_button.getX() < min_x:
                        attack_button.moveX(+amount_to_move)
                        direction_x = random.choice([True,False])
                    elif attack_button_move_count_x >= 100:
                        direction_x = random.choice([True,False])
                        attack_button_move_count_x = 0
                    else:
                        if direction_x:
                            attack_button.moveX(+amount_to_move)
                            attack_button_move_count_x += 1
                        else:
                            attack_button.moveX(-amount_to_move)
                            attack_button_move_count_x += 1

                    if attack_button.getY()>max_y:
                        attack_button.moveY(-amount_to_move)
                        direction_y = random.choice([True,False])
                    elif attack_button.getY()<min_y:
                        attack_button.moveY(+amount_to_move)
                        direction_y = random.choice([True,False])
                    elif attack_button_move_count_y >= 100:
                        direction_y = random.choice([True,False])
                        attack_button_move_count_y = 0
                    else:
                        if  direction_y:
                            attack_button.moveY(+amount_to_move)
                            attack_button_move_count_y += 1
                        else:
                            attack_button.moveY(-amount_to_move)
                            attack_button_move_count_y += 1

                    if current_hp < 0:
                        current_hp = 0

                else:
                    if current_hp == 0:
                        dead()
                    elif kill_count[kill_index] >= 1:
                        enable_forward_button()
                        enable_previous_button()
                        enable_inventory_not_menu()
                        gold_sack_flag = True
                        while gold_sack_flag == True:
                            gold_sack_flag = gold_sack(gold_sack_flag)
                        money_text.set_colorkey(black)
                        screen.blit(money_text, (450,400))  
                    not_attacking()
                    return
                fighting_buttons()
                
def mushroom_clicked(button):
    global inventory
    inventory[1] += 1
    button.disable()
    button.hide()

def talk_to_fairy():
    global talked_to_fairy
    talked_to_fairy = True
    talk_to_fairy_button_disable()

def fairy_forest():
    global current_hp,talked_to_fairy
    random_mushroom()
    counter = 0
    healed_flag = False
    if talked_to_fairy == False:
        amount_to_heal = max_hp-current_hp
        while(True):
            screen.blit(fairy_forest_image,fairy_forest_rect)
            show_health()
            if healed_flag == False or counter < 1000:
                screen.blit(goblin_Fairy_image,(400,400))
                talk_to_fairy_button.enable()
                talk_to_fairy_button.show()
                if talked_to_fairy == True:
                    fairy_chat1 = small_font.render("Hrmpf.. you are lucky i was programmed to heal you",True,black,white)
                    fairy_chat2 = small_font.render("I wouldnt do it otherwise, i don't like you",True,black,white)
                    screen.blit(fairy_chat1,(300,400))
                    screen.blit(fairy_chat2,(300,440))
                    
                    healed_text = font.render("+ " + str(amount_to_heal),True,green,red).convert()
                    healed_text.set_colorkey(red)
                    current_hp = max_hp
                    screen.blit(healed_text,(450,150))
                    healed_flag = True
                    counter += 1

            else:
                talk_to_fairy_button_disable()
            not_attacking()
            main_loop()

def buy():
    global current_sword,max_hp,money, current_hp,current_shield
    bought_shield_flag = False
    bought_sword_flag = False
    if type(current_viewing_item)== Sword:
        if current_sword == None:
            if current_viewing_item.return_name() == "Iron Sword":
                if inventory[2] >= IRON_ORE_COST and money >= current_viewing_item.value():
                    inventory[2] -= IRON_ORE_COST
                    bought_sword_flag = True
            elif current_viewing_item.return_name() == "Gold Sword":
                if inventory[3] >= GOLD_ORE_COST and money >= current_viewing_item.value():
                    inventory[3] -= GOLD_ORE_COST
                    bought_sword_flag = True
            elif money >= current_viewing_item.value():
                bought_sword_flag = True

    elif type(current_viewing_item) == Shield:
        if current_shield == None:
            if current_viewing_item.return_name() == "Mushy Shield":
                if inventory[1] >= MUSHY_SHIELD_COST:
                    current_shield = copy.copy(current_viewing_item)
                    inventory[1] -= MUSHY_SHIELD_COST
                    bought_shield_flag = True

            elif money >= current_viewing_item.value():
                current_shield = copy.copy(current_viewing_item)
                money -= current_shield.value()
                bought_shield_flag = True

    if bought_sword_flag == True:
        current_sword = copy.copy(current_viewing_item)
        add_hp = 0
        if current_shield != None:
            add_hp = current_shield.hp()
        max_hp = BASE_HP + current_sword.hp() + add_hp
        money -= current_sword.value()
        current_hp = max_hp

    if bought_shield_flag == True:
        add_hp = 0
        if current_sword != None:
            add_hp = current_sword.hp()
        max_hp = BASE_HP + current_shield.hp() + add_hp
        current_hp = max_hp

def upgrade_sword():
    global money
    global current_sword
    if money < current_sword.return_level():
        print("cannot afford an upgrade \n")
    else:
        amount = current_sword.upgrade()
        if amount > 0:
            upgrade_sound.play()
        money -=current_sword.return_level()

def sell_window():
    global current_sword, current_shield, buying
    buying = True
    while (current_sword != None or current_shield != None) and buying == True:
        back_shop_button_enable()
        not_choosing_buy_or_sell_buttons()
        main_loop()
        screen.blit(shop_image, shop_image_rect)
        money_text = small_font.render("Money: " + str(money),False,gold,blue).convert()
        money_text.set_colorkey(blue)
        screen.blit(money_text,(420,350))
        screen.blit(money_image,(370,330))
        if current_sword != None:
            screen.blit(current_sword.return_image(),(100,200))
            name_text = small_font.render(current_sword.return_name(), True,current_sword.return_name_color(),blue)
            screen.blit(name_text,(100,450))
            sword_price_text = font.render("Price: " + str(current_sword.value()),True,white,blue)
            screen.blit(sword_price_text,(530,550))
            sell_sword_button_enable()
        else:
            sell_sword_button_disable()
        if current_shield != None:
            screen.blit(current_shield.return_image(),(700,200))
            shield_name_text = small_font.render(current_shield.return_name(), True,gold,blue)
            screen.blit(shield_name_text,(750,450))
            shield_price_text = font.render("Price: " + str(current_shield.value()),True,white,blue)
            screen.blit(shield_price_text,(730,450))
            sell_shield_button_enable()
        else:
            sell_shield_button_disable()
    screen.blit(shop_image, shop_image_rect)
    sell_sword_button_disable()
    sell_shield_button_disable()

def sell_sword():
    global money,current_sword,max_hp,current_hp
    money += current_sword.value()
    max_hp -= current_sword.hp()
    current_hp = max_hp
    current_sword = None
    if current_shield == None:
        shop_buy_sell_menu()

def sell_shield():
    global money,current_shield,max_hp,current_hp
    if current_shield.name != "Mushy Shield":
        money += current_shield.value()
    else:
        inventory[1] += MUSHY_SHIELD_COST
    max_hp -= current_shield.hp()
    current_hp = max_hp
    current_shield = None
    if current_sword == None:
        shop_buy_sell_menu()

def next_sword():
    global current_viewing_item_index,current_viewing_item_db
    if current_viewing_item_index < len(current_viewing_item_db) - 1:
        current_viewing_item_index += 1

def previous_sword():
    global current_viewing_item_index
    if current_viewing_item_index > 0:
        current_viewing_item_index -= 1

def upgrade_screen():
    global current_sword,in_upgrading_menu
    in_upgrading_menu = True
    if current_sword != None:
        global money
        exit_main_menu_to_upgrade_screen()
        while(in_upgrading_menu):
            main_loop()
            screen.blit(background_image, background_rect)
            screen.blit(current_sword.return_image(),(250,200))
            name_text = font.render(current_sword.return_name(), True,white,blue)
            screen.blit(name_text,(270,450))
            power_text = font.render("Power: " + str(current_sword.return_power()),True,white,blue)
            screen.blit(power_text,(530,300))
            level_text = font.render("level: " + str(current_sword.return_level()),True,white,blue)
            screen.blit(level_text,(530,250))
            price_text = font.render("Value: " + str(current_sword.value()),True,gold,blue)
            screen.blit(price_text,(530,450))
            money_text = font.render("Money:    " + str(money),False,gold,blue)
            screen.blit(money_text,(365,650))
            screen.blit(money_image,(482,647))
            if money < current_sword.level:
                money_color = red
            else:
                money_color = white
            cost_text = font.render("Cost:    "+ str(current_sword.level),True,money_color,blue)
            screen.blit(cost_text,(485,560))
            screen.blit(money_image,(567,557))
            events = pygame.event.get()
            pw.update(events)
            pygame.display.update()

def shopping_menu(menu_screen):
    global in_shop
    in_shop = True
    exit_main_menu_to_shop()
    while(in_shop):
        screen.blit(shop_image,(0,0))
        if menu_screen == 1:
            not_browsing_shop_items_buttons()
            choose_buy_or_sell_buttons()
            back_shop_button_disable()
            back_to_buy_sell_button_disable()
        elif menu_screen == 2:
            browsing_shop_items_buttons()
            not_choosing_buy_or_sell_buttons()
            back_to_buy_sell_button_enable()
        elif menu_screen == 3:
            screen.blit(shop_image, shop_image_rect)
            screen.blit(wooden_frame_image,(150,150))
            shopping()
            if item_type == None:
                break
            else:
                if item_type == "shield":
                    current_item = current_shield
                elif item_type == "sword":
                    current_item = current_sword

                current_viewing_item_db = item_db(item_type)
                current_viewing_item = current_viewing_item_db[current_viewing_item_index]
                screen.blit(current_viewing_item.return_image(),(240,250))
                name_text = font.render(current_viewing_item.return_name(), True,current_viewing_item.return_name_color(),None)
                screen.blit(name_text,(270,490))
                hp_text = font.render("+" + str(current_viewing_item.hp()) + " HP", True,black,None)
                screen.blit(hp_text,(500,400))
                money_text = font.render("Money:    " + str(money),True,white,brown)
                screen.blit(money_text,(380,650))
                screen.blit(money_image,(495,648))

                if current_viewing_item.type == "Shield":
                    if current_viewing_item.return_name() == "Mushy Shield":
                        token = mushroom_token
                        cost = MUSHY_SHIELD_COST
                        inventory_index = 1
                        screen.blit(token,(508,573))
                    elif current_viewing_item.return_name() == "Gold Shield":
                        token = gold_ore_token
                        cost = GOLD_SHIELD_COST
                        inventory_index = 3
                        screen.blit(token,(508,573))
                    if inventory[inventory_index] < cost:
                        price_text = small_font.render(str(cost),True,red,None)
                    if inventory[inventory_index] >= cost:
                        price_text = small_font.render(str(cost),True,white,None)
                    screen.blit(price_text,(550,583))
                elif current_viewing_item.type == "Sword":
                    if current_viewing_item.return_name() == "Iron Sword":
                        if inventory[2] < IRON_ORE_COST:
                            iron_price_text = small_font.render(str(IRON_ORE_COST),True,red,None)
                        else:
                            iron_price_text = small_font.render(str(IRON_ORE_COST),True,white,None)
                        text = iron_price_text
                        token = iron_ore_token
                        screen.blit(text,(550,583))
                        screen.blit(token,(508,573))
                    elif current_viewing_item.return_name() == "Gold Sword":
                        if inventory[3] < GOLD_ORE_COST:
                            gold_price_text = small_font.render(str(GOLD_ORE_COST),True,red,None)
                        else:
                            gold_price_text = small_font.render(str(GOLD_ORE_COST),True,white,None)
                        text = gold_price_text
                        token = gold_ore_token
                        screen.blit(text,(550,583))
                        screen.blit(token,(508,573))
                if (money < current_viewing_item.value() or current_item != None):
                    price_text = font.render("Price:    " + str(current_viewing_item.value()),True,red,None)
                    screen.blit(price_text,(420,540))
                    screen.blit(money_image,(510,537))
                else:      
                    price_text = font.render("Price:     " + str(current_viewing_item.value()),True,white,None)
                    screen.blit(price_text,(420,540))
                    screen.blit(money_image,(510,537))

                if(item_type == "sword"):
                    power_text = font.render("Power: " + str(current_viewing_item.return_power()),True,black,None)
                    screen.blit(power_text,(490,350))

                if item_type == "shield":
                    defence_text = font.render("Defence: +" + str(current_viewing_item.defence()),True,black,None)
                    screen.blit(defence_text,(460,350))
    screen.blit(shop_image, shop_image_rect)

def shop_buy_sell_menu():
    global inventory_open,in_buy_sell_menu
    in_buy_sell_menu = True
    inventory_open = False
    while in_buy_sell_menu:
        screen.blit(shop_image, shop_image_rect)
        main_loop()
        global buying
        buying = False
        exit_main_menu_to_shop()
        not_browsing_shop_items_buttons()
        choose_buy_or_sell_buttons()
        back_shop_button_disable()
        back_to_buy_sell_button_disable()


def shop_menu(shopping_flag = True):
    global buying,in_buy_sell_menu
    in_buy_sell_menu = False
    if shopping_flag:
        buying = True
    else:
        buying = False
    screen.blit(shop_image, shop_image_rect)
    main_loop()
    exit_main_menu_to_shop()
    browsing_shop_items_buttons()
    not_choosing_buy_or_sell_buttons()
    back_to_buy_sell_button_enable()

def shop(item_type = None):
    exit_main_menu_to_shop()
    not_in_menu()
    shopping()
    global current_viewing_item,current_viewing_item_db,current_viewing_item_index
    current_viewing_item_index = 0
    text = ""
    token = None
    cost = 0
    inventory_index = 0
    while(buying):
        main_loop()
        screen.blit(shop_image, shop_image_rect)
        screen.blit(wooden_frame_image,(150,150))
        if item_type == None:
            break
        else:
            if item_type == "shield":
                current_item = current_shield
            elif item_type == "sword":
                current_item = current_sword

            current_viewing_item_db = item_db(item_type)
            current_viewing_item = current_viewing_item_db[current_viewing_item_index]
            screen.blit(current_viewing_item.return_image(),(240,250))
            name_text = font.render(current_viewing_item.return_name(), True,current_viewing_item.return_name_color(),None)
            screen.blit(name_text,(270,490))
            hp_text = font.render("+" + str(current_viewing_item.hp()) + " HP", True,black,None)
            screen.blit(hp_text,(500,400))
            money_text = font.render("Money:    " + str(money),True,white,brown)
            screen.blit(money_text,(380,650))
            screen.blit(money_image,(495,648))

            if current_viewing_item.type == "Shield":
                if current_viewing_item.return_name() == "Mushy Shield":
                    token = mushroom_token
                    cost = MUSHY_SHIELD_COST
                    inventory_index = 1
                    screen.blit(token,(508,573))
                elif current_viewing_item.return_name() == "Gold Shield":
                    token = gold_ore_token
                    cost = GOLD_SHIELD_COST
                    inventory_index = 3
                    screen.blit(token,(508,573))
                if inventory[inventory_index] < cost:
                    price_text = small_font.render(str(cost),True,red,None)
                if inventory[inventory_index] >= cost:
                    price_text = small_font.render(str(cost),True,white,None)
                screen.blit(price_text,(550,583))
            elif current_viewing_item.type == "Sword":
                if current_viewing_item.return_name() == "Iron Sword":
                    if inventory[2] < IRON_ORE_COST:
                        iron_price_text = small_font.render(str(IRON_ORE_COST),True,red,None)
                    else:
                        iron_price_text = small_font.render(str(IRON_ORE_COST),True,white,None)
                    text = iron_price_text
                    token = iron_ore_token
                    screen.blit(text,(550,583))
                    screen.blit(token,(508,573))
                elif current_viewing_item.return_name() == "Gold Sword":
                    if inventory[3] < GOLD_ORE_COST:
                        gold_price_text = small_font.render(str(GOLD_ORE_COST),True,red,None)
                    else:
                        gold_price_text = small_font.render(str(GOLD_ORE_COST),True,white,None)
                    text = gold_price_text
                    token = gold_ore_token
                    screen.blit(text,(550,583))
                    screen.blit(token,(508,573))
            if (money < current_viewing_item.value() or current_item != None):
                price_text = font.render("Price:    " + str(current_viewing_item.value()),True,red,None)
                screen.blit(price_text,(420,540))
                screen.blit(money_image,(510,537))
            else:      
                price_text = font.render("Price:     " + str(current_viewing_item.value()),True,white,None)
                screen.blit(price_text,(420,540))
                screen.blit(money_image,(510,537))

            if(item_type == "sword"):
                power_text = font.render("Power: " + str(current_viewing_item.return_power()),True,black,None)
                screen.blit(power_text,(490,350))

            if item_type == "shield":
                defence_text = font.render("Defence: +" + str(current_viewing_item.defence()),True,black,None)
                screen.blit(defence_text,(460,350))
    screen.blit(shop_image, shop_image_rect)
    main_loop()
    shop_buy_sell_menu()

########################## Buttons ##########################
scroll_next_button = Button(
    screen, 650, 750, 100, 50, text='Next',
    fontSize=20, margin=20,
    inactiveColour = tan,
    hoverColour=(150,0,0),
    pressedColour=(0, 255, 0), radius=20,
    onClick = lambda: next_scroll())

finish_read_scroll = Button(
    screen, 450, 750, 100, 50, text='Ok',
    fontSize=20, margin=20,
    inactiveColour = tan,
    hoverColour=(150,0,0),
    pressedColour=(0, 255, 0), radius=20,
    onClick = lambda: finish_read()) 

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

exit_button = Button(
    screen, 900, 100, 100, 50, text='Exit',
    fontSize=20, margin=20,
    inactiveColour=gold,
    hoverColour=(150,0,0),
    pressedColour=orange, radius=20,
    onClick = lambda: quit())

shop_button = Button(
    screen, 20, 600, 150, 75, text='Shop',
    fontSize=30, margin=20,
    inactiveColour= tan,
    hoverColour=(150,0,0),
    pressedColour = orange, radius=20,
    onClick = lambda: shop_buy_sell_menu())

upgrade_button = Button(
    screen, 880, 600, 150, 75, text='Upgrade',
    fontSize=30, margin=20,
    inactiveColour=tan,
    hoverColour=(150,0,0),
    pressedColour=orange, radius=20,
    onClick = lambda: upgrade_screen())

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

fight_button = Button(
    screen, 450, 500, 150, 75, text='Adventure',
    fontSize=30, margin=20,
    inactiveColour= tan,
    hoverColour=(150,0,0),
    pressedColour = orange, radius=20,
    onClick = lambda: adventure())

save_button = Button(
    screen, 800, 100, 100, 50, text='Save',
    fontSize = 20, margin = 20,
    inactiveColour= gold,
    hoverColour=(150,0,0),
    pressedColour = orange, radius=20,
    onClick = lambda: savegame())

load_button = Button(
    screen, 150, 300, 300, 150, text='Load Game',
    fontSize=50, margin=20,
    inactiveColour= tan,
    hoverColour=(150,0,0),
    pressedColour = orange, radius=20,
    onClick = lambda: load())

new_game_button = Button(
    screen, 490, 300, 300, 150, text='New Game',
    fontSize=50, margin=20,
    inactiveColour= tan,
    hoverColour=(150,0,0),
    pressedColour = orange, radius=20,
    onClick = lambda: main_menu(True))

player_stats_button = Button(
    screen, 900, 800, 100, 50,
    fontSize = 20, margin = 20,
    inactiveColour= gold,
    image = inventory_image,
    hoverColour=(150,0,0),
    pressedColour = orange, radius=20,
    onClick = lambda: open_inventory(True))

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

heal_button = Button(
    screen, 650, 700, 150, 75, text='Heal',
    fontSize=30, margin=20,
    inactiveColour= nature_green,
    hoverColour = gold,
    pressedColour = green, radius=20,
    onClick = lambda: heal(False))

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
running = True
while running:
    new_game()


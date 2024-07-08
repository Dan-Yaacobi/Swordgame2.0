import random
import time
import math

levels_dic = {"Copper Sword":3,"Iron Sword":5,"Gold Sword":7,"Fire Sword":7, "Unicorn Sword": 10, "Living Sword":25}
ts = time.time()
random.seed(ts)

class Item():
    def __init__(self,name,type,name_color,image):
        self.name = name
        self.type = type
        self.name_color = name_color
        self.image = image

    def return_name(self):
        return getattr(self,'name')
    
    def return_image(self):
        return getattr(self,'image')
    
    def return_name_color(self):
        return getattr(self,'name_color')


class Shield(Item):
    def __init__(self,name,type,name_color,image,defence,hp,price):
        super().__init__(name,type,name_color,image)
        self.name = name
        self.type = type
        self.plus_defence = defence
        self.plus_hp = hp
        self.price = price
        self.image = image
        self.name_color = name_color

    def defence(self):
        return self.plus_defence
    def hp(self):
        return self.plus_hp
    
    def value(self):
        return self.price
    

class Sword(Item):
    def __init__(self,name,power,type,name_color,image):
        super().__init__(name,type,name_color,image)
        self.name = name
        self.power = power
        self.type = type

        self.image = image
        self.name_color = name_color

        self.level = levels_dic[self.name]
        self.start_power = power
        self.plus_hp = self.level*10

    def upgrade(self):
        power_upgrade = random.randrange(max(math.floor((self.level*self.start_power)/(self.power)),2))
        if self.power + power_upgrade >=0:
            self.power += power_upgrade
        return power_upgrade
        
    def value(self):
        x = self.power
        return math.ceil(x*math.log(x)) 

    def return_level(self):
        return self.level
    
    def return_power(self):
        return self.power
    
    def hp(self):
        return self.plus_hp
    
    def set_power(self,new_power):
        self.power = new_power


class Health_Potion(Item):
        def __init__(self,name,heal,type,name_color,image):
            super().__init__(name,type,name_color,image)
            self.name = name
            self.heal = heal
            self.type = type
            self.image = image
            self.name_color = name_color
    
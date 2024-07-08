import os
from sword import Sword
def loadgame():
    current_dir = os.path.dirname(__file__)
    with open(os.path.join(current_dir, "savefile.txt"),'r+') as savefile:
        list1 = savefile.readline()
        list2 = []
        i = 0
        while list1 != "":
            list2.append(list1.split())
            print(list2)
            list1 = savefile.readline()
            i += 1
        money_line = list2[0][1]
        current_hp_line = list2[1][1]
        max_hp_line = list2[1][2]
        sword_line = list2[2]
        if len(sword_line) == 2: #meaning current sword = none
            sword_line = None
            sword_power = 0
        else:
            sword_line = list2[2][1]+ " " + list2[2][2]
            sword_power = list2[2][3]
        shield_line = list2[3]
        if len(shield_line) == 2: # meaning shield = None
            shield_line = None
        else:
            shield_line = list2[3][1] + " " + list2[3][2]
        inventory_line = list2[4]
        inventory_line.pop(0)
    for i in range (len(inventory_line)):
        inventory_line[i] = int(inventory_line[i])
    return int(money_line),int(current_hp_line),int(max_hp_line),sword_line,int(sword_power),shield_line,inventory_line

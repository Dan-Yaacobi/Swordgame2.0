from sword import Sword
import os
def saving(money, current_hp,max_hp,current_sword,current_shield,inventory_list):
    saved_flag = False
    current_dir = os.path.dirname(__file__)
    money = int(money)
    with open(os.path.join(current_dir, "savefile.txt"),'w') as savefile:
        if current_sword != None and current_shield != None:
            stat_list = ["money: " + str(money) + "\n",
                "health: " + str(current_hp) + " " + str(max_hp) + "\n",
                "sword: " + current_sword.return_name() + " " + str(current_sword.return_power()) + "\n",
                "shield: " + str(current_shield.return_name()) + "\n",
                "inventory: "]
            saved_flag = True
        elif current_sword == None and saved_flag == False:
            stat_list = ["money: " + str(money) + "\n",
                         "health: " + str(current_hp) + " " + str(max_hp) + "\n",
                          "sword: " + str(None) + "\n",
                          "shield: " + str(current_shield) + "\n",
                          "inventory: "]
            saved_flag = True

        elif current_shield == None and saved_flag == False:
            stat_list = ["money: " + str(money) + "\n",
                         "health: " + str(current_hp) + " " + str(max_hp) + "\n",
                          "sword: " + current_sword.return_name() + " " + str(current_sword.return_power()) + "\n",
                          "shield: " + str(current_shield) + "\n",
                          "inventory: "]
            saved_flag = True
        for i in range(len(inventory_list)):
            stat_list.append(str(inventory_list[i]) + " ")
        savefile.writelines(stat_list)


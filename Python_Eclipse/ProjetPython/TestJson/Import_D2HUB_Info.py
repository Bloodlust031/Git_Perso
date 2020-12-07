# -*-coding:Latin-1 -*
'''
Created on 5 déc. 2020

@author: blood
'''

import os
import Configuration
import json

item_list = list()

def Import_from_ImportD2HUB():
    global item_list
    liste_lignes = list()
    item_list.clear()
    with open(Configuration.path_ImportD2HUB, 'r')as mon_fichier:
        liste_lignes = mon_fichier.readlines()
        for ligne in liste_lignes:
            item_list.append(get_item_dico(ligne))

def get_item_dico(Ligne_txt):
    current_item = dict()
    current_item.clear()
    ligne_split = Ligne_txt.split("|")
    current_item["Item_IMEI"] = ligne_split[0]
    if (len(ligne_split[1]) >= 1):
        current_item["Account_Name"] = ligne_split[1]
    if (len(ligne_split[2]) >= 1):
        current_item["Item_Type"] = ligne_split[2]
    if (len(ligne_split[3]) >= 1):
        current_item["Item_FW"] = ligne_split[3]
    if (len(ligne_split[4]) >= 1):
        current_item["VEH_Immat"] = ligne_split[4]
    if (len(ligne_split[5]) >= 1):
        current_item["VEH_Model"] = ligne_split[5]
    if (len(ligne_split[6]) >= 1):
        current_item["Account_Number"] = ligne_split[6]
    return current_item
    
def Import_from_ExportD2HUB():
    liste_lignes = list()

            
if __name__ == '__main__':
    Import_from_ImportD2HUB()
    with open('D:\Temp_JSON\INPUT_D2HUB/genericInfo.json', 'w') as json_file_result:
        json.dump(item_list, json_file_result)
    pass 
   
    pass
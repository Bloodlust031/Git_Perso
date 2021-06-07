# -*-coding:utf-8 -*
'''
Created on 5 juin 2021

@author: blood
'''

import Configuration
import csv
import json
import Boite_Outils
import os

stat_dico = dict()

@Boite_Outils.print_temps
def listdirectory(): 
    if (userchoice == 1):
        path = "D:\Temp_JSON\IMEI_SORTED"
    if (userchoice == 2):
        path = Configuration.Chemin_json_msg
    
    liste_fichier=[] 
    for root, dirs, files in os.walk(path): 
        for i in files:
            if i.endswith(".json"):
                liste_fichier.append(os.path.join(root, i))
    liste_fichier.sort()    #Les messages sont traités dans l'ordre chronologique.
    
    return liste_fichier


def init_Stat_directory():
    dico = dict()
    dico["nb_msg"] = 0
    dico["nb_Heartbeat"] = 0
    dico["nb_Journey"] = 0
    dico["nb_events"] = 0
    dico["KM"] = 0
    return dico


def Lect_one_json_file(nom_fic_msg):
    global stat_dico

    with open(nom_fic_msg) as json_file2:
        data = json.load(json_file2)
        st_IMEI = str(data['ime'])
        
        if st_IMEI not in stat_dico["Unitary"]:
            stat_dico["Unitary"][st_IMEI] = init_Stat_directory()
        stat_dico["Global"]["nb_msg"] += 1
        stat_dico["Unitary"][st_IMEI]["nb_msg"] += 1
        
        if (str(data['evt']) == "102"):
            stat_dico["Global"]["nb_Journey"] += 1
            stat_dico["Unitary"][st_IMEI]["nb_Journey"] += 1
            if "2010" in data['cnt']:
                stat_dico["Global"]["KM"] += int(data['cnt']["2010"])
                stat_dico["Unitary"][st_IMEI]["KM"] += int(data['cnt']["2010"])
                
        if (str(data['evt']) == "100"):
            if (str(data['eid']) == "2a"):
                stat_dico["Global"]["nb_Heartbeat"] += 1
                stat_dico["Unitary"][st_IMEI]["nb_Heartbeat"] += 1
            else:
                stat_dico["Global"]["nb_events"] += 1
                stat_dico["Unitary"][st_IMEI]["nb_events"] += 1
                
    
def add_D2Hub_infos():
    global stat_dico
    with open(Configuration.path_json_D2Hub_info_total) as json_file3:
        equipment_dico = json.load(json_file3)
        for st_IMEi in stat_dico["Unitary"]:
            if st_IMEi in equipment_dico:
                if "Account_Name" in equipment_dico[st_IMEi]:
                    stat_dico["Unitary"][st_IMEi]["Account_Name"] = equipment_dico[st_IMEi]["Account_Name"]
                if "VEH_Mark" in equipment_dico[st_IMEi]:
                    stat_dico["Unitary"][st_IMEi]["Model"] = equipment_dico[st_IMEi]["VEH_Mark"]
                    if "VEH_Model" in equipment_dico[st_IMEi]:
                        stat_dico["Unitary"][st_IMEi]["Model"] = stat_dico["Unitary"][st_IMEi]["Model"] + " " + equipment_dico[st_IMEi]["VEH_Model"]
                if "Service_Name" in equipment_dico[st_IMEi]:
                    stat_dico["Unitary"][st_IMEi]["Service_Name"] = equipment_dico[st_IMEi]["Service_Name"]
                
def Gen_stat_ByModel():
    global stat_dico
    for st_IMEI in stat_dico["Unitary"]:
        if "Model" in stat_dico["Unitary"][st_IMEI]:
            st_model = stat_dico["Unitary"][st_IMEI]["Model"]
            if st_model not in stat_dico["ByModel"]:
                stat_dico["ByModel"][st_model] = init_Stat_directory()
            stat_dico["ByModel"][st_model]["nb_msg"] += stat_dico["Unitary"][st_IMEI]["nb_msg"]
            stat_dico["ByModel"][st_model]["nb_Heartbeat"] += stat_dico["Unitary"][st_IMEI]["nb_Heartbeat"]
            stat_dico["ByModel"][st_model]["nb_Journey"] += stat_dico["Unitary"][st_IMEI]["nb_Journey"]
            stat_dico["ByModel"][st_model]["nb_events"] += stat_dico["Unitary"][st_IMEI]["nb_events"]
            stat_dico["ByModel"][st_model]["KM"] += stat_dico["Unitary"][st_IMEI]["KM"]


def Gen_stat_ByServ():
    global stat_dico
    for st_IMEI in stat_dico["Unitary"]:
        if "Service_Name" in stat_dico["Unitary"][st_IMEI]:
            st_serv = stat_dico["Unitary"][st_IMEI]["Service_Name"]
            if st_serv not in stat_dico["ByService"]:
                stat_dico["ByService"][st_serv] = init_Stat_directory()
            stat_dico["ByService"][st_serv]["nb_msg"] += stat_dico["Unitary"][st_IMEI]["nb_msg"]
            stat_dico["ByService"][st_serv]["nb_Heartbeat"] += stat_dico["Unitary"][st_IMEI]["nb_Heartbeat"]
            stat_dico["ByService"][st_serv]["nb_Journey"] += stat_dico["Unitary"][st_IMEI]["nb_Journey"]
            stat_dico["ByService"][st_serv]["nb_events"] += stat_dico["Unitary"][st_IMEI]["nb_events"]
            stat_dico["ByService"][st_serv]["KM"] += stat_dico["Unitary"][st_IMEI]["KM"]


@Boite_Outils.print_temps
def Analyse_Messages():
    global stat_dico
    print("définition de la liste de fichiers a analyser")
    liste_fichiers = listdirectory()
    
    nb_fic = 0
    nb_fic_total = str(len(liste_fichiers))
    print(nb_fic_total + " fichiers a analyser")
    
    stat_dico["Global"] = init_Stat_directory()
    stat_dico["Unitary"] = dict()
    stat_dico["ByModel"] = dict()
    stat_dico["ByService"] = dict()

    for nom_fic in liste_fichiers:
        Lect_one_json_file(nom_fic)
        nb_fic = nb_fic + 1
        if ((nb_fic % 10000) == 0):
            print(str(nb_fic) + " fichiers analysés sur " + nb_fic_total)
    print("Fin de lecture des messages")

    add_D2Hub_infos()
    Gen_stat_ByModel()
    Gen_stat_ByServ()
    
    sauvegarde()
    
    
def sauvegarde():
    print(stat_dico)
    with open(Configuration.path_sortie_Stat + "Stat_msg.json", 'w') as json_file_result:
        json.dump(stat_dico, json_file_result, indent=4)
    

def Menu():
    global userchoice
    retry = True
    while retry:
        print("Faites votre choix:")
        print("1 Analyse des messages depuis IMEI_SORTED")
        print("2 Analyse des messages depuis INPUT_Msg")
        txt_input = input()
        try:
            if ((txt_input[0] == "1") or (txt_input[0] == "2")):
                userchoice = int(txt_input[0])
                retry = False
                Analyse_Messages()
            else:
                print("Try again !")
        except:
            print("Try again !")  

if __name__ == '__main__':
    Menu()
    pass
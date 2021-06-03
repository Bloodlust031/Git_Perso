# -*-coding:utf-8 -*
'''
Created on 26 mai 2021

@author: blood
'''

import Configuration
import csv
import json
import Boite_Outils
import os

#------------Mettre la liste des PID � analyser ici:
PID_list = [0x5E, 0x83,0xA1]

liste_Mapping = ["983BA013801B8015CCDC804DFFC9814302040000000000000000000000000000","983BA017B019A015CCD200110000010129000000000000000000000000000000","9838A017B00BA001C8CF80CDFDE98B5FEF37F02C000000000000000000000000"]

dicoMapping = dict()
dico_result = dict()
strPID_list = list()    #equivalent à PID_list mais sous forme de chaine de caracteres pour faciliter l'impression
userchoice = 4

def listdirectory(path): 
    liste_fichier=[] 
    for root, dirs, files in os.walk(path): 
        for i in files:
            if i.endswith(".json"):
                liste_fichier.append(os.path.join(root, i))
    liste_fichier.sort()    #Les messages sont traités dans l'ordre chronologique.
    return liste_fichier


def Masque_OU(car_a, car_b):
    car_result = hex(int(car_a,16)|int(car_b,16)).lstrip("0x")
    if len(car_result) == 0:
        car_result = "0"
    return car_result


def Fusion_Mapping_PID(st_Mapping_old, st_Mapping_new):
    st_temp = ""
    if (len(st_Mapping_new) == 64):
        if (len(st_Mapping_old) != 64):
            st_temp = st_Mapping_new
        else:
            for i in range(0, len(st_Mapping_old)):
                st_temp = st_temp + Masque_OU(st_Mapping_old[i:i+1],st_Mapping_new[i:i+1])
    else:
        st_temp = st_Mapping_old
    return st_temp


def get_mapping_from_MappingList_log():
    global dicoMapping
    dicoMapping.clear
    with open(Configuration.path_sortie_PID + "allMappings.log", "r") as filin:
        ligne = filin.readline()
        while ligne != "":
            st_IMEI = ligne[0:15]
            st_Mapping = ligne[16:80]
            if (st_IMEI not in dicoMapping):
                dicoMapping[st_IMEI] = st_Mapping
            else:
                dicoMapping[st_IMEI] = Fusion_Mapping_PID(dicoMapping[st_IMEI], st_Mapping)
            ligne = filin.readline()


def set_IMEI_INFO():
    global dico_result
    with open(Configuration.path_json_D2Hub_info_total) as json_file3:
        equipment_dico = json.load(json_file3)
        for st_IMEI in equipment_dico:
            if equipment_dico[st_IMEI]["Item_communicating"] == True:
                dico_result[st_IMEI] = dict()
                dico_result[st_IMEI]["IMEI"] = st_IMEI
                if "Item_FW" in equipment_dico[st_IMEI]:
                    dico_result[st_IMEI]["Item_FW"] = equipment_dico[st_IMEI]["Item_FW"]
                if "Service_Name" in equipment_dico[st_IMEI]:
                    dico_result[st_IMEI]["Service_Name"] = equipment_dico[st_IMEI]["Service_Name"]
                if "VEH_Mark" in equipment_dico[st_IMEI]:
                    dico_result[st_IMEI]["VEH_Mark"] = equipment_dico[st_IMEI]["VEH_Mark"]
                if "VEH_Model" in equipment_dico[st_IMEI]:
                    dico_result[st_IMEI]["VEH_Model"] = equipment_dico[st_IMEI]["VEH_Model"]
                    if "VEH_Serie" in equipment_dico[st_IMEI]:
                        if equipment_dico[st_IMEI]["VEH_Serie"] is not None:
                            dico_result[st_IMEI]["VEH_Model"] = dico_result[st_IMEI]["VEH_Model"] + " " + equipment_dico[st_IMEI]["VEH_Serie"]
                if st_IMEI in dicoMapping:
                    dico_result[st_IMEI]["Mapping_PID"] = dicoMapping[st_IMEI]


def set_PID_Present():
    global dico_result
    global strPID_list
    
    #remplissage de strPID_list
    for i in range(0, len(PID_list)):
        st_PID = "PID_" + hex(PID_list[i]).lstrip("0x")
        strPID_list.append(st_PID)
            
    for st_IMEI in dico_result:
        if "Mapping_PID" in dico_result[st_IMEI]:
            for i in range(0, len(PID_list)):
                if Is_PID_present(dico_result[st_IMEI]["Mapping_PID"], PID_list[i]):
                    dico_result[st_IMEI][strPID_list[i]] = "Present"
                else:
                    dico_result[st_IMEI][strPID_list[i]] = "Absent"
                  

def Is_PID_present(st_Mapping, PID):
    if len(st_Mapping) == 64:
        digit = (PID-1) // 4
        masque = 1 << (3-((PID-1) % 4))
        
        st_digit = int(st_Mapping[digit:digit+1],16)
        if (st_digit & masque) == 0:
            return False
        else:
            return True
    else:
        return False
    

def sauvegarde():
    with open(Configuration.path_sortie_PID + "PID_list.json", 'w') as json_file_result:
        json.dump(dicoMapping, json_file_result, indent=4)
    with open(Configuration.path_sortie_PID + "PID_analysis.csv", 'w', newline='') as csvfile:
        fieldnames = ['IMEI', 'Item_FW',"Service_Name","VEH_Mark","VEH_Model", "Mapping_PID"]
        fieldnames.extend(strPID_list)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,extrasaction='ignore',delimiter=";")
        writer.writeheader()
        for st_IMEI in dico_result:
            writer.writerow(dico_result[st_IMEI])
    pass

def get_mapping_from_PID_list_json():
    global dicoMapping
    with open(Configuration.path_sortie_PID + "PID_list.json", 'r') as json_file_result:
        dicoMapping = json.load(json_file_result)


def get_mapping_from_json_files():
    global dicoMapping
    dicoMapping.clear()
    print("définition de la liste de fichiers a analyser")
    if (userchoice == 1):
        liste_fichiers = listdirectory("D:\Temp_JSON\IMEI_SORTED")
    if (userchoice == 2):
        liste_fichiers = listdirectory(Configuration.Chemin_json_msg)
    
    nb_fic = 0
    nb_fic_total = str(len(liste_fichiers))
    print(nb_fic_total + " fichiers a analyser")
    for nom_fic in liste_fichiers:
        get_mapping_from_one_json_file(nom_fic)
        nb_fic = nb_fic+1
        if ((nb_fic % 10000) == 0):
            print(str(nb_fic) + " fichiers analysés sur " + nb_fic_total)
    print("Fin de lecture des messages")


def get_mapping_from_one_json_file(nom_fic_msg):
    global dicoMapping
    st_temp =""
    
    with open(nom_fic_msg) as json_file2:
        data = json.load(json_file2)
        st_IMEI = str(data['ime'])
        st_Mapping = "0"
        if (str(data['evt']) == "102"):
            st_temp = data["bin"]
            pos = st_temp.find('DB0719002000')
            if pos>0:
                st_temp = st_temp[pos+12:]
                st_Mapping = st_temp[:64]
            if (st_IMEI not in dicoMapping):
                dicoMapping[st_IMEI] = st_Mapping
            else:
                dicoMapping[st_IMEI] = Fusion_Mapping_PID(dicoMapping[st_IMEI], st_Mapping)


@Boite_Outils.print_temps
def Analyse_PID():
    if (userchoice == 1)or(userchoice == 2):
        get_mapping_from_json_files()           #pour récupérer les mappings OBD depuis les messages json
    elif (userchoice == 3):
        get_mapping_from_PID_list_json()
    elif (userchoice == 4):
        get_mapping_from_MappingList_log()    #pour récupérer les mappings depuis l'extract "allMappings.log" à récupérer sur la VM
    
    
    set_IMEI_INFO()
    set_PID_Present()
    sauvegarde()


def Analyse_Mapping():
    liste_PID_Presents = list()
    liste_PID_Presents.clear()
    mapping_decomp = list()
    
    for unMapping in liste_Mapping:
        mapping_decomp.clear()
        mapping_decomp.append(unMapping)
        for i in range(1,256):
            if Is_PID_present(unMapping, i):
                mapping_decomp.append(hex(i))
        liste_PID_Presents.append(mapping_decomp)
    print(liste_PID_Presents)
    with open(Configuration.path_sortie_PID + "PID_mapping.json", 'w') as json_file_result:
        json.dump(liste_PID_Presents, json_file_result, indent=4)
    


def Menu():
    global userchoice
    retry = True
    while retry:
        print("Faites votre choix:")
        print("1 Analyse des messages depuis IMEI_SORTED")
        print("2 Analyse des messages depuis INPUT_Msg")
        print("3 Analyse des messages depuis le précédent PID_list.json")
        print("4 Analyse des messages depuis le allMappings.log")
        print("5 Analyse du MAPPING depuis un buffer")
        txt_input = input()
        try:
            if ((txt_input[0] == "1") or (txt_input[0] == "2") or (txt_input[0] == "3") or (txt_input[0] == "4")):
                userchoice = int(txt_input[0])
                retry = False
                Analyse_PID()
            elif (txt_input[0] == "5"):
                userchoice = 5
                Analyse_Mapping()
                retry = False
            else:
                print("Try again !")
        except:
            print("Try again !")        
    


if __name__ == '__main__':
    Menu()
    print ("Fini")
    pass
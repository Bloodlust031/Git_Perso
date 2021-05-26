'''
Created on 26 mai 2021

@author: blood
'''

import Configuration
import csv
import json
import Boite_Outils

dico83 = dict()
dico5E = dict()
dico_result = dict()

def set_liste_PID_83():
    global dico83
    dico83.clear
    nb_IMEI = 0
    
    with open("D:\Temp_JSON\PID_83_analysis.log", "r") as filin:
        ligne = filin.readline()
        while ligne != "":
            #print(ligne)
            st_IMEI = ligne[0:15]
            #print(st_IMEI)
            if (st_IMEI not in dico83):
                nb_IMEI += 1
                dico83[st_IMEI] = dict()
                dico83[st_IMEI]["IMEI"] = st_IMEI
            ligne = filin.readline()

def set_liste_PID_5E():
    global dico5E
    dico5E.clear
    nb_IMEI = 0
    
    with open("D:\Temp_JSON\PID_5E_analysis.log", "r") as filin:
        ligne = filin.readline()
        while ligne != "":
            #print(ligne)
            st_IMEI = ligne[0:15]
            #print(st_IMEI)
            if (st_IMEI not in dico5E):
                nb_IMEI += 1
                dico5E[st_IMEI] = dict()
                dico5E[st_IMEI]["IMEI"] = st_IMEI
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
                if st_IMEI in dico83:
                    dico_result[st_IMEI]["PID_83"] = "Present"
                else:
                    dico_result[st_IMEI]["PID_83"] = "Absent"
                if st_IMEI in dico5E:
                    dico_result[st_IMEI]["PID_5E"] = "Present"
                else:
                    dico_result[st_IMEI]["PID_5E"] = "Absent"
                

def sauvegarde():
    with open("D:\Temp_JSON\PID_analysis.csv", 'w', newline='') as csvfile:
        fieldnames = ['IMEI', 'Item_FW',"Service_Name","VEH_Mark","VEH_Model", "PID_83", "PID_5E"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,extrasaction='ignore',delimiter=";")
        writer.writeheader()
        for st_IMEI in dico_result:
            writer.writerow(dico_result[st_IMEI])
    pass

if __name__ == '__main__':
    set_liste_PID_83()
    set_liste_PID_5E()
    set_IMEI_INFO()
    sauvegarde()
    print ("Fini")
    pass
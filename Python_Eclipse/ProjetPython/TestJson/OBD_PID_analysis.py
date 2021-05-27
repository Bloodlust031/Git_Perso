'''
Created on 26 mai 2021

@author: blood
'''

import Configuration
import csv
import json
import Boite_Outils

#------------Mettre la liste des PID à analyser ici:
PID_list = [0x5E, 0x83]


dicoMapping = dict()
dico_result = dict()
strPID_list = list()



def Masque_OU(car_a, car_b):
    car_result = hex(int(car_a,16)|int(car_b,16)).lstrip("0x")
    if len(car_result) == 0:
        car_result = "0"
    return car_result


def Fusion_Mapping_PID(st_Mapping_old, st_Mapping_new):
    st_temp = ""
    for i in range(0, len(st_Mapping_old)):
        st_temp = st_temp + Masque_OU(st_Mapping_old[i:i+1],st_Mapping_new[i:i+1])
    return st_temp


def set_liste_Mapping():
    global dicoMapping
    dicoMapping.clear
    with open("D:\\Temp_JSON\\allMappings.log", "r") as filin:
        ligne = filin.readline()
        while ligne != "":
            st_IMEI = ligne[0:15]
            st_Mapping = ligne[16:80]
            if (st_IMEI not in dicoMapping):
                dicoMapping[st_IMEI] = dict()
                dicoMapping[st_IMEI]["IMEI"] = st_IMEI
                dicoMapping[st_IMEI]["Mapping_PID"] = st_Mapping
            else:
                dicoMapping[st_IMEI]["Mapping_PID"] = Fusion_Mapping_PID(dicoMapping[st_IMEI]["Mapping_PID"], st_Mapping)
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
                    dico_result[st_IMEI]["Mapping_PID"] = dicoMapping[st_IMEI]["Mapping_PID"]


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
    with open("D:\Temp_JSON\PID_analysis.csv", 'w', newline='') as csvfile:
        fieldnames = ['IMEI', 'Item_FW',"Service_Name","VEH_Mark","VEH_Model", "Mapping_PID"]
        fieldnames.extend(strPID_list)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,extrasaction='ignore',delimiter=";")
        writer.writeheader()
        for st_IMEI in dico_result:
            writer.writerow(dico_result[st_IMEI])
    pass


if __name__ == '__main__':
    set_liste_Mapping()
    set_IMEI_INFO()
    set_PID_Present()
    sauvegarde()
    print ("Fini")
    pass
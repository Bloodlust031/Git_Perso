# -*-coding:utf-8 -*
'''
Created on 30 janv. 2021

@author: blood
'''

import Configuration
import json
import Import_D2HUB_Info
import logging
import csv
#import os
#import sys



def gen_stat_by_account():
    current_account = dict()
    stat_account_dict = dict()
        
    with open(Configuration.path_json_D2Hub_account) as json_file2:
        account_dico = json.load(json_file2)
        
    stat_account_dict.clear()
    
    #préparation du dictionnaire résultat    
    current_account["uuid"] = "Global"
    current_account["name"] = "Global"
    current_account["nb_iCAN1"] = 0
    current_account["nb_iCAN2"] = 0
    current_account["nb_iCAN_Active"] = 0
    current_account["nb_iCAN1_Active"] = 0
    current_account["nb_iCAN2_Active"] = 0
    current_account["nb_iCAN_communicating"] = 0
    current_account["nb_iCAN1_communicating"] = 0
    current_account["nb_iCAN2_communicating"] = 0
    current_account["FW_list"] = dict()
    current_account["nb FW 2.6.x older"] = 0
    current_account["nb FW 2.7.x 2.8.x"] = 0
    current_account["nb FW 3.1.x 3.2.x"] = 0
    current_account["nb FW 3.3.x newer"] = 0
    stat_account_dict[current_account["uuid"]] = current_account.copy()
    for account_UUID in account_dico:
        if account_dico[account_UUID]["isMaster"] == True:
            current_account["uuid"] = account_UUID
            current_account["name"] = account_dico[account_UUID]["accountName"].replace("\u00e9","e")
            current_account["nb_iCAN1"] = 0
            current_account["nb_iCAN2"] = 0
            current_account["nb_iCAN_Active"] = 0
            current_account["nb_iCAN1_Active"] = 0
            current_account["nb_iCAN2_Active"] = 0
            current_account["nb_iCAN_communicating"] = 0
            current_account["nb_iCAN1_communicating"] = 0
            current_account["nb_iCAN2_communicating"] = 0
            current_account["FW_list"] = dict()
            current_account["nb FW 2.6.x older"] = 0
            current_account["nb FW 2.7.x 2.8.x"] = 0
            current_account["nb FW 3.1.x 3.2.x"] = 0
            current_account["nb FW 3.3.x newer"] = 0
            stat_account_dict[current_account["uuid"]] = current_account.copy()

    #parcours du tableau des équipements
    with open(Configuration.path_json_D2Hub_info_total) as json_file3:
        equipment_dico = json.load(json_file3)    
    for imei in equipment_dico:
        account_uuid = equipment_dico[imei]["Account_ID"]
        if account_dico[account_uuid]["isMaster"] == True:
            master_uuid = account_uuid
        else:    
            master_uuid = account_dico[account_uuid]["MastertUuid"]
        if (equipment_dico[imei]["Item_Type"] == "ICAN_V2"):
            stat_account_dict["Global"]["nb_iCAN2"] +=1
            stat_account_dict[master_uuid]["nb_iCAN2"] +=1
            if(equipment_dico[imei]["Item_active"] == True):
                stat_account_dict["Global"]["nb_iCAN_Active"] +=1
                stat_account_dict["Global"]["nb_iCAN2_Active"] +=1
                stat_account_dict[master_uuid]["nb_iCAN_Active"] +=1
                stat_account_dict[master_uuid]["nb_iCAN2_Active"] +=1
            if(equipment_dico[imei]["Item_communicating"] == True):
                stat_account_dict["Global"]["nb_iCAN_communicating"] +=1
                stat_account_dict["Global"]["nb_iCAN2_communicating"] +=1
                stat_account_dict[master_uuid]["nb_iCAN_communicating"] +=1
                stat_account_dict[master_uuid]["nb_iCAN2_communicating"] +=1
        else:
            stat_account_dict["Global"]["nb_iCAN1"] +=1
            stat_account_dict[master_uuid]["nb_iCAN1"] +=1
            if(equipment_dico[imei]["Item_active"] == True):
                stat_account_dict["Global"]["nb_iCAN_Active"] +=1
                stat_account_dict["Global"]["nb_iCAN1_Active"] +=1
                stat_account_dict[master_uuid]["nb_iCAN_Active"] +=1
                stat_account_dict[master_uuid]["nb_iCAN1_Active"] +=1
            if(equipment_dico[imei]["Item_communicating"] == True):
                stat_account_dict["Global"]["nb_iCAN_communicating"] +=1
                stat_account_dict["Global"]["nb_iCAN1_communicating"] +=1
                stat_account_dict[master_uuid]["nb_iCAN_communicating"] +=1
                stat_account_dict[master_uuid]["nb_iCAN1_communicating"] +=1
        if(equipment_dico[imei]["Item_active"] == True):    
            str_fw = equipment_dico[imei]["Item_FW"]
            if(str_fw not in stat_account_dict["Global"]["FW_list"]):
                stat_account_dict["Global"]["FW_list"][str_fw] = 1
            else:
                stat_account_dict["Global"]["FW_list"][str_fw] += 1
            if(str_fw not in stat_account_dict[master_uuid]["FW_list"]):
                stat_account_dict[master_uuid]["FW_list"][str_fw] = 1
            else:
                stat_account_dict[master_uuid]["FW_list"][str_fw] += 1
            if(str_fw < "2.7.0"):
                stat_account_dict["Global"]["nb FW 2.6.x older"] += 1
                stat_account_dict[master_uuid]["nb FW 2.6.x older"] += 1
            elif(str_fw < "3.0.0"):
                stat_account_dict["Global"]["nb FW 2.7.x 2.8.x"] += 1
                stat_account_dict[master_uuid]["nb FW 2.7.x 2.8.x"] += 1
            elif(str_fw < "3.3.0"):
                stat_account_dict["Global"]["nb FW 3.1.x 3.2.x"] += 1
                stat_account_dict[master_uuid]["nb FW 3.1.x 3.2.x"] += 1
            else:
                stat_account_dict["Global"]["nb FW 3.3.x newer"] += 1
                stat_account_dict[master_uuid]["nb FW 3.3.x newer"] += 1
                
    
    #suppression des comptes sans iCAN actives et/ou communicantes
    inactive_account = ""
    inactive_account_list = list()
    for account_UUID in stat_account_dict:
        if stat_account_dict[account_UUID]["nb_iCAN_Active"] == 0:
            if len(inactive_account) > 0:
                inactive_account = inactive_account + ", "
            inactive_account = inactive_account + stat_account_dict[account_UUID]["name"] + "(" + str(stat_account_dict[account_UUID]["nb_iCAN1"]) + "/" + str(stat_account_dict[account_UUID]["nb_iCAN2"]) + ")"
            inactive_account_list.append(account_UUID)
    for account_UUID in inactive_account_list:
        del stat_account_dict[account_UUID]
    if len(inactive_account) > 0:
        logging.info('Comptes sans iCAN actives (nb_iCAN1/nb_iCAN2): ' + inactive_account)
    
    #sauvegarde du résultat
    with open(Configuration.path_json_stat_by_account, 'w') as json_file_result:
        json.dump(stat_account_dict, json_file_result, indent=4)
    with open(Configuration.path_json_stat_by_account_csv, 'w', newline='') as csvfile:
        fieldnames = ['name', 'nb_iCAN1','nb_iCAN2', 'nb_iCAN_Active', 'nb_iCAN_communicating', 'nb FW 2.6.x older', 'nb FW 2.7.x 2.8.x', 'nb FW 3.1.x 3.2.x', 'nb FW 3.3.x newer', 'FW_list']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,extrasaction='ignore',delimiter=";")
        writer.writeheader()
        for account_UUID in stat_account_dict:
            writer.writerow(stat_account_dict[account_UUID])
    pass


def gen_stat_by_equipment():
    stat_dict = dict()
    stat_dict.clear()
    with open(Configuration.path_json_D2Hub_info_total) as json_file3:
        equipment_dico = json.load(json_file3)
        stat_dict["Item_active"] = dict()
        stat_dict["Item_communicating"] = dict()
        stat_dict["Item_active"]["FW_list"] = dict()
        stat_dict["Item_active"]["Service_list"] = dict()
        stat_dict["Item_communicating"]["FW_list"] = dict()
        stat_dict["Item_communicating"]["Service_list"] = dict()
        for imei in equipment_dico:
            if(equipment_dico[imei]["Item_active"] == True):
                str_fw = equipment_dico[imei]["Item_FW"]
                if(str_fw not in stat_dict["Item_active"]["FW_list"]):
                    stat_dict["Item_active"]["FW_list"][str_fw] = 1
                else:
                    stat_dict["Item_active"]["FW_list"][str_fw] += 1
                
                if("Service_Name" in equipment_dico[imei]):
                    str_tmp = equipment_dico[imei]["Service_Name"]
                    if(str_tmp not in stat_dict["Item_active"]["Service_list"]):
                        stat_dict["Item_active"]["Service_list"][str_tmp] = 1
                    else:
                        stat_dict["Item_active"]["Service_list"][str_tmp] += 1
            if(equipment_dico[imei]["Item_communicating"] == True):
                str_fw = equipment_dico[imei]["Item_FW"]
                if(str_fw not in stat_dict["Item_communicating"]["FW_list"]):
                    stat_dict["Item_communicating"]["FW_list"][str_fw] = 1
                else:
                    stat_dict["Item_communicating"]["FW_list"][str_fw] += 1
                
                if("Service_Name" in equipment_dico[imei]):
                    str_tmp = equipment_dico[imei]["Service_Name"]
                    if(str_tmp not in stat_dict["Item_communicating"]["Service_list"]):
                        stat_dict["Item_communicating"]["Service_list"][str_tmp] = 1
                    else:
                        stat_dict["Item_communicating"]["Service_list"][str_tmp] += 1


    with open(Configuration.path_json_Globalstat, 'w') as json_file_result:
        json.dump(stat_dict, json_file_result, indent=4)

def gen_stat_by_Veh(st_Model):
    stat_dict = dict()
    stat_dict.clear()
    
    with open(Configuration.path_json_D2Hub_info_total) as json_file3:
        equipment_dico = json.load(json_file3)
        stat_dict["Count"] = 0
        stat_dict["Item_active"] = dict()
        stat_dict["Item_active"]["Count"] = 0
        stat_dict["Item_communicating"] = dict()
        stat_dict["Item_communicating"]["Count"] = 0
        stat_dict["Item_active"]["FW_list"] = dict()
        stat_dict["Item_active"]["Service_list"] = dict()
        stat_dict["Item_communicating"]["FW_list"] = dict()
        stat_dict["Item_communicating"]["Service_list"] = dict()

        nom_fic = Configuration.path_sortie + "Stat_Veh_" + st_Model + ".json"
        stat_dict["Item_active"]["Serie"] = dict()
        stat_dict["Item_communicating"]["Serie"] = dict()
        
        for imei in equipment_dico:
            a_traiter = False
            if "VEH_Model" in equipment_dico[imei]:
                if(equipment_dico[imei]["VEH_Model"] == st_Model):
                    a_traiter = True
                        
            if a_traiter == True:
                stat_dict["Count"] += 1
                if(equipment_dico[imei]["Item_active"] == True):
                    stat_dict["Item_active"]["Count"] += 1
                    str_fw = equipment_dico[imei]["Item_FW"]
                    if(str_fw not in stat_dict["Item_active"]["FW_list"]):
                        stat_dict["Item_active"]["FW_list"][str_fw] = 1
                    else:
                        stat_dict["Item_active"]["FW_list"][str_fw] += 1
                    
                    if("Service_Name" in equipment_dico[imei]):
                        str_tmp = equipment_dico[imei]["Service_Name"]
                        if(str_tmp not in stat_dict["Item_active"]["Service_list"]):
                            stat_dict["Item_active"]["Service_list"][str_tmp] = 1
                        else:
                            stat_dict["Item_active"]["Service_list"][str_tmp] += 1
                    
                    st_VEH_Serie = equipment_dico[imei]["VEH_Serie"]
                    try:
                        if len(st_VEH_Serie) == 0:
                            st_VEH_Serie = "vide"
                    except:
                        st_VEH_Serie = "vide"
                    if(st_VEH_Serie not in stat_dict["Item_active"]["Serie"]):
                        stat_dict["Item_active"]["Serie"][st_VEH_Serie] = dict()
                        stat_dict["Item_active"]["Serie"][st_VEH_Serie]["Count"] = 0
                        stat_dict["Item_active"]["Serie"][st_VEH_Serie]["FW_list"] = dict()
                        stat_dict["Item_active"]["Serie"][st_VEH_Serie]["Service_list"] = dict()
                    
                    stat_dict["Item_active"]["Serie"][st_VEH_Serie]["Count"] += 1
                    if("Service_Name" in equipment_dico[imei]):
                        str_tmp = equipment_dico[imei]["Service_Name"]
                        if(str_tmp not in stat_dict["Item_active"]["Serie"][st_VEH_Serie]["Service_list"]):
                            stat_dict["Item_active"]["Serie"][st_VEH_Serie]["Service_list"][str_tmp] = 1
                        else:
                            stat_dict["Item_active"]["Serie"][st_VEH_Serie]["Service_list"][str_tmp] += 1
                    if(str_fw not in stat_dict["Item_active"]["Serie"][st_VEH_Serie]["FW_list"]):
                        stat_dict["Item_active"]["Serie"][st_VEH_Serie]["FW_list"][str_fw] = 1
                    else:
                        stat_dict["Item_active"]["Serie"][st_VEH_Serie]["FW_list"][str_fw] += 1
                            
                        
                if(equipment_dico[imei]["Item_communicating"] == True):
                    stat_dict["Item_communicating"]["Count"] += 1
                    str_fw = equipment_dico[imei]["Item_FW"]
                    if(str_fw not in stat_dict["Item_communicating"]["FW_list"]):
                        stat_dict["Item_communicating"]["FW_list"][str_fw] = 1
                    else:
                        stat_dict["Item_communicating"]["FW_list"][str_fw] += 1
                    
                    if("Service_Name" in equipment_dico[imei]):
                        str_tmp = equipment_dico[imei]["Service_Name"]
                        if(str_tmp not in stat_dict["Item_communicating"]["Service_list"]):
                            stat_dict["Item_communicating"]["Service_list"][str_tmp] = 1
                        else:
                            stat_dict["Item_communicating"]["Service_list"][str_tmp] += 1
                    st_VEH_Serie = equipment_dico[imei]["VEH_Serie"]
                    try:
                        if len(st_VEH_Serie) == 0:
                            st_VEH_Serie = "vide"
                    except:
                        st_VEH_Serie = "vide"
                    if(st_VEH_Serie not in stat_dict["Item_communicating"]["Serie"]):
                        stat_dict["Item_communicating"]["Serie"][st_VEH_Serie] = dict()
                        stat_dict["Item_communicating"]["Serie"][st_VEH_Serie]["Count"] = 0
                        stat_dict["Item_communicating"]["Serie"][st_VEH_Serie]["FW_list"] = dict()
                        stat_dict["Item_communicating"]["Serie"][st_VEH_Serie]["Service_list"] = dict()
                    
                    stat_dict["Item_communicating"]["Serie"][st_VEH_Serie]["Count"] += 1
                    if("Service_Name" in equipment_dico[imei]):
                        str_tmp = equipment_dico[imei]["Service_Name"]
                        if(str_tmp not in stat_dict["Item_communicating"]["Serie"][st_VEH_Serie]["Service_list"]):
                            stat_dict["Item_communicating"]["Serie"][st_VEH_Serie]["Service_list"][str_tmp] = 1
                        else:
                            stat_dict["Item_communicating"]["Serie"][st_VEH_Serie]["Service_list"][str_tmp] += 1
                    if(str_fw not in stat_dict["Item_communicating"]["Serie"][st_VEH_Serie]["FW_list"]):
                        stat_dict["Item_communicating"]["Serie"][st_VEH_Serie]["FW_list"][str_fw] = 1
                    else:
                        stat_dict["Item_communicating"]["Serie"][st_VEH_Serie]["FW_list"][str_fw] += 1
                        
    with open(nom_fic, 'w') as json_file_result:
        json.dump(stat_dict, json_file_result, indent=4)

def gen_stat_by_Service():
    stat_dict = dict()
    stat_dict.clear()
    
    with open(Configuration.path_json_D2Hub_info_total) as json_file3:
        equipment_dico = json.load(json_file3)
        stat_dict["Item_active"] = dict()
        stat_dict["Item_active"]["Count"] = 0
        stat_dict["Item_communicating"] = dict()
        stat_dict["Item_communicating"]["Count"] = 0
        stat_dict["Item_active"]["Veh_list"] = dict()
        stat_dict["Item_communicating"]["Veh_list"] = dict()

        nom_fic = Configuration.path_sortie + "Stat_Services.json"
        stat_dict["Item_active"]["Serie"] = dict()
        stat_dict["Item_communicating"]["Serie"] = dict()
        
        for imei in equipment_dico:
            if "Service_Name" in equipment_dico[imei]:
                str_serv = equipment_dico[imei]["Service_Name"]
                
                veh_ID = ""
                if "VEH_Mark" in equipment_dico[imei]:
                    veh_ID = veh_ID + equipment_dico[imei]["VEH_Mark"]
                veh_ID = veh_ID + " / "
                if "VEH_Model" in equipment_dico[imei]:
                    veh_ID = veh_ID + equipment_dico[imei]["VEH_Model"]
                veh_ID = veh_ID + " / "
                if "VEH_Serie" in equipment_dico[imei]:
                    try:
                        veh_ID = veh_ID + equipment_dico[imei]["VEH_Serie"]
                    except:
                        pass
                    
                if(equipment_dico[imei]["Item_active"] == True):
                    stat_dict["Item_active"]["Count"] += 1
                    if str_serv not in stat_dict["Item_active"]:
                        stat_dict["Item_active"][str_serv] = dict()
                        stat_dict["Item_active"][str_serv]["Count"] = 0
                        stat_dict["Item_active"][str_serv]["Veh_list"] = dict()
                    stat_dict["Item_active"][str_serv]["Count"] += 1
                    if (veh_ID not in stat_dict["Item_active"][str_serv]["Veh_list"]):
                        stat_dict["Item_active"][str_serv]["Veh_list"][veh_ID] = 1
                    else:
                        stat_dict["Item_active"][str_serv]["Veh_list"][veh_ID] += 1
                    #TODO
                if(equipment_dico[imei]["Item_communicating"] == True):
                    stat_dict["Item_communicating"]["Count"] += 1
                    if str_serv not in stat_dict["Item_communicating"]:
                        stat_dict["Item_communicating"][str_serv] = dict()
                        stat_dict["Item_communicating"][str_serv]["Count"] = 0
                        stat_dict["Item_communicating"][str_serv]["Veh_list"] = dict()
                    stat_dict["Item_communicating"][str_serv]["Count"] += 1
                    if (veh_ID not in stat_dict["Item_communicating"][str_serv]["Veh_list"]):
                        stat_dict["Item_communicating"][str_serv]["Veh_list"][veh_ID] = 1
                    else:
                        stat_dict["Item_communicating"][str_serv]["Veh_list"][veh_ID] += 1                    #TODO

    with open(nom_fic, 'w') as json_file_result:
        json.dump(stat_dict, json_file_result, indent=4)
    

def gen_stat():
    
    fh_Stat = logging.FileHandler(Configuration.path_json_log_stat, 'w')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh_Stat.setFormatter(formatter)
    fh_Stat.setLevel(logging.DEBUG)
    log = logging.getLogger()  # root logger 
    log.setLevel(logging.DEBUG)
    for hdlr in log.handlers[:]:  # remove all old handlers
        log.removeHandler(hdlr)
    log.addHandler(fh_Stat)      # set the new handler    
    
    logging.info('Début de generation des stats')
    
    bretour = False
    txt_input = input("Voulez-vous mettre à jour les données d'entrées (O pour oui) ?")
    try:
        if ((txt_input[0] == "O") or (txt_input[0] == "o")):
            bretour = True
    except:
        bretour = False
        
    if bretour == True:
        logging.info('MAJ des infos d entree depuis D2Hub/AWS')
        Import_D2HUB_Info.Extract_infos_from_D2Hub()
        fh_Stat = logging.FileHandler(Configuration.path_json_log_stat, 'a')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh_Stat.setFormatter(formatter)
        log = logging.getLogger()  # root logger
        log.setLevel(logging.DEBUG)
        for hdlr in log.handlers[:]:  # remove all old handlers
            log.removeHandler(hdlr)
        log.addHandler(fh_Stat)      # set the new handler    

    logging.info('gen_stat_by_account')
    gen_stat_by_account()

    logging.info('gen_stat_by_equipment')
    gen_stat_by_equipment()
    
    gen_stat_by_Veh("MASTER")
    gen_stat_by_Veh("DAILY")
    gen_stat_by_Veh("MAXITY")
    
    gen_stat_by_Service()
    
    logging.info('Fin de generation des stats')

if __name__ == '__main__':
    
    #sys.stdin.read(1);
    gen_stat()
    
    
    pass
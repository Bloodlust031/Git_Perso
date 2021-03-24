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
    stat_account_dict.clear()
    stat_account_dict["Active account"] = dict()
    stat_account_dict["Inactive account"] = dict()
        
    with open(Configuration.path_json_D2Hub_account) as json_file2:
        account_dico = json.load(json_file2)
    
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
    stat_account_dict["Active account"][current_account["uuid"]] = current_account.copy()
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
            stat_account_dict["Active account"][current_account["uuid"]] = current_account.copy()

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
            stat_account_dict["Active account"]["Global"]["nb_iCAN2"] +=1
            stat_account_dict["Active account"][master_uuid]["nb_iCAN2"] +=1
            if(equipment_dico[imei]["Item_active"] == True):
                stat_account_dict["Active account"]["Global"]["nb_iCAN_Active"] +=1
                stat_account_dict["Active account"]["Global"]["nb_iCAN2_Active"] +=1
                stat_account_dict["Active account"][master_uuid]["nb_iCAN_Active"] +=1
                stat_account_dict["Active account"][master_uuid]["nb_iCAN2_Active"] +=1
            if(equipment_dico[imei]["Item_communicating"] == True):
                stat_account_dict["Active account"]["Global"]["nb_iCAN_communicating"] +=1
                stat_account_dict["Active account"]["Global"]["nb_iCAN2_communicating"] +=1
                stat_account_dict["Active account"][master_uuid]["nb_iCAN_communicating"] +=1
                stat_account_dict["Active account"][master_uuid]["nb_iCAN2_communicating"] +=1
        else:
            stat_account_dict["Active account"]["Global"]["nb_iCAN1"] +=1
            stat_account_dict["Active account"][master_uuid]["nb_iCAN1"] +=1
            if(equipment_dico[imei]["Item_active"] == True):
                stat_account_dict["Active account"]["Global"]["nb_iCAN_Active"] +=1
                stat_account_dict["Active account"]["Global"]["nb_iCAN1_Active"] +=1
                stat_account_dict["Active account"][master_uuid]["nb_iCAN_Active"] +=1
                stat_account_dict["Active account"][master_uuid]["nb_iCAN1_Active"] +=1
            if(equipment_dico[imei]["Item_communicating"] == True):
                stat_account_dict["Active account"]["Global"]["nb_iCAN_communicating"] +=1
                stat_account_dict["Active account"]["Global"]["nb_iCAN1_communicating"] +=1
                stat_account_dict["Active account"][master_uuid]["nb_iCAN_communicating"] +=1
                stat_account_dict["Active account"][master_uuid]["nb_iCAN1_communicating"] +=1
        if(equipment_dico[imei]["Item_active"] == True):    
            str_fw = equipment_dico[imei]["Item_FW"]
            if(str_fw not in stat_account_dict["Active account"]["Global"]["FW_list"]):
                stat_account_dict["Active account"]["Global"]["FW_list"][str_fw] = 1
            else:
                stat_account_dict["Active account"]["Global"]["FW_list"][str_fw] += 1
            if(str_fw not in stat_account_dict["Active account"][master_uuid]["FW_list"]):
                stat_account_dict["Active account"][master_uuid]["FW_list"][str_fw] = 1
            else:
                stat_account_dict["Active account"][master_uuid]["FW_list"][str_fw] += 1
            if(str_fw < "2.7.0"):
                stat_account_dict["Active account"]["Global"]["nb FW 2.6.x older"] += 1
                stat_account_dict["Active account"][master_uuid]["nb FW 2.6.x older"] += 1
            elif(str_fw < "3.0.0"):
                stat_account_dict["Active account"]["Global"]["nb FW 2.7.x 2.8.x"] += 1
                stat_account_dict["Active account"][master_uuid]["nb FW 2.7.x 2.8.x"] += 1
            elif(str_fw < "3.3.0"):
                stat_account_dict["Active account"]["Global"]["nb FW 3.1.x 3.2.x"] += 1
                stat_account_dict["Active account"][master_uuid]["nb FW 3.1.x 3.2.x"] += 1
            else:
                stat_account_dict["Active account"]["Global"]["nb FW 3.3.x newer"] += 1
                stat_account_dict["Active account"][master_uuid]["nb FW 3.3.x newer"] += 1
                
    with open(Configuration.path_sortie_Stat + "Stat_By_Account.csv", 'w', newline='') as csvfile:
        fieldnames = ['name', 'nb_iCAN1','nb_iCAN2', 'nb_iCAN_Active', 'nb_iCAN_communicating', 'nb FW 2.6.x older', 'nb FW 2.7.x 2.8.x', 'nb FW 3.1.x 3.2.x', 'nb FW 3.3.x newer', 'FW_list']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,extrasaction='ignore',delimiter=";")
        writer.writeheader()
        for account_UUID in stat_account_dict["Active account"]:
            writer.writerow(stat_account_dict["Active account"][account_UUID])
    pass
    
    #suppression des comptes sans iCAN actives et/ou communicantes
    inactive_account = ""
    inactive_account_list = list()
    for account_UUID in stat_account_dict["Active account"]:
        if stat_account_dict["Active account"][account_UUID]["nb_iCAN_Active"] == 0:
            stat_account_dict["Inactive account"][account_UUID] = dict()
            stat_account_dict["Inactive account"][account_UUID]["uuid"] = stat_account_dict["Active account"][account_UUID]["uuid"]
            stat_account_dict["Inactive account"][account_UUID]["name"] = stat_account_dict["Active account"][account_UUID]["name"]
            stat_account_dict["Inactive account"][account_UUID]["nb_iCAN1"] = stat_account_dict["Active account"][account_UUID]["nb_iCAN1"]
            stat_account_dict["Inactive account"][account_UUID]["nb_iCAN2"] = stat_account_dict["Active account"][account_UUID]["nb_iCAN2"]
            
            if len(inactive_account) > 0:
                inactive_account = inactive_account + ", "
            inactive_account = inactive_account + stat_account_dict["Active account"][account_UUID]["name"] + "(" + str(stat_account_dict["Active account"][account_UUID]["nb_iCAN1"]) + "/" + str(stat_account_dict["Active account"][account_UUID]["nb_iCAN2"]) + ")"
            inactive_account_list.append(account_UUID)
    for account_UUID in inactive_account_list:
        del stat_account_dict["Active account"][account_UUID]
    if len(inactive_account) > 0:
        logging.info('Comptes sans iCAN actives (nb_iCAN1/nb_iCAN2): ' + inactive_account)
    
    #sauvegarde du résultat
    with open(Configuration.path_sortie_Stat + "Stat_By_Account.json", 'w') as json_file_result:
        json.dump(stat_account_dict, json_file_result, indent=4)


def gen_stat_globales():
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


    with open(Configuration.path_sortie_Stat + "GlobalStat.json", 'w') as json_file_result:
        json.dump(stat_dict, json_file_result, indent=4)


def add_dict_stat_by_Veh(stat_dico, equipement_dico):
    stat_dico["Count"] += 1
    str_fw = equipement_dico["Item_FW"]
    if(str_fw not in stat_dico["FW_list"]):
        stat_dico["FW_list"][str_fw] = 1
    else:
        stat_dico["FW_list"][str_fw] += 1
    
    if("Service_Name" in equipement_dico):
        str_tmp = equipement_dico["Service_Name"]
        if(str_tmp not in stat_dico["Service_list"]):
            stat_dico["Service_list"][str_tmp] = 1
        else:
            stat_dico["Service_list"][str_tmp] += 1
    
    st_VEH_Serie = equipement_dico["VEH_Serie"]
    try:
        if len(st_VEH_Serie) == 0:
            st_VEH_Serie = "vide"
    except:
        st_VEH_Serie = "vide"
    if(st_VEH_Serie not in stat_dico["Serie"]):
        stat_dico["Serie"][st_VEH_Serie] = dict()
        stat_dico["Serie"][st_VEH_Serie]["Count"] = 0
        stat_dico["Serie"][st_VEH_Serie]["FW_list"] = dict()
        stat_dico["Serie"][st_VEH_Serie]["Service_list"] = dict()
        stat_dico["Serie"][st_VEH_Serie]["Motor_list"] = dict()
    
    stat_dico["Serie"][st_VEH_Serie]["Count"] += 1
    if("Service_Name" in equipement_dico):
        str_tmp = equipement_dico["Service_Name"]
        if(str_tmp not in stat_dico["Serie"][st_VEH_Serie]["Service_list"]):
            stat_dico["Serie"][st_VEH_Serie]["Service_list"][str_tmp] = 1
        else:
            stat_dico["Serie"][st_VEH_Serie]["Service_list"][str_tmp] += 1
    if(str_fw not in stat_dico["Serie"][st_VEH_Serie]["FW_list"]):
        stat_dico["Serie"][st_VEH_Serie]["FW_list"][str_fw] = 1
    else:
        stat_dico["Serie"][st_VEH_Serie]["FW_list"][str_fw] += 1
    
    st_motor = ""
    if("VEH_Motor_FuelType" in equipement_dico):
        st_motor += equipement_dico["VEH_Motor_FuelType"]
    else:
        st_motor += "-"
    st_motor += " / "
    if("VEH_Motor_NbCyl" in equipement_dico):
        st_motor += equipement_dico["VEH_Motor_NbCyl"]
    else:
        st_motor += "-"
    st_motor += " / "
    if("VEH_Motor_Cyl" in equipement_dico):
        st_motor += equipement_dico["VEH_Motor_Cyl"]
    else:
        st_motor += "-"
    if(st_motor not in stat_dico["Serie"][st_VEH_Serie]["Motor_list"]):
        stat_dico["Serie"][st_VEH_Serie]["Motor_list"][st_motor] = 1
    else:
        stat_dico["Serie"][st_VEH_Serie]["Motor_list"][st_motor] += 1
    
    
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

        nom_fic = Configuration.path_sortie_Stat + "Stat_Veh_" + st_Model + ".json"
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
                    add_dict_stat_by_Veh(stat_dict["Item_active"], equipment_dico[imei])
                if(equipment_dico[imei]["Item_communicating"] == True):
                    add_dict_stat_by_Veh(stat_dict["Item_communicating"], equipment_dico[imei])
                        
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

        nom_fic = Configuration.path_sortie_Stat + "Stat_Services.json"
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
                        stat_dict["Item_active"][str_serv]["FW_list"] = dict()
                    stat_dict["Item_active"][str_serv]["Count"] += 1
                    if (veh_ID not in stat_dict["Item_active"][str_serv]["Veh_list"]):
                        stat_dict["Item_active"][str_serv]["Veh_list"][veh_ID] = 1
                    else:
                        stat_dict["Item_active"][str_serv]["Veh_list"][veh_ID] += 1
                        
                    str_fw = equipment_dico[imei]["Item_FW"]
                    if(str_fw not in stat_dict["Item_active"][str_serv]["FW_list"]):
                        stat_dict["Item_active"][str_serv]["FW_list"][str_fw] = 1
                    else:
                        stat_dict["Item_active"][str_serv]["FW_list"][str_fw] += 1
                                                
                if(equipment_dico[imei]["Item_communicating"] == True):
                    stat_dict["Item_communicating"]["Count"] += 1
                    if str_serv not in stat_dict["Item_communicating"]:
                        stat_dict["Item_communicating"][str_serv] = dict()
                        stat_dict["Item_communicating"][str_serv]["Count"] = 0
                        stat_dict["Item_communicating"][str_serv]["Veh_list"] = dict()
                        stat_dict["Item_communicating"][str_serv]["FW_list"] = dict()
                    stat_dict["Item_communicating"][str_serv]["Count"] += 1
                    if (veh_ID not in stat_dict["Item_communicating"][str_serv]["Veh_list"]):
                        stat_dict["Item_communicating"][str_serv]["Veh_list"][veh_ID] = 1
                    else:
                        stat_dict["Item_communicating"][str_serv]["Veh_list"][veh_ID] += 1
                    str_fw = equipment_dico[imei]["Item_FW"]
                    if(str_fw not in stat_dict["Item_communicating"][str_serv]["FW_list"]):
                        stat_dict["Item_communicating"][str_serv]["FW_list"][str_fw] = 1
                    else:
                        stat_dict["Item_communicating"][str_serv]["FW_list"][str_fw] += 1                        

    with open(nom_fic, 'w') as json_file_result:
        json.dump(stat_dict, json_file_result, indent=4)


def gen_stat():
    
    fh_Stat = logging.FileHandler(Configuration.path_sortie_Stat + "Log_Stat.log", 'w')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh_Stat.setFormatter(formatter)
    fh_Stat.setLevel(logging.DEBUG)
    log = logging.getLogger()  # root logger 
    log.setLevel(logging.DEBUG)
    for hdlr in log.handlers[:]:  # remove all old handlers
        log.removeHandler(hdlr)
    log.addHandler(fh_Stat)      # set the new handler    
    
    
    logging.info('Lecture de Config.ini')
    Configuration.init_config()
    logging.info('D2Hub API username: ' + Configuration.API_D2HUB_USER)
    
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
        fh_Stat = logging.FileHandler(Configuration.path_sortie_Stat + "Log_Stat.log", 'a')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh_Stat.setFormatter(formatter)
        log = logging.getLogger()  # root logger
        log.setLevel(logging.DEBUG)
        for hdlr in log.handlers[:]:  # remove all old handlers
            log.removeHandler(hdlr)
        log.addHandler(fh_Stat)      # set the new handler    

    logging.info('gen_stat_by_account')
    gen_stat_by_account()

    logging.info('gen_stat_globales')
    gen_stat_globales()
    
    gen_stat_by_Veh("MASTER")
    gen_stat_by_Veh("DAILY")
    #gen_stat_by_Veh("MAXITY")
    #gen_stat_by_Veh("CLIO")
    #gen_stat_by_Veh("RANGER")
    
    gen_stat_by_Service()
    
    logging.info('Fin de generation des stats')

if __name__ == '__main__':
    
    #sys.stdin.read(1);
    gen_stat()
    print("Fini")
    
    
    pass
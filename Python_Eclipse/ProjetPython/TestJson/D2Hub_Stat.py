# -*-coding:utf-8 -*
'''
Created on 30 janv. 2021

@author: blood
'''

import Configuration
import json
import Import_D2HUB_Info
import logging


account_dico = dict()
stat_account_dict = dict()

def gen_stat_by_account():
    account_dico = dict()
    equipment_dico = dict()
    current_account = dict()
    
    with open(Configuration.path_json_D2Hub_account) as json_file2:
        account_dico = json.load(json_file2)
        
    stat_account_dict.clear()
    
    #préparation du dictionnaire résultat    
    current_account["uuid"] = "Global"
    current_account["name"] = "Global"
    current_account["nb_iCAN1"] = 0
    current_account["nb_iCAN2"] = 0
    current_account["nb_iCAN1_Active"] = 0
    current_account["nb_iCAN2_Active"] = 0
    current_account["nb_iCAN1_communicating"] = 0
    current_account["nb_iCAN2_communicating"] = 0
    current_account["FW_list"] = dict()
    stat_account_dict[current_account["uuid"]] = current_account.copy()
    for account_UUID in account_dico:
        if account_dico[account_UUID]["isMaster"] == True:
            current_account["uuid"] = account_UUID
            current_account["name"] = account_dico[account_UUID]["accountName"].replace("\u00e9","e")
            current_account["nb_iCAN1"] = 0
            current_account["nb_iCAN2"] = 0
            current_account["nb_iCAN1_Active"] = 0
            current_account["nb_iCAN2_Active"] = 0
            current_account["nb_iCAN1_communicating"] = 0
            current_account["nb_iCAN2_communicating"] = 0
            current_account["FW_list"] = dict()
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
                stat_account_dict["Global"]["nb_iCAN2_Active"] +=1
                stat_account_dict[master_uuid]["nb_iCAN2_Active"] +=1
            if(equipment_dico[imei]["Item_communicating"] == True):
                stat_account_dict["Global"]["nb_iCAN2_communicating"] +=1
                stat_account_dict[master_uuid]["nb_iCAN2_communicating"] +=1
        else:
            stat_account_dict["Global"]["nb_iCAN1"] +=1
            stat_account_dict[master_uuid]["nb_iCAN1"] +=1
            if(equipment_dico[imei]["Item_active"] == True):
                stat_account_dict["Global"]["nb_iCAN1_Active"] +=1
                stat_account_dict[master_uuid]["nb_iCAN1_Active"] +=1
            if(equipment_dico[imei]["Item_communicating"] == True):
                stat_account_dict["Global"]["nb_iCAN1_communicating"] +=1
                stat_account_dict[master_uuid]["nb_iCAN1_communicating"] +=1
        if((equipment_dico[imei]["Item_communicating"] == True) or (equipment_dico[imei]["Item_active"] == True)):    
            str_fw = equipment_dico[imei]["Item_FW"]
            if(str_fw not in stat_account_dict["Global"]["FW_list"]):
                stat_account_dict["Global"]["FW_list"][str_fw] = 1
            else:
                stat_account_dict["Global"]["FW_list"][str_fw] += 1
            if(str_fw not in stat_account_dict[master_uuid]["FW_list"]):
                stat_account_dict[master_uuid]["FW_list"][str_fw] = 1
            else:
                stat_account_dict[master_uuid]["FW_list"][str_fw] += 1
    
    #suppression des comptes sans iCAN actives et/ou communicantes
    inactive_account = ""
    inactive_account_list = list()
    for account_UUID in stat_account_dict:
        nb_ican = stat_account_dict[account_UUID]["nb_iCAN1_Active"] + stat_account_dict[account_UUID]["nb_iCAN2_Active"] + stat_account_dict[account_UUID]["nb_iCAN1_communicating"] + stat_account_dict[account_UUID]["nb_iCAN2_communicating"]
        if nb_ican == 0:
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


def gen_stat():
    '''logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh_Stat = logging.FileHandler(filename=Configuration.path_json_log_stat)
    fh_Stat.setLevel(logging.DEBUG)
    fh_Stat.setFormatter(formatter)    
    logger.addHandler(fh_Stat)'''
    logging.shutdown()
    logging.basicConfig(filename=Configuration.path_json_log_stat, filemode='w', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
    logging.info('Début de generation des stats')
    
    bretour = False
    txt_input = input("Voulez-vous mettre à jour les données d'entrées (O pour oui) ?")
    try:
        if ((txt_input[0] == "O") or (txt_input[0] == "o")):
            bretour = True
    except:
        bretour = False
        
    #if os.path.exists(Configuration.path_json_log_stat):
    #    os.remove(Configuration.path_json_log_stat)

    if bretour == True:
        
        logging.info('MAJ des infos d entree depuis D2Hub/AWS')
        #logging.shutdown()
        Import_D2HUB_Info.Extract_infos_from_D2Hub()
        #logging.shutdown()
        #logging.basicConfig(filename=Configuration.path_json_log_stat, filemode='a', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
        #logging.config.fileConfig(Configuration.path_json_log_stat)

    #logging.basicConfig(filename=Configuration.path_json_log_stat, filemode='a', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
    logging.info('gen_stat_by_account')
    gen_stat_by_account()

    
    
    logging.info('Fin de generation des stats')

if __name__ == '__main__':
    #mise � jour des informations depuis D2Hub
    #Import_D2HUB_Info.Extract_infos_from_D2hHub()
    #Import_D2HUB_Info.Get_D2Hub_Account_list()
    
    gen_stat()
    
    
    pass
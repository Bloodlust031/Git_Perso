# -*-coding:utf-8 -*
'''
Created on 5 dï¿½c. 2020

@author: blood
'''

import os
import Configuration
import json
import csv
import requests

item_list_1 = list()    #liste d'ï¿½quipement issus de "genericInfo.txt" sous forme de liste
item_list_2 = list()    #liste d'ï¿½quipement issus de "export.csv" sous forme de liste
item_dico = dict()      #liste d'ï¿½quipement issus de "genericInfo.txt" et de "export.csv" sous forme de dictionnaire (avec l'IMEI pour identifiant principal)
date_fic1 = 0
date_fic2 = 0

def Get_Info_Directly_from_D2Hub():
    to_continue = True
    cmd_number = 0
    current_item = dict()
    #Commande à répéter autant de fois que possible:
    #curl -X GET "https://admin.d2hub.fr/api/admin/v2/integration/device.search?page=0" -H "X-Api-Token: eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJqZGV2YXkiLCJhdXRoIjoiUk9MRV9BRE1JTiIsImV4cCI6MTYxMzE5Nzc5NX0.EXEQxe8_bm2G_hatGCKoX1ZnqqPypHybqGf8v0MlkhSSS13uwMzs5fJg_u7O5xFJJDn-bsVNx2L2bu4m0KoUzA" -H "Accept: application/json" -H "Content-Type: application/json"
    
    while to_continue:
        try:
            #envoi de la commande CURL

            #analyse du résultat            
            
            #incrémentation du compteur de page
            cmd_number += 1
        except:
            to_continue = False
            
    

def Telech_D2HUb_Info_from_AWS():
    cmd_list = list()
    commande = "start aws s3 sync s3://exchange.d2hub.fr/checkers/ " + Configuration.path_InputD2HUB    #cette requete donne des résultats obsolettes
    #cmd_list.append(commande)
    commande = "start aws s3 sync s3://exchange.d2hub.fr/iCANGeneralInfo/ " + Configuration.path_InputD2HUB
    cmd_list.append(commande)
    nb_req = len(cmd_list)
    i = 0
    for str_cmd in cmd_list:
        i+=1
        os.system(str_cmd)
        print ("Commande " + str(i) + " / " + str(nb_req))
    print("Téléchargement en cours")
    os.system("pause") # On met le programme en pause pour Ã©viter qu'il ne se referme (Windows)
    
    
def Import_from_ImportD2HUB():
    global item_list_1
    global date_fic1
    liste_lignes = list()
    date_fic1 = os.path.getmtime(Configuration.path_ImportD2HUB)
    with open(Configuration.path_ImportD2HUB, 'r')as mon_fichier:
        liste_lignes = mon_fichier.readlines()
        for ligne in liste_lignes:
            item_list_1.append(get_item_dico(ligne))

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
        current_item["VEH_MarkModel"] = ligne_split[5]
    if (len(ligne_split[6]) >= 1):
        current_item["Account_ID"] = ligne_split[6]
    if (len(ligne_split[7]) >= 1):
        current_item["VEH_Label"] = ligne_split[7]
    if (len(ligne_split[8]) >= 1):
        current_item["VEH_VIN"] = ligne_split[8]
    current_item["Item_Serial"] = ligne_split[9].rstrip()
    return current_item
    
    
def Import_from_ExportD2HUB():
    liste_lignes = list()

def get_item_dico_ExportD2HUBcsv(ligne):
    current_item = dict()
    current_item.clear()
    current_item["Item_IMEI"] = ligne["IMEI"]
    current_item["Item_Type"] = ligne["Device type"]
    current_item["Item_FW"] = ligne["Current firmware version"]
    current_item["Item_Serial"] = ligne["Serial number"]
    if (len(ligne["Customer account"]) >= 1):
        current_item["Account_Name"] = ligne["Customer account"]
    if (len(ligne["Registration"]) >= 1):
        current_item["VEH_Immat"] = ligne["Registration"]
    if (len(ligne["Brand"]) >= 1):
        current_item["VEH_Mark"] = ligne["Brand"]
    if (len(ligne["Model"]) >= 1):
        current_item["VEH_Model"] = ligne["Model"]
    if (len(ligne["Serie"]) >= 1):
        current_item["VEH_Serie"] = ligne["Serie"]
    if (len(ligne["Vehicle name"]) >= 1):
        current_item["VEH_Label"] = ligne["Vehicle name"]
    if (len(ligne["VIN"]) >= 1):
        current_item["VEH_VIN"] = ligne["VIN"]  
    if (len(ligne["last OTA update Request Date"]) >= 1):
        current_item["Last_OTA_QUERY_Date"] = ligne["last OTA update Request Date"]  
    if (len(ligne["Date of the first reco message received"]) >= 1):
        current_item["First_RECO_Date"] = ligne["Date of the first reco message received"]  
    if (len(ligne["Date of the last message received"]) >= 1):
        current_item["Last_Msg_Date"] = ligne["Date of the last message received"]  
    if (len(ligne["Current service"]) >= 1):
        current_item["Service_Name"] = ligne["Current service"]  
    return current_item

def Import_from_ExportD2HUBcsv():
    global item_list_2
    global date_fic2
    
    date_fic2 = os.path.getmtime(Configuration.path_ExportD2HUBcsv)
    with open(Configuration.path_ExportD2HUBcsv, mode='r', newline='', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        liste_champs = csv_reader.fieldnames
        if "Type de boitier" in liste_champs:
            print ("Export en franï¿½ais. Il faut utiliser l'export gï¿½nï¿½rï¿½ en anglais")
        else:
            if "Device type" in liste_champs:
                #print ("export en anglais")
                for ligne in csv_reader:
                    #print (ligne)
                    item_list_2.append(get_item_dico_ExportD2HUBcsv(ligne))
    pass
    
    
    
def Dict_from_D2Hub_exports():
    #assemblage des donnï¿½es des 2 sources dans un dictionnaire
    global item_list_1
    global item_list_2
    global item_dico

    current_item = dict()
    current_item.clear()

    for current_item in item_list_1:
        st_IMEI = current_item["Item_IMEI"]
        item_dico[st_IMEI] = current_item
    for current_item in item_list_2:
        st_IMEI = current_item["Item_IMEI"]
        if st_IMEI not in item_dico:
            item_dico[st_IMEI] = dict()
        for cle,valeur in current_item.items():
            if ((date_fic2>date_fic1) or (cle not in item_dico[st_IMEI])):
                #le second fichier est plus recent ou l'information n'existe pas -> on peut ï¿½craser la valeur
                item_dico[st_IMEI][cle] = valeur


def Extract_infos_from_D2hHub():
    global item_list_1
    global item_list_2
    global item_dico

    item_list_1.clear()
    item_list_2.clear()
    item_dico.clear()

    Telech_D2HUb_Info_from_AWS()
    Import_from_ImportD2HUB()       #lecture des donnees de "genericInfo.txt"
    Import_from_ExportD2HUBcsv()    #lecture des donnees de "export.csv"
    Dict_from_D2Hub_exports()       #assemblage des donnees des 2 sources dans un dictionnaire
    Get_Info_Directly_from_D2Hub()  #ces données sont plus récentes et peuvent donc écraser les autres.
    
    #enregistrement des rï¿½sultats
    with open(Configuration.path_json_D2Hub_info1, 'w') as json_file_result:
        json.dump(item_list_1, json_file_result)
    pass
    with open(Configuration.path_json_D2Hub_info2, 'w') as json_file_result:
        json.dump(item_list_2, json_file_result)
    pass 
    with open(Configuration.path_json_D2Hub_info_total, 'w') as json_file_result:
        json.dump(item_dico, json_file_result)
    pass   

    #Effacement des 2 premiï¿½res listes pour gagner en mï¿½moire vive. 
    item_list_1.clear()
    item_list_2.clear()

def Get_D2Hub_Account_list():
    curl_url = 'https://admin.d2hub.fr/api/admin/v2/integration/account.getlist'
    curl_hearders = {'X-Api-Token':'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJqZGV2YXkiLCJhdXRoIjoiUk9MRV9BRE1JTiIsImV4cCI6MTYxMjE3Mjg0MH0.rPqQWR9pw3_LCYZJMMhu8eBhEGmBiXsYdMihY6Ud4Rq6w7ha_mrNx2RwVSnTX4-rGD56vCMVarAFF-Ap1Q3fTg','Accept':'application/json','Content-Type':'application/json'}
    r = requests.get(curl_url, headers = curl_hearders)
    #print (r)
    #r.encoding = 'cp1252'
    with open(Configuration.path_json_D2Hub_account, 'w') as json_file_result:
        json.dump(r.json(), json_file_result)
    pass 
    
if __name__ == '__main__':
    Extract_infos_from_D2hHub()
    '''
    with open('D:\Temp_JSON\OUTPUT\genericInfo.json', 'w') as json_file_result:
        json.dump(item_list_1, json_file_result)
    pass
    with open('D:\Temp_JSON\OUTPUT\exportD2HubCSV.json', 'w') as json_file_result:
        json.dump(item_list_2, json_file_result)
    pass''' 
    with open('D:\Temp_JSON\OUTPUT\exportD2HubGlobal.json', 'w') as json_file_result:
        json.dump(item_dico, json_file_result)
    pass   
    print ("traitement termine")
    
   
    Get_D2Hub_Account_list()
   
    pass
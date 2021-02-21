# -*-coding:utf-8 -*
'''
Created on 5 d�c. 2020

@author: blood
'''

import os
import Configuration
import json
import csv
import requests

item_list_1 = list()    #liste d'�quipement issus de "genericInfo.txt" sous forme de liste
item_list_2 = list()    #liste d'�quipement issus de "export.csv" sous forme de liste
item_dico = dict()      #liste d'�quipement issus de "genericInfo.txt" et de "export.csv" sous forme de dictionnaire (avec l'IMEI pour identifiant principal)
date_fic1 = 0
date_fic2 = 0
account_uuid_list = list()    #liste d'�quipement issus de "export.csv" sous forme de liste

def Get_Info_Directly_from_D2Hub(): #bloque à la page 100
    global item_dico
    current_item = dict()
    list_item = list()
    #Commande � r�p�ter autant de fois que possible:
    #curl -X GET "https://admin.d2hub.fr/api/admin/v2/integration/device.search?page=0" -H "X-Api-Token: eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJqZGV2YXkiLCJhdXRoIjoiUk9MRV9BRE1JTiIsImV4cCI6MTYxMzE5Nzc5NX0.EXEQxe8_bm2G_hatGCKoX1ZnqqPypHybqGf8v0MlkhSSS13uwMzs5fJg_u7O5xFJJDn-bsVNx2L2bu4m0KoUzA" -H "Accept: application/json" -H "Content-Type: application/json"
    num_compte = 1
    nb_compte = len(account_uuid_list)
    print("Recuperation des données des iCAN directement depuis 2Hub.")
    for compte in account_uuid_list:
        print("Recuperation depuis le compte: " + str(num_compte) + " / " + str(nb_compte))
        num_compte += 1
        to_continue = True
        cmd_number = 0
        curl_url = 'https://admin.d2hub.fr/api/admin/v2/integration/device.search?c=' + compte + '&size=100&sort=imei,asc&page='
        #curl_url = 'https://admin.d2hub.fr/api/admin/v2/integration/device.search?size=100&sort=imei,asc&page='
        curl_hearders = {'Accept':'application/json','Content-Type':'application/json'}
        curl_hearders['X-Api-Token'] = Configuration.API_D2HUB_Token
        while to_continue:
            #try:
            #envoi de la commande CURL
            curl_url_nb = curl_url + str(cmd_number)
            #print (curl_url_nb)
            r = requests.get(curl_url_nb, headers = curl_hearders)
            #print (r.status_code)
            if (r.status_code == 200):
                list_item.clear()
                list_item = r.json()
                if len(list_item) >= 1:
                    print("   " + str(len(list_item)) + " objets sur ce compte.")
                    
                    for equipment in list_item:
                        Dict_from_json_Directly_from_D2Hub(equipment)
                    #print (r)
                    #r.encoding = 'cp1252'
                    '''with open(Configuration.path_json_D2Hub_item_list, 'a') as json_file_result:
                        json.dump(list_item, json_file_result)
                        #json.dump(r.json(), json_file_result)
                    pass'''
                else:
                    print("   Aucun objet sur ce compte")
                if len(list_item) < 100:
                    #La dernière réponse n'était pa pleine, pas la peine de continuer.
                    to_continue = False
            else:
                to_continue = False

            #analyse du r�sultat            
            
            #incr�mentation du compteur de page
            cmd_number += 1
            #except:
            #    to_continue = False

        '''to_continue = True
        cmd_number = 0
        curl_url = 'https://admin.d2hub.fr/api/admin/v2/integration/device.search?size=100&sort=imei,desc&page='
        curl_hearders = {'Accept':'application/json','Content-Type':'application/json'}
        curl_hearders['X-Api-Token'] = Configuration.API_D2HUB_Token
        while to_continue:
            try:
                #envoi de la commande CURL
                curl_url_nb = curl_url + str(cmd_number)
                print (curl_url_nb)
                r = requests.get(curl_url_nb, headers = curl_hearders)
                print (r.status_code)
                if (r.status_code == 200):
                    #print (r)
                    #r.encoding = 'cp1252'
                    with open(Configuration.path_json_D2Hub_item_list, 'a') as json_file_result:
                        json.dump(r.json(), json_file_result)
                    pass
                else:
                    to_continue = False
    
                #analyse du r�sultat            
                
                #incr�mentation du compteur de page
                cmd_number += 1
            except:
                to_continue = False'''
            
def Dict_from_json_Directly_from_D2Hub(equipment):
    global item_dico

    current_item = dict()
    current_item.clear()
    
    st_IMEI = equipment["imei"]
    if st_IMEI not in item_dico:
        item_dico[st_IMEI] = dict()
        item_dico[st_IMEI]["Item_IMEI"] = st_IMEI
    if "account" in equipment:
        if "accountName" in equipment["account"]:
            item_dico[st_IMEI]["Account_Name"] = equipment["account"]["accountName"]
        if "uuid" in equipment["account"]:
            item_dico[st_IMEI]["Account_ID"] = equipment["account"]["uuid"]
    if "type" in equipment:
        item_dico[st_IMEI]["Item_Type"] = equipment["type"]
    if "firmware" in equipment:
        if "firmwareTag" in equipment["firmware"]:
            item_dico[st_IMEI]["Item_FW"] = equipment["firmware"]["firmwareTag"]
    if "vehicle" in equipment:
        if type(equipment["vehicle"]) == dict:
            if "registration" in equipment["vehicle"]:
                item_dico[st_IMEI]["VEH_Immat"] = equipment["vehicle"]["registration"]
            if "vin" in equipment["vehicle"]:
                item_dico[st_IMEI]["VEH_VIN"] = equipment["vehicle"]["vin"]
            if "name" in equipment["vehicle"]:
                item_dico[st_IMEI]["VEH_Label"] = equipment["vehicle"]["name"]
            if "model" in equipment["vehicle"]:
                if type(equipment["vehicle"]["model"]) == dict:
                    if "brand" in equipment["vehicle"]["model"]:
                        if "name" in equipment["vehicle"]["model"]["brand"]:
                            item_dico[st_IMEI]["VEH_Mark"] = equipment["vehicle"]["model"]["brand"]["name"]
                    if "name" in equipment["vehicle"]["model"]:
                        item_dico[st_IMEI]["VEH_Model"] = equipment["vehicle"]["model"]["name"]
                    if "serie" in equipment["vehicle"]["model"]:
                        item_dico[st_IMEI]["VEH_Serie"] = equipment["vehicle"]["model"]["serie"]
            if "nbCylinders" in equipment["vehicle"]:
                item_dico[st_IMEI]["VEH_Motor_NbCyl"] = str(equipment["vehicle"]["nbCylinders"])
            if "engineDisplacement" in equipment["vehicle"]:
                item_dico[st_IMEI]["VEH_Motor_Cyl"] = str(equipment["vehicle"]["engineDisplacement"])
            if "fuelType" in equipment["vehicle"]:
                item_dico[st_IMEI]["VEH_Motor_FuelType"] = str(equipment["vehicle"]["fuelType"])
    if "serialNumber" in equipment:
        item_dico[st_IMEI]["Item_Serial"] = str(equipment["serialNumber"])
    if "lastMessageDate" in equipment:
        item_dico[st_IMEI]["Last_Msg_Date"] = equipment["lastMessageDate"]
    if "serviceType" in equipment:
        if type(equipment["serviceType"]) == dict:
            #print(equipment)
            if "toto" in equipment["serviceType"]:
                if len(equipment["serviceType"]["name"]) > 0:
                    item_dico[st_IMEI]["Service_Name"] = equipment["serviceType"]["name"]
    if "parameters" in equipment:
        #lecture des paramètres de configuration
        for conf_param in equipment["parameters"]:
            if conf_param["id"] == 18:
                item_dico[st_IMEI]["VEH_Motor_ConsoFormul"] = conf_param["value"]
                



def Telech_D2HUb_Info_from_AWS():
    cmd_list = list()
    print("Telechargement d'informations depuis AWS")
    commande = "start aws s3 sync s3://exchange.d2hub.fr/checkers/ " + Configuration.path_InputD2HUB    #cette requete donne des r�sultats obsolettes
    #cmd_list.append(commande)
    commande = "start aws s3 sync s3://exchange.d2hub.fr/iCANGeneralInfo/ " + Configuration.path_InputD2HUB
    cmd_list.append(commande)
    nb_req = len(cmd_list)
    i = 0
    for str_cmd in cmd_list:
        i+=1
        os.system(str_cmd)
        print ("Commande " + str(i) + " / " + str(nb_req))
    print("Telechargement en cours")
    os.system("pause") # On met le programme en pause pour éviter qu'il ne se referme (Windows)
    
    
def Import_from_ImportD2HUB():
    #import depuis genericInfo.txt
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
            print ("Export en fran�ais. Il faut utiliser l'export g�n�r� en anglais")
        else:
            if "Device type" in liste_champs:
                #print ("export en anglais")
                for ligne in csv_reader:
                    #print (ligne)
                    item_list_2.append(get_item_dico_ExportD2HUBcsv(ligne))
    pass
    
    
    
def Dict_from_D2Hub_exports():
    #assemblage des donn�es des 2 sources dans un dictionnaire
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
                #le second fichier est plus recent ou l'information n'existe pas -> on peut �craser la valeur
                item_dico[st_IMEI][cle] = valeur


def Extract_infos_from_D2hHub():
    global item_list_1
    global item_list_2
    global item_dico

    #extraction des données dans l'ordre des plus vieilles aux plus recente/fiables

    bretour = False
    txt_input = input("Avez-vous mis � jour l'Api-Token (O pour oui) ?")
    try:
        if ((txt_input[0] == "O") or (txt_input[0] == "o")):
            bretour = True
    except:
        bretour = False
    if bretour:
        Get_D2Hub_Account_list()
        
        item_list_1.clear()
        item_list_2.clear()
        item_dico.clear()
    
        #export depuis 2 fichiers à copier manuellement
        Import_from_ImportD2HUB()       #lecture des donnees de "genericInfo.txt"
        Import_from_ExportD2HUBcsv()    #lecture des donnees de "export.csv"
        Dict_from_D2Hub_exports()       #assemblage des donnees des 2 sources dans un dictionnaire

        #export depuis 1 fichier mis à jour la nuit sur AWS
        Telech_D2HUb_Info_from_AWS()
        
        #export direct depuis D2Hub
        Get_Info_Directly_from_D2Hub()  #ces donn�es sont plus r�centes et peuvent donc �craser les autres.
        
        #enregistrement des r�sultats
        '''with open(Configuration.path_json_D2Hub_info1, 'w') as json_file_result:
            json.dump(item_list_1, json_file_result)
        pass
        with open(Configuration.path_json_D2Hub_info2, 'w') as json_file_result:
            json.dump(item_list_2, json_file_result)
        pass''' 
        with open(Configuration.path_json_D2Hub_info_total, 'w') as json_file_result:
            json.dump(item_dico, json_file_result)
        pass   
    
        #Effacement des 2 premieres listes pour gagner en m�moire vive. 
        item_list_1.clear()
        item_list_2.clear()
        
        
    else:
        print("Mettez � jour l'Api-Token (du module Configuration).")


def Get_D2Hub_Account_list():
    global account_uuid_list
    curl_url = 'https://admin.d2hub.fr/api/admin/v2/integration/account.getlist'
    curl_hearders = {'Accept':'application/json','Content-Type':'application/json'}
    curl_hearders['X-Api-Token'] = Configuration.API_D2HUB_Token
    r = requests.get(curl_url, headers = curl_hearders)
    #print (r)
    #r.encoding = 'cp1252'
    if (r.status_code == 200):
        with open(Configuration.path_json_D2Hub_account, 'w') as json_file_result:
            json.dump(r.json(), json_file_result)
        pass
        account_uuid_list.clear()
        for compte in r.json():
            account_uuid_list.append(compte["uuid"])
    else:
        print("probleme dans la requete API de recuperation des comptes utilisateurs")
    
    
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
    
    pass
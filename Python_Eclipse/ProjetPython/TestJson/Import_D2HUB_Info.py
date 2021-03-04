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
import time
import re
import Boite_Outils

item_dico = dict()      #liste d'�quipement issus de "genericInfo.txt" et de "export.csv" sous forme de dictionnaire (avec l'IMEI pour identifiant principal)
account_dico = dict()
date_fic1 = 0
date_fic2 = 0
account_uuid_list = list()
start_time = 0
end_time = 0

def recup_D2Hub_API_Token():
    curl_url = 'https://admin.d2hub.fr/api/admin/public/authenticate'
    curl_headers = {'Accept':'application/json','Content-Type':'application/json'}
    curl_payload = {'password':Configuration.API_D2HUB_PASS,'username':Configuration.API_D2HUB_USER,"rememberMe":True}
    r = requests.post(curl_url, headers = curl_headers, json = curl_payload)
    if (r.status_code == 200):
        tokenAuth = r.json()["id_token"]
        Configuration.set_D2HubToken(tokenAuth)
        Configuration.set_D2Hub_xsrf_Token(re.sub(".*XSRF-TOKEN=(.*);.*",'\\1',r.headers['Set-Cookie']))
        
        return True
    else:
        print("cmdNOK: " + str(r.status_code))
        return False

'''def Get_Info_Directly_from_D2Hub_by_account(): #récupération de la liste des devices en passant par l'API device.search de D2Hub en filtrant puis en bouclant sur les comptes
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
        nb_item = 0
        num_compte += 1
        to_continue = True
        cmd_number = 0
        curl_url = 'https://admin.d2hub.fr/api/admin/v2/integration/device.search?c=' + compte + '&size=100&sort=imei,asc&page='
        #curl_url = 'https://admin.d2hub.fr/api/admin/v2/integration/device.search?size=100&sort=imei,asc&page='
        curl_hearders = {'Accept':'application/json','Content-Type':'application/json'}
        curl_hearders['X-Api-Token'] = Configuration.API_D2HUB_Token
        while to_continue:
            try:
                #envoi de la commande CURL
                curl_url_nb = curl_url + str(cmd_number)
                r = requests.get(curl_url_nb, headers = curl_hearders)
                if (r.status_code == 200):
                    list_item.clear()
                    list_item = r.json()
                    if len(list_item) >= 1:
                        if (cmd_number == 0):
                            nb_item = r.headers['X-Total-Count']
                            print("   " + str(nb_item) + " objets sur ce compte.")
                        for equipment in list_item:
                            Dict_from_json_Directly_from_D2Hub(equipment)
                    else:
                        if (cmd_number == 0):
                            print("   Aucun objet sur ce compte")
                    if len(list_item) < 100:
                        #La dernière réponse n'était pa pleine, pas la peine de continuer.
                        to_continue = False
                else:
                    to_continue = False
                #incr�mentation du compteur de page
                cmd_number += 1
            except:
                to_continue = False'''


def Get_Info_Directly_from_D2Hub(): #récupération de la liste des devices en passant par l'API device.search de D2Hub
    global item_dico
    list_item = list()
    raw_list_item = list()
    raw_list_item.clear()
    last_IMEI = "000000000000000"
    #Commande � r�p�ter autant de fois que possible:
    #curl -X GET "https://admin.d2hub.fr/api/admin/v2/integration/device.search?page=0" -H "X-Api-Token: eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJqZGV2YXkiLCJhdXRoIjoiUk9MRV9BRE1JTiIsImV4cCI6MTYxMzE5Nzc5NX0.EXEQxe8_bm2G_hatGCKoX1ZnqqPypHybqGf8v0MlkhSSS13uwMzs5fJg_u7O5xFJJDn-bsVNx2L2bu4m0KoUzA" -H "Accept: application/json" -H "Content-Type: application/json"
    nb_item = 0
    to_continue = True
    num_page = 0
    nb_page = 0
    
    #curl_url = 'https://admin.d2hub.fr/api/admin/v2/integration/device.search?size=100&sort=imei,asc&page='
    curl_hearders = {'Accept':'application/json','Content-Type':'application/json'}
    curl_hearders['X-Api-Token'] = Configuration.API_D2HUB_Token
    while to_continue:
        try:
            #envoi de la commande CURL
            curl_url = 'https://admin.d2hub.fr/api/admin/v2/integration/device.search?&size=100&sort=imei,asc&page=0&f=imei:>' + last_IMEI
            r = requests.get(curl_url, headers = curl_hearders)
            if (r.status_code == 200):
                list_item.clear()
                list_item = r.json()
                if (len(list_item) >= 1):
                    raw_list_item.extend(list_item)
                    if (num_page == 0):
                        nb_item = r.headers['X-Total-Count']
                        print("   " + str(nb_item) + " objets.")
                        nb_page = int(nb_item)//100
                    print("page: " + str(num_page) + " / " + str(nb_page))
                    for equipment in list_item:
                        Dict_from_json_Directly_from_D2Hub(equipment)
                        last_IMEI = equipment["imei"]
                else:
                    if (num_page == 0):
                        print("   Aucun objet sur ce compte")
                if len(list_item) < 100:
                    #La dernière réponse n'était pa pleine, pas la peine de continuer.
                    to_continue = False
            else:
                to_continue = False
            #incr�mentation du compteur de page
            num_page += 1
        except:
            to_continue = False
    with open(Configuration.path_json_D2Hub_equipment_list_raw, 'w') as json_file_result:
        json.dump(raw_list_item, json_file_result, indent=4)
    pass   

def set_item_activ_communicating():
    global item_dico
    for equipment in item_dico.values():
        #print(equipment)
        equipment["Item_active"] = ""
        if "Last_OTA_QUERY_Date" in equipment:
            if(Boite_Outils.is_date_recent(equipment["Last_OTA_QUERY_Date"])):
                equipment["Item_active"] = True
            else:
                equipment["Item_active"] = False
            if "Last_Msg_Date" in equipment:
                if(Boite_Outils.is_date_recent(equipment["Last_Msg_Date"])):
                    equipment["Item_communicating"] = True
                else:
                    equipment["Item_communicating"] = False
            else:
                equipment["Item_communicating"] = False
        else:
            #le boitier n'a jamais tenté d'OTA. Il arrive qu'on ait reçu un message unique un jour.
            equipment["Item_communicating"] = False
            equipment["Item_active"] = False

            
def Dict_from_json_Directly_from_D2Hub(equipment):
    global item_dico

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
    #os.system("pause") # On met le programme en pause pour éviter qu'il ne se referme (Windows) -> pas besoin 
    
'''    #maintenant inutile: le fichier GenericInfo.txt est extrait des mêmes données que les API de D2Hub: /api/admin/v2/integration/device.search
def Import_from_ImportD2HUB():
    #import depuis genericInfo.txt
    global item_list_1
    global date_fic1
    liste_lignes = list()
    date_fic1 = os.path.getmtime(Configuration.path_ImportD2HUB)
    with open(Configuration.path_ImportD2HUB, 'r')as mon_fichier:
        liste_lignes = mon_fichier.readlines()
        for ligne in liste_lignes:
            item_list_1.append(get_item_dico(ligne))'''

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
    global item_dico

    st_IMEI = ligne["IMEI"]
    if st_IMEI not in item_dico:
        item_dico[st_IMEI] = dict()
        item_dico[st_IMEI]["Item_IMEI"] = st_IMEI
    
    item_dico[st_IMEI]["Item_IMEI"] = ligne["IMEI"]
    item_dico[st_IMEI]["Item_Type"] = ligne["Device type"]
    item_dico[st_IMEI]["Item_FW"] = ligne["Current firmware version"]
    item_dico[st_IMEI]["Item_Serial"] = ligne["Serial number"]
    if (len(ligne["Customer account"]) >= 1):
        item_dico[st_IMEI]["Account_Name"] = ligne["Customer account"]
    if (len(ligne["Registration"]) >= 1):
        item_dico[st_IMEI]["VEH_Immat"] = ligne["Registration"]
    if (len(ligne["Brand"]) >= 1):
        item_dico[st_IMEI]["VEH_Mark"] = ligne["Brand"]
    if (len(ligne["Model"]) >= 1):
        item_dico[st_IMEI]["VEH_Model"] = ligne["Model"]
    if (len(ligne["Serie"]) >= 1):
        item_dico[st_IMEI]["VEH_Serie"] = ligne["Serie"]
    if (len(ligne["Vehicle name"]) >= 1):
        item_dico[st_IMEI]["VEH_Label"] = ligne["Vehicle name"]
    if (len(ligne["VIN"]) >= 1):
        item_dico[st_IMEI]["VEH_VIN"] = ligne["VIN"]  
    if (len(ligne["last OTA update Request Date"]) >= 1):
        item_dico[st_IMEI]["Last_OTA_QUERY_Date"] = ligne["last OTA update Request Date"] 
    if (len(ligne["Date of the first reco message received"]) >= 1):
        item_dico[st_IMEI]["First_RECO_Date"] = ligne["Date of the first reco message received"]  
    if (len(ligne["Date of the last message received"]) >= 1):
        item_dico[st_IMEI]["Last_Msg_Date"] = ligne["Date of the last message received"]  
    if (len(ligne["Current service"]) >= 1):
        item_dico[st_IMEI]["Service_Name"] = ligne["Current service"]  


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
                    get_item_dico_ExportD2HUBcsv(ligne)
    pass
    
def Telech_Export_csv_from_D2Hub():
    to_continue = True
    
    curl_hearders1 = {}
    curl_hearders1['cookie'] = 'NG_TRANSLATE_LANG_KEY=%22en%22; XSRF-TOKEN=' + Configuration.API_D2HUB_xsrf_Token
    curl_hearders1['x-xsrf-token'] = Configuration.API_D2HUB_xsrf_Token
    curl_hearders1['X-Api-Token'] = Configuration.API_D2HUB_Token
    curl_url1 = 'https://admin.d2hub.fr/api/admin/v2/devices/export?format=CSV&full=true&sort=accountName,asc'
    curl_json1 = {"c":"1e50b244-3953-442e-a210-632a50dcf2fe"}
    
    try:
        r = requests.post(curl_url1, headers = curl_hearders1, json=curl_json1)
        tempfile_name = str(r.text)
        #print ("r.status_code: " + str(r.status_code))
        #print ("r.headers: " + str(r.headers))
        #print ("r.text: " + str(r.text))
        #print ("fini")
    except:
        print ("erreur")
        to_continue = False
        
    if to_continue:
        #xsrf_token = 'bcfa9285-2b1d-406e-830c-5008fd1c0f59'
        curl_url2 = 'https://admin.d2hub.fr/api/admin/v2/devices/export?filename=' + tempfile_name + '&format=CSV'
        curl_hearders2 = {}
        curl_hearders2['cookie'] = 'NG_TRANSLATE_LANG_KEY=%22fr%22; XSRF-TOKEN=' + Configuration.API_D2HUB_xsrf_Token
        curl_hearders2['x-xsrf-token'] = Configuration.API_D2HUB_xsrf_Token
        curl_hearders2['X-Api-Token'] = Configuration.API_D2HUB_Token
    while to_continue:
        r = requests.get(curl_url2, headers = curl_hearders2,stream=True)
        #print ("r.status_code: " + str(r.status_code))
        #print ("r.headers: " + str(r.headers))
        #print ("r.text: " + str(r.text))
        if str(r.status_code) == '204':
            print ("Generation en cours")
        else:
            to_continue = False
            try:
                if str(r.status_code) == '200':
                    print ("Generation terminee OK")
                    '''with open('D:\Temp_JSON/export1.csv', 'w', newline='') as fp:
                        fp.write(str(r.text))
                        print ("Telechargement OK")                    
                    with open('D:\Temp_JSON/export2.csv', 'w') as fp:
                        fp.write(str(r.text))
                        print ("téléchargement OK")'''                    
                    with open(Configuration.path_ExportD2HUBcsv, 'wb') as fp:
                        fp.write(r.content)
                        print ("téléchargement OK")                    
                else:
                    print ("echec de téléchargement")
            except:
                to_continue = False

    

def Extract_infos_from_D2Hub():
    global item_dico

    #extraction des données dans l'ordre des plus vieilles aux plus recente/fiables

    bretour = recup_D2Hub_API_Token()
    if (bretour == False):
        print("Le token n'a pas pu être récupéré automatiquement.")
        txt_input = input("Avez-vous mis a jour manuellement l'Api-Token (O pour oui) ?")
        try:
            if ((txt_input[0] == "O") or (txt_input[0] == "o")):
                bretour = True
        except:
            bretour = False
    if bretour:
        #Telechargement des fichiers sur AWS
        Telech_D2HUb_Info_from_AWS()

        item_dico.clear()
    
        #export depuis export.csv téléchargé automatiquement ici
        Telech_Export_csv_from_D2Hub()
        Import_from_ExportD2HUBcsv()    #lecture des donnees de "export.csv"

        
        #export direct depuis D2Hub
        Get_Info_Directly_from_D2Hub()  #ces donn�es sont plus r�centes et peuvent donc �craser les autres.
        
        set_item_activ_communicating()
        
        Get_Info_from_ICAN_HARDSTATUS()
        
        #enregistrement des r�sultats
        with open(Configuration.path_json_D2Hub_info_total, 'w') as json_file_result:
            json.dump(item_dico, json_file_result, indent=4)
        pass   
    
        #traitement de la liste des comptes
        Get_D2Hub_Account_list()
    
    else:
        print("Mettez � jour l'Api-Token (du module Configuration).")

def Get_Info_from_ICAN_HARDSTATUS():
    #on ne récupère que le bucket
    global item_dico
    
    with open(Configuration.path_D2Hub_ICAN_HARD_STATUS, mode='r', newline='', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for ligne in csv_reader:
            st_IMEI = ligne["imei"]
            if type(st_IMEI) == str:
                #Msg_Bucket
                st_Temp = ligne["targetplatform"]
                if type(st_Temp) == str:
                    if len(st_Temp) >= 1:
                        if st_Temp == "-Inherited-":
                            st_Temp = "MARKETIP"
                        if "MARKETIP" in st_Temp:
                            st_Temp = "MARKETIP"
                    else:
                        st_Temp = "MARKETIP"
                else:
                    st_Temp = "MARKETIP"
                item_dico[st_IMEI]["Msg_Bucket"] = st_Temp
                #Item_conf_Validity
                st_Temp = ligne["config_valid"]
                item_dico[st_IMEI]["Item_conf_Validity"] = st_Temp
    pass
    

def Get_D2Hub_Account_list():
    global account_uuid_list
    global account_dico
    
    
    curl_url = 'https://admin.d2hub.fr/api/admin/v2/integration/account.getlist'
    curl_hearders = {'Accept':'application/json','Content-Type':'application/json'}
    curl_hearders['X-Api-Token'] = Configuration.API_D2HUB_Token
    r = requests.get(curl_url, headers = curl_hearders)
    
    if (r.status_code == 200):
        account_dico.clear()
        with open(Configuration.path_json_D2Hub_account_raw, 'w') as json_file_result:
            json.dump(r.json(), json_file_result, indent=4)
        pass
        account_uuid_list.clear()
        for compte in r.json():
            account_uuid_list.append(compte["uuid"])
            account_dico[compte["uuid"]] = dict()
            account_dico[compte["uuid"]]["uuid"] = compte["uuid"]
            account_dico[compte["uuid"]]["parentUuid"] = compte["parentUuid"]
            account_dico[compte["uuid"]]["accountName"] = compte["accountName"]
            account_dico[compte["uuid"]]["parentName"] = compte["parentName"]
            account_dico[compte["uuid"]]["state"] = compte["state"]
            if (compte["parentName"] == "ADMIN_ROOT") or (compte["accountName"] == "ADMIN_ROOT"):
                account_dico[compte["uuid"]]["isMaster"] = True
            else:
                account_dico[compte["uuid"]]["isMaster"] = False

        for compte_uuid in account_dico:
            if  account_dico[compte_uuid]["isMaster"] == False:
                to_continue = True
                parent_uuid = account_dico[compte_uuid]["parentUuid"]
                while to_continue:
                    if account_dico[parent_uuid]["isMaster"] == True:
                        account_dico[compte_uuid]["MasterName"] = account_dico[parent_uuid]["accountName"]
                        account_dico[compte_uuid]["MastertUuid"] = account_dico[parent_uuid]["uuid"]
                        to_continue = False
                    else:
                        parent_uuid = account_dico[parent_uuid]["parentUuid"]
        with open(Configuration.path_json_D2Hub_account, 'w') as json_file_result:
            json.dump(account_dico, json_file_result, indent=4)
        pass
    else:
        print("probleme dans la requete API de recuperation des comptes clients")
    
    
def get_bucket_IMEI(stIMEI):
    global item_dico
    
    if len(item_dico) == 0:
        #le dictionnaire est vide, on va le remplir depuis le fichier json
        print("Remplissage du dictionnaire")
        with open(Configuration.path_json_D2Hub_info_total) as json_file:
            item_dico = json.load(json_file)
    bucket = item_dico[stIMEI]["Msg_Bucket"]
    #print("bucket: ", bucket)
    return bucket


if __name__ == '__main__':
    start_time = time.time()
    print ("Debut")
    Extract_infos_from_D2Hub()
    print ("Traitement termine")
    end_time = time.time()
    print( end_time-start_time, "secondes d'executions")    
    pass
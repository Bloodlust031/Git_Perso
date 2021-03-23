# -*-coding:Latin-1 -*
'''
Created on 26 nov. 2020

@author: blood
'''

from datetime import date
from datetime import timedelta

import sys
import os
import configparser

deja_init = False

to_integrate_Msg_bin = False
to_integrate_Msg_raw = False
to_integrate_Msg_cnt = False
to_integrate_Msg_decompose = False
to_integrate_Msg_non_decompose_D2Hub = True

Chemin_json = 'D:\Temp_JSON\INPUT_Msg'
Chemin_json_Outil_iCAN = 'TempDownAWSS3'

path_sortie = 'D:/Temp_JSON/OUTPUT/'
path_sortie_Stat = 'D:/Temp_JSON/OUTPUT/Stat/'
path_InputD2HUB = 'D:\Temp_JSON\INPUT_D2HUB/'
path_ExportD2HUBcsv = 'D:\Temp_JSON\INPUT_D2HUB/export.csv'
path_json_D2Hub_info_total = 'D:\Temp_JSON\INPUT_D2HUB\exportD2HubGlobal.json'   #dictionnaire des équipements declares sur D2Hub 
path_json_D2Hub_equipment_list_raw = 'D:\Temp_JSON\INPUT_D2HUB\D2Hub_equipment_list_raw.json'   #dictionnaire des équipements declares sur D2Hub
path_json_D2Hub_account = 'D:\Temp_JSON\INPUT_D2HUB\Account_dict.json'
path_json_D2Hub_account_raw = 'D:\Temp_JSON\INPUT_D2HUB\Account_list_raw.json'
path_D2Hub_ICAN_HARD_STATUS = 'D:\Temp_JSON\INPUT_D2HUB\ICAN_HARD_STATUS.csv'           
path_json_log_D2HubInfo = 'D:\Temp_JSON\OUTPUT\Log_D2HubInfo.log'

API_D2HUB_USER = 'admin'
API_D2HUB_PASS = 'w,DVBYMbQAz@&6x5HlUFY:bz-z0d7'
#API_D2HUB_USER = 'jdevay'
#API_D2HUB_PASS = 'Bordel31'

#valeurs remplies automatiquement par des API de D2Hub
API_D2HUB_Token = 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJqZGV2YXkiLCJhdXRoIjoiUk9MRV9BRE1JTiIsImV4cCI6MTYxNDA3MDQ1NX0._wCx66P4G_-Ed3oYBkLkTpK96CkvZTM6H4F1l1maNNvwGV68kTWSTeMYtDsTSkkEZKjiScsBsExSDGsAJRzemQ'
API_D2HUB_xsrf_Token = 'bcfa9285-2b1d-406e-830c-5008fd1c0f59'

#ATTENTION: ces information peuvent être surchargées par la fonction "maj_configuration" du module Telech_AWS_Json
IMEI_list = ['867322034083212','867322034092015','867322034105809']
Date_list = ['2020-12-02','2020-12-03']

lbl_msg_Dic_Params_D2Hub_cnt = 'Msg_Params_decompose_D2Hub_cnt'  #decomposition du message en paramètre réalisé par D2Hub - Sous forme de dictionnaire
lbl_msg_Dic_Params_D2Hub_raw = 'Msg_Params_decompose_D2Hub_raw'             #decomposition du message en paramètre réalisé par D2Hub - Sous forme de texte
lbl_msg_Dic_Params_Python = 'Msg_Params_decompose_Python'
lbl_msg_Dic_Params_NonD2Hub = 'Msg_Params_non_decompose_D2Hub'

distribution_delais_GSM = [10, 60, 120, 180, 300, 600, 1200, 3600]    #Distribution des délais de réception en secondes

def set_IMEI_List(liste):
    global IMEI_list
    IMEI_list.clear()
    IMEI_list = liste.copy()

def set_Date_list(str_Date_Deb, str_Date_fin="0"):
    global Date_list
    Date_list.clear()
    if str_Date_fin=="0":
        Date_list.append(str_Date_Deb)
    else:
        #remplissage de la liste avec chaque jour entre la date de début et la date de fin
        d_date_deb = date.fromisoformat(str_Date_Deb)
        d_date_fin = date.fromisoformat(str_Date_fin)
        ecart = d_date_fin - d_date_deb
        for i in range(0, (ecart.days+1)):
            d_date_temp = d_date_deb + timedelta(days=i)
            str_date_temp = d_date_temp.isoformat()
            Date_list.append(str_date_temp)

def set_D2HubToken(auth_Token):
    global API_D2HUB_Token
    API_D2HUB_Token = auth_Token    

def set_D2Hub_xsrf_Token(auth_Token):
    global API_D2HUB_xsrf_Token
    API_D2HUB_xsrf_Token = auth_Token    
    
def write_config_ini(Chemin):
    config = configparser.ConfigParser()
    
    config['Extract_VCI_files_content'] = {'bin' : to_integrate_Msg_bin,
                                           'raw' : to_integrate_Msg_raw,
                                           'cnt' : to_integrate_Msg_cnt,
                                           'decompose' : to_integrate_Msg_decompose,
                                           'non_decompose_D2Hub' : to_integrate_Msg_non_decompose_D2Hub}
    config['API_D2HUB'] = {'user' : API_D2HUB_USER,
                           'pass' : API_D2HUB_PASS}

    with open(Chemin, 'w') as configfile:
        config.write(configfile)
    
def read_config_ini(Chemin):
    global API_D2HUB_USER
    global API_D2HUB_PASS
    
    if os.path.exists(Chemin):
        #Lecture du fichier de configuration
        config = configparser.ConfigParser()
        config.read(Chemin)
        if 'API_D2HUB' in config:
            if 'user' in config['API_D2HUB']:
                API_D2HUB_USER = config['API_D2HUB']['user']
            if 'pass' in config['API_D2HUB']:
                API_D2HUB_PASS = config['API_D2HUB']['pass']
        
    #Ecriture de Config.ini"
    write_config_ini(Chemin)
    
def init_config():
    global deja_init
    
    if not deja_init:
        pathname = os.path.dirname(sys.argv[0])
        Chemin = os.path.abspath(pathname) + "\Config.ini"
        read_config_ini(Chemin)
        write_config_ini(Chemin)
        deja_init = True

if __name__ == '__main__':
    init_config()
    print('D2Hub API username: ' + API_D2HUB_USER)
    set_Date_list('2020-11-22', '2020-12-11')
    print (Date_list)
    pass
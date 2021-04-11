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
import json
import ast
import Boite_Outils

deja_init = False

to_integrate_Msg_bin = False
to_integrate_Msg_raw = False
to_integrate_Msg_cnt = False
to_integrate_Msg_decompose = False
to_integrate_Msg_non_decompose_D2Hub = True

Chemin_json = 'D:\Temp_JSON\INPUT_Msg'
Chemin_json_msg = 'D:\Temp_JSON\INPUT_Msg\TempDownAWSS3'
Chemin_json_failure = 'D:\Temp_JSON\INPUT_Msg\Failure'
Chemin_json_reco = 'D:\Temp_JSON\INPUT_Msg\Reco'
Chemin_json_rescue = 'D:\Temp_JSON\INPUT_Msg\Rescue'
Chemin_json_BatTemp = 'D:\Temp_JSON\INPUT_Msg\BatTemp'

Chemin_json_Outil_iCAN = 'TempDownAWSS3'

path_sortie = 'D:/Temp_JSON/OUTPUT/'
path_sortie_Stat = 'D:/Temp_JSON/OUTPUT/Stat/'
path_InputD2HUB = 'D:\Temp_JSON\INPUT_D2HUB/'
path_json_D2Hub_info_total = path_InputD2HUB + 'Processed_Equipement_List.json' #dictionnaire des équipements declares sur D2Hub
path_json_D2Hub_account = path_InputD2HUB + 'Processed_Account_List.json'       #dictionnaire des comptes declares sur D2Hub

API_D2HUB_USER = 'admin'
API_D2HUB_PASS = 'w,DVBYMbQAz@&6x5HlUFY:bz-z0d7'

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

str_veh_list = ["MASTER","DAILY","MAXITY","CLIO","RANGER"]

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
    config['Path'] = {'path_sortie' : path_sortie,
                      'path_sortie_Stat' : path_sortie_Stat,
                      'path_InputD2HUB' : path_InputD2HUB,
                      'path_Input_msg': Chemin_json}
    config['Stat'] = {'Veh_list' : str_veh_list}
                      
    with open(Chemin, 'w') as configfile:
        config.write(configfile)
    
def read_config_ini(Chemin):
    global API_D2HUB_USER
    global API_D2HUB_PASS
    global to_integrate_Msg_bin
    global to_integrate_Msg_raw
    global to_integrate_Msg_cnt
    global to_integrate_Msg_decompose
    global to_integrate_Msg_non_decompose_D2Hub
    global path_sortie
    global path_sortie_Stat
    global path_InputD2HUB
    global path_json_D2Hub_info_total
    global Chemin_json
    global str_veh_list
    
    
    if os.path.exists(Chemin):
        #Lecture du fichier de configuration
        config = configparser.ConfigParser()
        config.read(Chemin)
        if 'API_D2HUB' in config:
            if 'user' in config['API_D2HUB']:
                API_D2HUB_USER = config['API_D2HUB']['user']
            if 'pass' in config['API_D2HUB']:
                API_D2HUB_PASS = config['API_D2HUB']['pass']
        if 'Extract_VCI_files_content' in config:
            if 'bin' in config['Extract_VCI_files_content']:
                to_integrate_Msg_bin = config['Extract_VCI_files_content']['bin']
            if 'raw' in config['Extract_VCI_files_content']:
                to_integrate_Msg_raw = config['Extract_VCI_files_content']['raw']
            if 'cnt' in config['Extract_VCI_files_content']:
                to_integrate_Msg_cnt = config['Extract_VCI_files_content']['cnt']
            if 'decompose' in config['Extract_VCI_files_content']:
                to_integrate_Msg_decompose = config['Extract_VCI_files_content']['decompose']
            if 'non_decompose_D2Hub' in config['Extract_VCI_files_content']:
                to_integrate_Msg_non_decompose_D2Hub = config['Extract_VCI_files_content']['non_decompose_D2Hub']
        if 'Path' in config:
            if 'path_sortie' in config['Path']:
                path_sortie = config['Path']['path_sortie']
            if 'path_sortie_Stat' in config['Path']:
                path_sortie_Stat = config['Path']['path_sortie_Stat']
            if 'path_InputD2HUB' in config['Path']:
                path_InputD2HUB = config['Path']['path_InputD2HUB']
                path_json_D2Hub_info_total = path_InputD2HUB + 'Processed_Equipement_List.json' 
                path_json_D2Hub_account = path_InputD2HUB + 'Processed_Account_List.json'
            if 'path_Input_msg' in config['Path']:
                Chemin_json = config['Path']['path_Input_msg']
                Chemin_json_msg = Chemin_json + 'TempDownAWSS3'
                Chemin_json_failure = Chemin_json + 'Failure'
                Chemin_json_reco = Chemin_json + 'Reco'
                Chemin_json_rescue = Chemin_json + 'TempDownAWSS3'
                Chemin_json_BatTemp = Chemin_json + 'BatTemp'
        if 'Stat' in config:
            if 'Veh_list' in config['Stat']:
                str_veh_list = ast.literal_eval(config.get("Stat","Veh_list"))  #pour décomposer la liste
    #Ecriture de Config.ini"
    write_config_ini(Chemin)
    
@Boite_Outils.print_temps    
def init_config():
    global deja_init
    
    if not deja_init:
        pathname = os.path.dirname(sys.argv[0])
        Chemin = os.path.abspath(pathname) + "\Config.ini"
        read_config_ini(Chemin)
        write_config_ini(Chemin)
        deja_init = True

def verif_create_dossier(st_chemin):
    if not os.path.exists(st_chemin):
        try:
            os.makedirs(st_chemin)
        except:
            print ("Ce dossier n'existe pas et il est impossible de le créer: " + st_chemin)
        
        
            

if __name__ == '__main__':
    init_config()
    
    print('D2Hub API username: ' + API_D2HUB_USER)
    set_Date_list('2020-11-22', '2020-12-11')
    print (Date_list)
    
    pass
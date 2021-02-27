# -*-coding:Latin-1 -*
'''
Created on 26 nov. 2020

@author: blood
'''

from datetime import date
from datetime import timedelta

to_integrate_Msg_bin = False
to_integrate_Msg_raw = False
to_integrate_Msg_cnt = False
to_integrate_Msg_decompose = False
to_integrate_Msg_non_decompose_D2Hub = True

Chemin_json = 'D:\Temp_JSON\INPUT_Msg'
#Chemin_json = 'D:\Boulot\Main\Ican\Extract_traces_FTP\TempDownAWSS3'
path_sortie = 'D:/Temp_JSON/OUTPUT/'
path_InputD2HUB = 'D:\Temp_JSON\INPUT_D2HUB/'
#path_ImportD2HUB = 'D:\Temp_JSON\INPUT_D2HUB/genericInfo.txt'
#path_ExportD2HUB = 'D:\Temp_JSON\INPUT_D2HUB/export.xlsx
path_ExportD2HUBcsv = 'D:\Temp_JSON\INPUT_D2HUB/export.csv'
#path_json_D2Hub_info1 = 'D:\Temp_JSON\OUTPUT\genericInfo.json'              #reflet du genericInfo.txt
#path_json_D2Hub_info2 = 'D:\Temp_JSON\OUTPUT\exportD2HubCSV.json'           #reflet de export.csv
path_json_D2Hub_info_total = 'D:\Temp_JSON\INPUT_D2HUB\exportD2HubGlobal.json'   #dictionnaire des équipements declares sur D2Hub 
path_json_D2Hub_equipment_list_raw = 'D:\Temp_JSON\INPUT_D2HUB\D2Hub_equipment_list_raw.json'   #dictionnaire des équipements declares sur D2Hub
path_json_D2Hub_account = 'D:\Temp_JSON\INPUT_D2HUB\Account_list.json'
path_D2Hub_ICAN_HARD_STATUS = 'D:\Temp_JSON\INPUT_D2HUB\ICAN_HARD_STATUS.csv'           
#path_json_D2Hub_item_list = 'D:\Temp_JSON\OUTPUT\D2Hub_Item_list.json'
API_D2HUB_Token = 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJqZGV2YXkiLCJhdXRoIjoiUk9MRV9BRE1JTiIsImV4cCI6MTYxNDA3MDQ1NX0._wCx66P4G_-Ed3oYBkLkTpK96CkvZTM6H4F1l1maNNvwGV68kTWSTeMYtDsTSkkEZKjiScsBsExSDGsAJRzemQ'
API_D2HUB_xsrf_Token = 'bcfa9285-2b1d-406e-830c-5008fd1c0f59'
#API_D2HUB_USER = 'admin'
#API_D2HUB_PASS = 'w,DVBYMbQAz@&6x5HlUFY:bz-z0d7'
API_D2HUB_USER = 'jdevay'
API_D2HUB_PASS = 'Bordel31'


#ATTENTION: ces information peuvent être surchargées par la fonction "maj_configuration" du module Telech_AWS_Json
IMEI_list = ['867322034083212','867322034092015','867322034105809']
#Date_list = ['2020-11-22','2020-11-23','2020-11-24','2020-11-25','2020-11-26','2020-11-27','2020-11-28','2020-11-29','2020-11-30','2020-12-01','2020-12-02','2020-12-03','2020-12-04','2020-12-05','2020-12-06','2020-12-07','2020-12-08','2020-12-09','2020-12-10','2020-12-11']
Date_list = ['2020-12-02','2020-12-03']
Bucket = "/MARKETIP/"
Bucket2 = ""
#Bucket2 = "/OCEAN/"


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

def set_Bucket(Bucket_name):
    global Bucket
    Bucket = Bucket_name

def set_Bucket2(Bucket_name):
    global Bucket2
    Bucket2 = Bucket_name

def set_D2HubToken(auth_Token):
    global API_D2HUB_Token
    API_D2HUB_Token = auth_Token    

def set_D2Hub_xsrf_Token(auth_Token):
    global API_D2HUB_xsrf_Token
    API_D2HUB_xsrf_Token = auth_Token    

if __name__ == '__main__':
    set_Date_list('2020-11-22', '2020-12-11')
    print (Date_list)
    pass
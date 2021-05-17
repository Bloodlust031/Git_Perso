# -*-coding:Latin-1 -*
'''
Created on 30 nov. 2020

@author: blood
'''

import os
import json
import Configuration
import Import_D2HUB_Info
#import os.path 

#commande =  "aws s3 sync s3://ican.processed.d2hub.fr/2020-11-27/MARKETIP/864504031504844/ H:/Boulot/TempDownAWSS3/MARKETIP/864504031504844/"
#os.system("start " + commande)

#strreq = "cmd /c ""echo Téléchargement en cours..... Merci de ne pas fermer cette fenêtre && aws s3 sync s3://ican.processed.d2hub.fr/2020-11-27/MARKETIP/864504031504844/ H:/Boulot/TempDownAWSS3/MARKETIP/864504031504844/ >nul 2>&1"""
#start aws s3 sync s3://ican.processed.d2hub.fr/2020-11-22/MARKETIP/867322034083212 / D:\Temp_JSON\INPUT_Msg/MARKETIP/867322034083212 /
#start aws s3 sync s3://ican.processed.d2hub.fr/2020-11-22/SDPV/867322034083212 / D:\Temp_JSON\INPUT_Msg/MARKETIP/867322034083212 /
#start aws s3 sync s3://ican.processed.d2hub.fr/2020-11-22/UNMATCHED/867322034083212 / D:\Temp_JSON\INPUT_Msg/UNMATCHED/867322034083212 /
#start aws s3 sync s3://ican.invalid.d2hub.fr/2020-11-22//867322034083212 / D:\Temp_JSON\INPUT_Msg/INVALID/867322034083212 /

liste_cmd_bucket = list()
liste_cmd_bucket2 = list()
liste_cmd_UNMATCHED = list()
liste_cmd_invalid = list()

str_Date_list = ['2021-05-01', '2021-05-17']
str_IMEI_list = ["864504031666486","864504039671660","867322038021580","868996033847682","868996033832148","868996033813734","867322038574737","868996033832155","868996033818816","868996033818824","868996033841008","868996033839960","868996033837634","868997035954773","867322034104968","868997035954708","868996033847690","868996033833401","867322034113324","868996033846692","868996033843129","868996033849365","868996033818360","868996033847625","867322038041828","868996033815655","867322038060984","868996033839697","864504039699729","868996033813197","865794031378062","867322034095505","865794031463005","867322038051033","867322034106906","864504031156249","869103026251605","867322038016408","865794031339080","864504039673575","865794031485925","864504031771799","864504039683657","865794031485420","864504031156355","865794031325014","864504031605948","865794031486477","864504031239631","864504031263466","865794031212766","864504031624451","864504039695289","865794031323217","868996033851304","863977036491129","864504031827815","867322034116418","867322038007985","868997035945326","867322038021036","864504031491620","864504031618826","864504031308253","863977036412687","864504031132208","864504031619147","864504031430644"] 

#mes iCANs: '867322034096248','865794031287537'

def Supprim_Event_msg():
    print("Effacement des messages Event")
    current_dict_messages = dict()
    current_dict_messages.clear()
    
    for root, dirs, files in os.walk(Configuration.Chemin_json_msg): 
        for fichier in files: 
            nom_fichier = os.path.join(root, fichier)
            if nom_fichier.endswith(".json"):
                with open(nom_fichier, 'r') as json_file_result:
                    current_dict_messages = json.load(json_file_result)
                pass
                if 'evt' in current_dict_messages:
                    if (str(current_dict_messages['evt']) == '100'):
                        #message event à supprimer
                        if (str(current_dict_messages['eid']) != '43'):
                            os.remove(nom_fichier)
                current_dict_messages.clear()


def gen_liste_cmd():
    global liste_cmd_bucket
    global liste_cmd_bucket2
    global liste_cmd_UNMATCHED
    global liste_cmd_invalid
    liste_cmd_bucket.clear()
    liste_cmd_bucket2.clear()
    liste_cmd_UNMATCHED.clear()
    liste_cmd_invalid.clear()
    
    efface_BatTemp()
    for imei in Configuration.IMEI_list:
        bucket = "/" + Import_D2HUB_Info.get_bucket_IMEI(imei) + "/"
        for jour in Configuration.Date_list:
            str_temp = "aws s3 sync s3://ican.processed.d2hub.fr/" + jour + bucket + imei +  "/ " + Configuration.Chemin_json_msg + bucket + imei + "/"
            liste_cmd_bucket.append(str_temp)
            #print(str_temp)
            str_temp = "aws s3 sync s3://ican.processed.d2hub.fr/" + jour + "/UNMATCHED/" + imei +  "/ " + Configuration.Chemin_json_msg + "/UNMATCHED/" + imei + "/"
            liste_cmd_UNMATCHED.append(str_temp)
            str_temp = "aws s3 sync s3://ican.invalid.d2hub.fr/" + jour + "/" + imei +  "/ " + Configuration.Chemin_json_msg + "/INVALID/" + imei + "/"
            liste_cmd_invalid.append(str_temp)
    
    i = 0
    nb_req = len(liste_cmd_bucket)
    with open(Configuration.Chemin_json_BatTemp + '/bat_cmd_bucket.bat', 'w') as batfile:
        for str_temp in liste_cmd_bucket:
            i+=1
            batfile.write("echo Commande " + str(i) + " / " + str(nb_req) + "\n")
            batfile.write(str_temp + "\n")
        batfile.write("exit\n")
    pass
    i = 0
    nb_req = len(liste_cmd_UNMATCHED)
    with open(Configuration.Chemin_json_BatTemp + '/bat_cmd_UNMATCHED.bat', 'w') as batfile:
        for str_temp in liste_cmd_UNMATCHED:
            i+=1
            batfile.write("echo Commande " + str(i) + " / " + str(nb_req) + "\n")
            batfile.write(str_temp + "\n")
        batfile.write("exit\n")
    pass
    i = 0
    nb_req = len(liste_cmd_invalid)
    with open(Configuration.Chemin_json_BatTemp + '/bat_cmd_invalid.bat', 'w') as batfile:
        for str_temp in liste_cmd_invalid:
            i+=1
            batfile.write("echo Commande " + str(i) + " / " + str(nb_req) + "\n")
            batfile.write(str_temp + "\n")
        batfile.write("exit\n")
    pass


def execute_cmd():
    str_cmd = "start " + Configuration.Chemin_json_BatTemp + '/bat_cmd_bucket.bat'
    os.system(str_cmd)
    str_cmd = "start " + Configuration.Chemin_json_BatTemp + '/bat_cmd_UNMATCHED.bat'
    os.system(str_cmd)
    str_cmd = "start " + Configuration.Chemin_json_BatTemp + '/bat_cmd_invalid.bat'
    os.system(str_cmd)

 
def efface_old_msg():
    #effacement des messages précédemment téléchargés.
    bretour = False
    txt_input = input("Voulez vous effacer les messages précédents (O pour oui) ?")
    try:
        if ((txt_input[0] == "O") or (txt_input[0] == "o")):
            bretour = True
    except:
        bretour = False
    if bretour:
        for root, dirs, files in os.walk(Configuration.Chemin_json_msg): 
            for fichier in files: 
                nom_fichier = os.path.join(root, fichier)
                os.remove(nom_fichier)
                
def efface_BatTemp():
    #effacement des .bat précédents
    for root, dirs, files in os.walk(Configuration.Chemin_json_BatTemp): 
        for fichier in files: 
            nom_fichier = os.path.join(root, fichier)
            os.remove(nom_fichier)


def telech(Date_list = [], IMEI_list = []):
    Configuration.init_config()
    Configuration.verif_create_dossier(Configuration.Chemin_json_msg)
    Configuration.verif_create_dossier(Configuration.Chemin_json_BatTemp)
    
    if len(Date_list) == 1:
        Configuration.set_Date_list(Date_list[0], "0")  #on n'a pas de date de fin-> on va juste télécharger les messages de ce jour
    if len(Date_list) > 1:
        Configuration.set_Date_list(Date_list[0], Date_list[1]) #on prend tous les jours entre ces 2 dates
    if len(IMEI_list)>0:
        Configuration.set_IMEI_List(IMEI_list)
    efface_old_msg()
    gen_liste_cmd()
    execute_cmd()
        
if __name__ == '__main__':
    
    Configuration.init_config()
    telech(Date_list = str_Date_list, IMEI_list = str_IMEI_list)
    
    bretour = False
    txt_input = input("Voulez vous supprimer les messages Event (O pour oui) ?")
    try:
        if ((txt_input[0] == "O") or (txt_input[0] == "o")):
            bretour = True
    except:
        bretour = False
    if bretour:
        Supprim_Event_msg()

    
    pass
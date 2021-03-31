# -*-coding:Latin-1 -*
'''
Created on 30 nov. 2020

@author: blood
'''

import os
import json
import Configuration
import Import_D2HUB_Info
import sys
import shutil
import glob 
import os.path 

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

str_Date_list = ['2021-03-01', '2021-03-31']
str_IMEI_list = ['868996033842196']

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
                        if (str(current_dict_messages['eid']) != '2A'):
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
    
    for imei in Configuration.IMEI_list:
        bucket = "/" + Import_D2HUB_Info.get_bucket_IMEI(imei) + "/"
        for jour in Configuration.Date_list:
            str_temp = "start aws s3 sync s3://ican.processed.d2hub.fr/" + jour + bucket + imei +  "/ " + Configuration.Chemin_json_msg + bucket + imei + "/"
            liste_cmd_bucket.append(str_temp)
            #print(str_temp)
            str_temp = "start aws s3 sync s3://ican.processed.d2hub.fr/" + jour + "/UNMATCHED/" + imei +  "/ " + Configuration.Chemin_json_msg + "/UNMATCHED/" + imei + "/"
            liste_cmd_UNMATCHED.append(str_temp)
            str_temp = "start aws s3 sync s3://ican.invalid.d2hub.fr/" + jour + "/" + imei +  "/ " + Configuration.Chemin_json_msg + "/INVALID/" + imei + "/"
            liste_cmd_invalid.append(str_temp)

def execute_cmd():
    nb_req = len(liste_cmd_bucket) + len(liste_cmd_bucket2) + len(liste_cmd_UNMATCHED) + len(liste_cmd_invalid)
    i = 0
    for str_cmd in liste_cmd_invalid:
        i+=1
        os.system(str_cmd)
        print ("Commande " + str(i) + " / " + str(nb_req))
    for str_cmd in liste_cmd_UNMATCHED:
        i+=1
        os.system(str_cmd)
        print ("Commande " + str(i) + " / " + str(nb_req))
    for str_cmd in liste_cmd_bucket:
        i+=1
        os.system(str_cmd)
        print ("Commande " + str(i) + " / " + str(nb_req))
    for str_cmd in liste_cmd_bucket2:
        i+=1
        os.system(str_cmd)
        print ("Commande " + str(i) + " / " + str(nb_req))
 
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


def telech(Date_list = [], IMEI_list = []):
    Configuration.init_config()
    Configuration.verif_create_dossier(Configuration.Chemin_json_msg)
    
    if len(Date_list) == 1:
        Configuration.set_Date_list(Date_list[0], "0")  #on n'a pas de date de fin-> on va juste télécharger les messages de ce jour
    if len(Date_list) > 1:
        Configuration.set_Date_list(Date_list[0], Date_list[1]) #on prend tous les jours entre ces 2 dates
    if len(IMEI_list)>0:
        Configuration.set_IMEI_List(IMEI_list)
    efface_old_msg()
    gen_liste_cmd()
    execute_cmd()
        
'''def move_over(src_dir, dest_dir):
    fileList = os.listdir(src_dir)
    for i in fileList:
        src = os.path.join(src_dir, i)
        dest = os.path.join(dest_dir, i)
        if os.path.exists(dest):
            if os.path.isdir(dest):
                move_over(src, dest)
                continue
            else:
                os.remove(dest)
        shutil.move(src, dest_dir)        
        
def deplacement():
    
    bretour = False
    txt_input = input("Voulez vous déplacer les fichiers pour les extraire avec l'outil Excel ?")
    try:
        if ((txt_input[0] == "O") or (txt_input[0] == "o")):
            bretour = True
    except:
        bretour = False
        
    if bretour:
        l = glob.glob(Configuration.Chemin_json + '/*') 
        for nom_dossier in l: 
            if os.path.isdir(nom_dossier): 
                #print (nom_dossier)
                nom = nom_dossier[len(Configuration.Chemin_json)+1:]
                #print (nom)
                if (nom != Configuration.Chemin_json_Outil_iCAN):
                    new_dossier = Configuration.Chemin_json + "/" + Configuration.Chemin_json_Outil_iCAN + "/" + nom
                    #new_dossier = Configuration.Chemin_json + "/" + Configuration.Chemin_json_Outil_iCAN
                    #print (new_dossier)
                    #shutil.copy(nom_dossier, new_dossier)
                    if os.path.isdir(new_dossier): 
                        #print("le dossier de destination existe déjà.")
                        fileList = os.listdir(nom_dossier)
                        for i in fileList:
                            src = os.path.join(nom_dossier, i)
                            dest = os.path.join(new_dossier, i)
                            shutil.move(src, dest)   
                        #os.remove(nom_dossier)     
                    else:
                        #print("le dossier de destination n'existe pas.")
                        shutil.move(nom_dossier, new_dossier)'''
    

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

    #deplacement()        
    
    pass
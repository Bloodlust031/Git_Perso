# -*-coding:Latin-1 -*
'''
Created on 30 nov. 2020

@author: blood
'''

import os
import Configuration
import csv
import time
import json
import Boite_Outils

#commande =  "start aws s3 sync s3://ican.failure.d2hub.fr/2021-03-29/ D:\Temp_JSON\INPUT_Msg\Failure"

liste_cmd = list()
str_Date_list = ['2021-04-13', '2021-04-13']
list_fail = list()


def gen_liste_cmd():
    global liste_cmd
    liste_cmd.clear()
    
    for jour in Configuration.Date_list:
        str_temp = "start aws s3 sync s3://ican.failure.d2hub.fr/" + jour + "/ " + Configuration.Chemin_json_failure
        liste_cmd.append(str_temp)


def execute_cmd():
    nb_req = len(liste_cmd)
    i = 0
    for str_cmd in liste_cmd:
        i+=1
        os.system(str_cmd)
        print ("Commande " + str(i) + " / " + str(nb_req))
 

def telech(Date_list = []):
    Configuration.init_config()
    Configuration.verif_create_dossier(Configuration.Chemin_json_failure)
    
    if len(Date_list) == 1:
        Configuration.set_Date_list(Date_list[0], "0")  #on n'a pas de date de fin-> on va juste télécharger les messages de ce jour
    if len(Date_list) > 1:
        Configuration.set_Date_list(Date_list[0], Date_list[1]) #on prend tous les jours entre ces 2 dates
    gen_liste_cmd()
    execute_cmd()
         
         
@Boite_Outils.print_temps
def extract_failure():
    global list_fail
    
    liste_fichier=[] 
    list_fail.clear()
    fail_dict = dict()
    
    with open(Configuration.path_json_D2Hub_info_total) as json_file3:
        equipment_dico = json.load(json_file3)    
    
    fail_stat_dict = dict() 
    fail_stat_dict["NbFailure"] = 0
    fail_stat_dict["IMEI List"] = dict()
    
    for root, dirs, files in os.walk(Configuration.Chemin_json_failure): 
        for i in files: 
            liste_fichier.append(os.path.join(root, i))
    liste_fichier.sort()    #Les messages sont traités dans l'ordre chronologique.
    
    for nom_fic in liste_fichier:
        fail_stat_dict["NbFailure"] += 1
        fail_dict.clear()
        fail_dict["Fichier"] = nom_fic
        fail_dict["Date"] = time.ctime(os.path.getmtime(nom_fic))
        strIMEI = ""
        with open(nom_fic, mode='rb') as file:
            fileContent = file.read()
            taille = len(fileContent)
            for i in range(0, taille-22):
                if((fileContent[i] == 0) and (fileContent[i+1] == 153) and (fileContent[i+2] == 0) and (fileContent[i+3] == 24) and (fileContent[i+4] == 0) and (fileContent[i+5] == 15) and (fileContent[i+6] == 0)):
                    for j in range(0,15):
                        strIMEI =  strIMEI + chr(fileContent[i+7+j])
                    break;
            fail_dict["IMEI"] = strIMEI
            if len(strIMEI) >= 15:
                if strIMEI in fail_stat_dict["IMEI List"]:
                    fail_stat_dict["IMEI List"][strIMEI]["nb"] += 1
                else:
                    fail_stat_dict["IMEI List"][strIMEI] = dict()
                    fail_stat_dict["IMEI List"][strIMEI]["nb"] = 1
                    fail_stat_dict["IMEI List"][strIMEI]["IMEI"] = strIMEI
            if strIMEI in equipment_dico:
                fail_stat_dict["IMEI List"][strIMEI]["FW"] = equipment_dico[strIMEI]["Item_FW"]
                fail_stat_dict["IMEI List"][strIMEI]["Account"] = equipment_dico[strIMEI]["Account_Name"]
                fail_dict["FW"] = equipment_dico[strIMEI]["Item_FW"]
                fail_dict["Account"] = equipment_dico[strIMEI]["Account_Name"]

            
        list_fail.append(fail_dict.copy())
    
    with open(Configuration.Chemin_json_failure + "\Failure.csv", 'w', newline='') as csvfile:
        fieldnames = ['Fichier', 'Date','IMEI',"FW","Account"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,extrasaction='ignore',delimiter=";")
        writer.writeheader()
        for item in list_fail:
            writer.writerow(item)
    pass
    with open(Configuration.Chemin_json_failure + "\Failure.json", 'w') as json_file_result:
        json.dump(fail_stat_dict, json_file_result, indent=4)
    pass
    

if __name__ == '__main__':
    telech(Date_list = str_Date_list)
    os.system("pause") # On met le programme en pause pour Ã©viter qu'il ne se referme (Windows)
    extract_failure()
    pass
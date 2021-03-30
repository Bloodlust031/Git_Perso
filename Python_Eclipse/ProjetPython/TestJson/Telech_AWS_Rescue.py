# -*-coding:Latin-1 -*
'''
Created on 30 nov. 2020

@author: blood
'''

import os
import Configuration
#import time
import csv
import datetime

#aws s3 sync s3://ican.rescue.d2hub.fr/ D:\temp\Rescue\

liste_cmd = list()


def gen_liste_cmd():
    global liste_cmd
    liste_cmd.clear()
    str_temp = "start aws s3 sync s3://ican.rescue.d2hub.fr/ " + Configuration.Chemin_json_rescue
    liste_cmd.append(str_temp)


def execute_cmd():
    nb_req = len(liste_cmd)
    i = 0
    for str_cmd in liste_cmd:
        i+=1
        os.system(str_cmd)
        print ("Commande " + str(i) + " / " + str(nb_req))
 
def telech():
    Configuration.init_config()
    Configuration.verif_create_dossier(Configuration.Chemin_json_rescue)
    gen_liste_cmd()
    execute_cmd()
    
def Extract_rescue():
    extract_list = list()
    extract_list.clear()
    liste_fichier=[] 
    for root, dirs, files in os.walk(Configuration.Chemin_json_rescue): 
        for i in files: 
            if i.endswith(".bin"):
                liste_fichier.append(os.path.join(root, i))
                
                
                
    liste_fichier.sort()    #Les messages sont traités dans l'ordre chronologique.
    for nom_fic in liste_fichier:
        current_msg = dict()
        current_msg.clear()
        current_msg["nomfic"] = nom_fic
        current_msg["date_fic"] = datetime.datetime.fromtimestamp(os.path.getmtime(nom_fic))
        str_temp = nom_fic[-32:]
        str_temp = str_temp[0:15]
        current_msg["IMEI"] = str_temp
        print (str_temp)
        extract_list.append(dict(current_msg))
    
    print(extract_list)

    with open(Configuration.Chemin_json_rescue + "/OTA_Rescue.csv", 'w', newline='') as csvfile:
        fieldnames = ['nomfic', 'date_fic','IMEI']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,extrasaction='ignore',delimiter=";")
        writer.writeheader()
        for msg in extract_list:
            writer.writerow(msg)
    pass
    

if __name__ == '__main__':
    telech()
    Extract_rescue()
    pass
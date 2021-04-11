# -*-coding:Latin-1 -*
'''
Created on 30 nov. 2020

@author: blood
'''

import os
import Configuration

#commande =  "start aws s3 sync s3://ican.failure.d2hub.fr/2021-03-29/ D:\Temp_JSON\INPUT_Msg\Failure"

liste_cmd = list()
str_Date_list = ['2021-03-15', '2021-04-01']


def gen_liste_cmd():
    global liste_cmd
    liste_cmd.clear()
    
    for jour in Configuration.Date_list:
        str_temp = "start aws s3 sync s3://ican.reco.d2hub.fr/" + jour + "/ " + Configuration.Chemin_json_reco
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
    Configuration.verif_create_dossier(Configuration.Chemin_json_reco)
    
    if len(Date_list) == 1:
        Configuration.set_Date_list(Date_list[0], "0")  #on n'a pas de date de fin-> on va juste télécharger les messages de ce jour
    if len(Date_list) > 1:
        Configuration.set_Date_list(Date_list[0], Date_list[1]) #on prend tous les jours entre ces 2 dates
    gen_liste_cmd()
    execute_cmd()
         

if __name__ == '__main__':
    
    telech(Date_list = str_Date_list)
    
    pass
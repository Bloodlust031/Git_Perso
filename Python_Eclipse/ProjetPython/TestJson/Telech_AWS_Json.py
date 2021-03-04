# -*-coding:Latin-1 -*
'''
Created on 30 nov. 2020

@author: blood
'''

import os
import json
import Configuration
import Import_D2HUB_Info

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

def maj_configuration():
    Configuration.set_Date_list('2021-02-08', '2021-02-12')
    #Configuration.set_IMEI_List(['864504031504844','867322034117739','868996033820754']) #Tracking only
    #Configuration.set_IMEI_List(['867322038021531','867322034091553','864504031784453','867322034104158'])  #test GSM - TrackingOnly

    #Configuration.set_IMEI_List(['867322034083212','867322034092015','867322034105809','867322038019717']) #Clio5 essence
    Configuration.set_IMEI_List(['864504031783646','864504031784438','864504031308253','869103026381394','864504039629882','864504039684291','864504031769983'])
    #Configuration.set_Bucket2("/OCEAN/")
    #Configuration.set_IMEI_List(['867322034097105'])
    
def Supprim_Event_msg():
    print("Effacement des messages Event")
    current_dict_messages = dict()
    current_dict_messages.clear()
    
    for root, dirs, files in os.walk(Configuration.Chemin_json): 
        for fichier in files: 
            nom_fichier = os.path.join(root, fichier)
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
            str_temp = "start aws s3 sync s3://ican.processed.d2hub.fr/" + jour + bucket + imei +  "/ " + Configuration.Chemin_json + bucket + imei + "/"
            liste_cmd_bucket.append(str_temp)
            #print(str_temp)
            str_temp = "start aws s3 sync s3://ican.processed.d2hub.fr/" + jour + "/UNMATCHED/" + imei +  "/ " + Configuration.Chemin_json + "/UNMATCHED/" + imei + "/"
            liste_cmd_UNMATCHED.append(str_temp)
            str_temp = "start aws s3 sync s3://ican.invalid.d2hub.fr/" + jour + "/" + imei +  "/ " + Configuration.Chemin_json + "/INVALID/" + imei + "/"
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
    

if __name__ == '__main__':
    maj_configuration()
    gen_liste_cmd()
    execute_cmd()
    
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
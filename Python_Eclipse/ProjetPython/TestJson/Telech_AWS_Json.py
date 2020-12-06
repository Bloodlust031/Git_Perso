# -*-coding:Latin-1 -*
'''
Created on 30 nov. 2020

@author: blood
'''
import os
import Configuration

#commande =  "aws s3 sync s3://ican.processed.d2hub.fr/2020-11-27/MARKETIP/864504031504844/ H:/Boulot/TempDownAWSS3/MARKETIP/864504031504844/"
#os.system("start " + commande)

#strreq = "cmd /c ""echo Téléchargement en cours..... Merci de ne pas fermer cette fenêtre && aws s3 sync s3://ican.processed.d2hub.fr/2020-11-27/MARKETIP/864504031504844/ H:/Boulot/TempDownAWSS3/MARKETIP/864504031504844/ >nul 2>&1"""

liste_cmd_bucket = list()
liste_cmd_bucket2 = list()
liste_cmd_UNMATCHED = list()
liste_cmd_invalid = list()

def gen_liste_cmd():
    global liste_cmd_bucket
    global liste_cmd_bucket2
    global liste_cmd_UNMATCHED
    global liste_cmd_invalid
    liste_cmd_bucket.clear()
    liste_cmd_bucket2.clear()
    liste_cmd_UNMATCHED.clear()
    liste_cmd_invalid.clear()
    for jour in Configuration.Date_list:
        for imei in Configuration.IMEI_list:
            str_temp = "start aws s3 sync s3://ican.processed.d2hub.fr/" + jour + Configuration.Bucket + imei +  "/ " + Configuration.Chemin_json + Configuration.Bucket + imei + "/"
            liste_cmd_bucket.append(str_temp)
            if (len(Configuration.Bucket2) > 1):
                str_temp = "start aws s3 sync s3://ican.processed.d2hub.fr/" + jour + Configuration.Bucket2 + imei +  "/ " + Configuration.Chemin_json + Configuration.Bucket + imei + "/"
                liste_cmd_bucket2.append(str_temp)
            str_temp = "start aws s3 sync s3://ican.processed.d2hub.fr/" + jour + "/UNMATCHED/" + imei +  "/ " + Configuration.Chemin_json + "/UNMATCHED/" + imei + "/"
            liste_cmd_UNMATCHED.append(str_temp)
            str_temp = "start aws s3 sync s3://ican.invalid.d2hub.fr/" + jour + "//" + imei +  "/ " + Configuration.Chemin_json + "/INVALID/" + imei + "/"
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
    gen_liste_cmd()
    execute_cmd()
    
    pass
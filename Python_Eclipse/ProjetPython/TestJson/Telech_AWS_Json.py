# -*-coding:Latin-1 -*
'''
Created on 30 nov. 2020

@author: blood
'''
import os
import Configuration

#commande =  "aws s3 sync s3://ican.processed.d2hub.fr/2020-11-27/MARKETIP/864504031504844/ H:/Boulot/TempDownAWSS3/MARKETIP/864504031504844/"
#os.system("start " + commande)

IMEI_list = ['864504031504844','868996033820754']
Date_list = ['2020-11-27','2020-11-28','2020-11-29','2020-11-30']
Bucket = "/MARKETIP/"

#strreq = "cmd /c ""echo Téléchargement en cours..... Merci de ne pas fermer cette fenêtre && aws s3 sync s3://ican.processed.d2hub.fr/2020-11-27/MARKETIP/864504031504844/ H:/Boulot/TempDownAWSS3/MARKETIP/864504031504844/ >nul 2>&1"""

liste_cmd = list()

def gen_liste_cmd():
    global liste_cmd
    liste_cmd.clear()
    for jour in Date_list:
        for imei in IMEI_list:
            str_temp = "start aws s3 sync s3://ican.processed.d2hub.fr/" + jour + Bucket + imei +  "/ " + Configuration.Chemin_json + Bucket + imei + "/"
            liste_cmd.append(str_temp)
            str_temp = "start aws s3 sync s3://ican.processed.d2hub.fr/" + jour + "/UNMATCHED/" + imei +  "/ " + Configuration.Chemin_json + "/UNMATCHED/" + imei + "/"
            liste_cmd.append(str_temp)

if __name__ == '__main__':
    gen_liste_cmd()
    for str_cmd in liste_cmd:
        os.system(str_cmd)
        print (str_cmd)
    
    pass
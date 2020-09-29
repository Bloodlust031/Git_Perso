# -*-coding:Latin-1 -*
'''
Created on 29 sept. 2020

@author: jdevay
'''

import os
import json
import time

#chemin_base = 'H:/Boulot/Boulot Jeje/Main/Ican/Extract_traces_FTP/TempDownAWSS3/'
#chemin_base = 'D:/Boulot/Main/Ican/Extract_traces_FTP/TempDownAWSS3/'
chemin_base = 'D:/temp/DWLD msg Bastides/'
fichier_log = 'D:/temp/log_tata.txt'

def listdirectory(path): 
    liste_fichier=[] 
    for root, dirs, files in os.walk(path): 
        for i in files: 
            liste_fichier.append(os.path.join(root, i)) 
    return liste_fichier

def traite_1_1fic(path): 
    ecart_reception = 0
    #print("fichier en cours: ", path)
    #print("fichier en cours: ", os.path.basename(path))
    with open(nom_fic) as json_file:
        data = json.load(json_file)
        #print(data['tim'], data['int'])
        ecart_reception = (data['int']-data['tim'])/1000
        #print("Ecart r�ception: ", ecart_reception)
        #print(data['evt'], data['eid'])
        #print(os.path.basename(path), data['ime'], data['tim'], data['int'], ecart_reception, data['evt'], data['eid'])
        #chaine = str(os.path.basename(path))+ " " + str(data['ime'])+ " " + str(data['tim'])+ " " + str(data['int'])+ " " + str(ecart_reception)+ " " + str(data['evt'])+ " " + str(data['eid'])+ '\n'
        chaine = str(os.path.basename(path))+ "|" + str(data['ime'])+ "|" + str(ecart_reception)+ "|" + str(data['evt'])+ "|" + str(data['eid'])+ '\n'
        f.write(chaine)

if __name__ == "__main__":
    print("coucou")
    time1 = time.process_time()
    liste_fichiers = listdirectory(chemin_base)
    nb_fic = 0
    
    f= open(fichier_log, 'w')
    f.write("Nom_Fic|IMEI|Delai|Msg_Type|Event_ID\n")
    for nom_fic in liste_fichiers:
        traite_1_1fic(nom_fic)
        nb_fic = nb_fic+1
        #f.write(nom_fic)
        #print(nom_fic)
        #with open(nom_fic) as json_file:
        #    data = json.load(json_file)    
        
    f.closed

    time2 = time.process_time()
    print( time2-time1, "secondes d'executions")
    print (nb_fic, "fichiers analyses")
    
    os.system("pause") # On met le programme en pause pour éviter qu'il ne se referme (Windows)
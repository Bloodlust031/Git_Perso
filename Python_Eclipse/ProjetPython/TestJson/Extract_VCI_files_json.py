# -*-coding:Latin-1 -*
'''
Created on 6 nov. 2020

@author: blood
'''
import os
import json
import time

chemin_base = 'H:/Boulot/Boulot Jeje/Main/Ican/Extract_traces_FTP/TempDownAWSS3/'
#chemin_base = 'D:/Boulot/Main/Ican/Extract_traces_FTP/TempDownAWSS3/'
#chemin_base = 'D:/temp/DWLD msg Bastides/'
fichier_log = 'D:/temp/log_tata.txt'
fichier_log = 'D:/temp/JsonOut.json'
path_sortie = 'D:/temp/Msg_'

liste_fichiers = []
current_IMEI = ''


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
    current_msg = {}
    with open(nom_fic) as json_file2:
        data = json.load(json_file2)
        #print(data['tim'], data['int'])
        ecart_reception = (data['int']-data['tim'])/1000
        #print("Ecart r�ception: ", ecart_reception)
        #print(data['evt'], data['eid'])
        #print(os.path.basename(path), data['ime'], data['tim'], data['int'], ecart_reception, data['evt'], data['eid'])
        #chaine = str(os.path.basename(path))+ " " + str(data['ime'])+ " " + str(data['tim'])+ " " + str(data['int'])+ " " + str(ecart_reception)+ " " + str(data['evt'])+ " " + str(data['eid'])+ '\n'
        chaine = str(os.path.basename(path))+ "|" + str(data['ime'])+ "|" + str(ecart_reception)+ "|" + str(data['evt'])+ "|" + str(data['eid'])+ '\n'
        
        
        
        f.write(chaine)

def ecriture_resultats(path, current_IMEI):
    global liste_fichiers
    if(len(liste_fichiers)>0):
        nom_fic = path + strIMEI + '.json'
        list_msg = []
        with open(nom_fic, 'r') as json_file_result:
            list_msg = json.load(json_file_result)
        pass
        list_msg.extend(liste_fichiers)
        with open(nom_fic, 'w') as json_file_result:
            json.dump(list_msg, json_file_result)
        pass
    liste_fichiers.clear()


if __name__ == "__main__":
    print("coucou")
    time1 = time.process_time()
    liste_fichiers = listdirectory(chemin_base)
    nb_fic = 0
    
    for nom_fic in liste_fichiers:
        traite_1_1fic(nom_fic)
        nb_fic = nb_fic+1
    
    ecriture_resultats(path_sortie, current_IMEI)

    time2 = time.process_time()
    print( time2-time1, "secondes d'executions")
    print (nb_fic, "fichiers analyses")
    
    os.system("pause") # On met le programme en pause pour éviter qu'il ne se referme (Windows)
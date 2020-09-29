# -*-coding:Latin-1 -*

import Boite_outils
import os
import json

#chemin_base = 'H:/Boulot/Boulot Jeje/Main/Ican/Extract_traces_FTP/TempDownAWSS3/'
chemin_base = 'D:/Boulot/Main/Ican/Extract_traces_FTP/TempDownAWSS3/'

def listdirectory(path): 
    liste_fichier=[] 
    for root, dirs, files in os.walk(path): 
        for i in files: 
            liste_fichier.append(os.path.join(root, i)) 
    return liste_fichier

def traite_1_1fic(path): 
    ecart_reception = 0
    print("fichier en cours: ", path)
    with open(nom_fic) as json_file:
        data = json.load(json_file)
        print(data['tim'], data['int'])
        ecart_reception = (data['int']-data['tim'])/1000
        print("Ecart réception: ", ecart_reception)
		#print(data['evt'], data['eid'])

if __name__ == "__main__":
    print("coucou")
    
    liste_fichiers = listdirectory(chemin_base)

    for nom_fic in liste_fichiers:
        traite_1_1fic(nom_fic)
        #print(nom_fic)
        #with open(nom_fic) as json_file:
        #    data = json.load(json_file)    
    
#    with open('H:/Boulot/Boulot Jeje/Main/Ican/Extract_traces_FTP/TempDownAWSS3/MARKETIP/867322034090829/1587561083000-a0a6da01-4d74-4968-bac1-4239060ae6fd.json') as json_file:
#        data = json.load(json_file)    
    
    # On met le programme en pause pour Ã©viter qu'il ne se referme (Windows)
    os.system("pause")
    
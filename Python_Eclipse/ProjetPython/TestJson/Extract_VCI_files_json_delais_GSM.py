# -*-coding:Latin-1 -*
'''
Created on 6 nov. 2020

@author: blood
'''
import os
import json
import time
import fnmatch
import Boite_Outils
import Configuration
import csv
from datetime import datetime
import Telech_AWS_Json


prefixe_nom_sortie = 'Msg_IMEI_'

current_IMEI = str('rien')
current_dict_messages = dict()
global_log_dict = dict()
start_time = 0
end_time = 0
#str_IMEI_List = ['864504031784453','867322038021531','867322034091553','867322034104158','862010039042896','864504031167089','867322034107201']  #test GSM - TrackingOnly
str_IMEI_List = ['867322038021531','867322034091553','868996033829870','867322034104158','867322034107201']  #test GSM - TrackingOnly

def listdirectory(path): 
    liste_fichier=[] 
    #for root, dirs, files in os.walk(path):
    for root, dirs, files in os.walk(path): 
        for i in files:
            if i.endswith(".json"):
                liste_fichier.append(os.path.join(root, i))
    liste_fichier.sort()    #Les messages sont traités dans l'ordre chronologique.
    #liste_fichier.sort(reverse = True)    #Les messages sont traités dans l'ordre anti-chronologique.
    return liste_fichier


def traite_1_1fic(nom_fic_msg): 
    #print("fichier en cours: ", nom_fic_msg)
    global current_dict_messages
    current_msg = dict()
    
    with open(nom_fic_msg) as json_file2:
        data = json.load(json_file2)
            
        #traitement du nom du fichier
        current_msg['NomFichier_Msg'] = os.path.basename(nom_fic_msg)
        #str_temp = str(os.path.dirname(nom_fic_msg))
        #str_temp = str_temp.replace("\\","/")
        #current_msg['AdresseFichier_Msg'] = str_temp
            
        #incrémentation des compteurs
        global_log_dict['NB_Msg']+=1
        #remplissage du dictionnaire du message courrant
        current_msg['IMEI'] = str(data['ime'])
        current_msg['Timestamp_Reception'] = str(data['int'])
        current_msg['Timestamp_Generation'] = str(data['tim'])
        current_msg['Date_Reception'] = str(datetime.fromtimestamp(int(data['int']) / 1000))
        current_msg['Date_Generation'] = str(datetime.fromtimestamp(int(data['tim']) / 1000))
        current_msg['Delai_GSM'] = '{:.0f}'.format((data['int']-data['tim'])/1000)
        current_msg['VIN'] = str(data['vin'])
        current_msg['Msg_Size'] = '{:.0f}'.format((len(data['bin']))/2)

        if (str(data['evt']) == "100"):
            current_msg['Typ_Msg'] = 'Event'
        else:
            if (str(data['evt']) == "102"):
                current_msg['Typ_Msg'] = 'Journey'
            else:
                current_msg['Typ_Msg'] = 'Other'

        if (str(data['eid']) == "ff"):
            current_msg['Typ_Evt'] = "-"
        else:
            current_msg['Typ_Evt'] = str(data['eid'])

        if "20033" in data['cnt']:
            current_msg['FW'] = data['cnt']['20033']
        
        i = -1
        if "20046" in data['cnt']:
            i = int(data['cnt']['20046'])
        else:
            if "19" in data['cnt']:
                i = int(data['cnt']['19'])
        if (i>=0):
            i = i/1000
            current_msg['Odometre'] = str(i) + " km"

        if "2010" in data['cnt']:
            i = int(data['cnt']['2010'])
            i = i / 1000
            current_msg['Distance_parcourue'] = str(i) + " km"

        if "20092" in data['cnt']:
            current_msg['Journey_Nb'] = data['cnt']['20092']
        if "20093" in data['cnt']:
            current_msg['Msg_Nb'] = data['cnt']['20093']
            
        #GPS
        if "204" in data['cnt']:
            current_msg['GPS_Latitude'] = data['cnt']['204']
        else:
            if "101" in data['cnt']:
                current_msg['GPS_Latitude'] = data['cnt']['101']
        if "205" in data['cnt']:
            current_msg['GPS_Longitude'] = data['cnt']['205']
        else:
            if "102" in data['cnt']:
                current_msg['GPS_Longitude'] = data['cnt']['102']
        if (('GPS_Latitude' in current_msg) and ('GPS_Longitude' in current_msg)): 
            current_msg['http_link'] = 'https://www.google.fr/maps/search/' + str(current_msg['GPS_Latitude']) + "," + str(current_msg['GPS_Longitude']) + "/@" + str(current_msg['GPS_Latitude']) + "," + str(current_msg['GPS_Longitude']) + ",19z?hl=fr"
        
        if "20229" in data['cnt']:
            current_msg['ICCID'] = data['cnt']['20229']
        if "20230" in data['cnt']:
            current_msg['IMSI'] = data['cnt']['20230']
        if "20032" in data['cnt']:
            current_msg['Serial'] = data['cnt']['20032']
        
        #ajout du message courrant dans la liste de messages du boitier
        global_log_dict["Msg_list"].append(dict(current_msg))
    current_msg.clear()

def get_nom_fic_sortie(extension):
    nom = Configuration.path_sortie + '__Global_log_delai_GSM.' + extension
    return nom
    
def close_global_log_dict():
    global global_log_dict
    global start_time
    global end_time
    end_time = time.process_time()
    global_log_dict['End Process Time'] = time.asctime(time.localtime())
    global_log_dict['Process Duration'] = end_time - start_time

    nom_fic = get_nom_fic_sortie('json')
    with open(nom_fic, 'w') as json_file_result:
        json.dump(global_log_dict, json_file_result)
    pass

def ecriture_csv():
    nom_fic = get_nom_fic_sortie('csv')
    with open(nom_fic, 'w', newline='') as csvfile:
        fieldnames = ['http_link', 'NomFichier_Msg','IMEI', 'VIN', 'Date_Reception', 'Date_Generation', 'Delai_GSM', 'Typ_Msg', 'Typ_Evt', 'Msg_Size', 'FW', 'Odometre', 'Distance_parcourue', 'Journey_Nb', 'Msg_Nb', 'GPS_Latitude', 'GPS_Longitude', 'Timestamp_Reception', 'Timestamp_Generation', 'ICCID', 'IMSI', 'Serial']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=";")

        writer.writeheader()
        for msg in global_log_dict["Msg_list"]:
            writer.writerow(msg)
    pass

if __name__ == "__main__":
    print("coucou")
    
    Configuration.init_config()
    
    print("Lancement du Téléchargement")
    Telech_AWS_Json.telech(Date_list = ['2021-04-08', '2021-04-08'], IMEI_list = str_IMEI_List)
    os.system("pause") # On met le programme en pause pour Ã©viter qu'il ne se referme (Windows)
    
    liste_fichiers = list()
    global_log_dict['NB_Msg'] = 0
    global_log_dict["Msg_list"] = list() 
    
    liste_fichiers = listdirectory(Configuration.Chemin_json_msg)
    nb_fic = 0
    
    
    print(str(len(liste_fichiers)) + " fichiers a analyser")
    
    for nom_fic in liste_fichiers:
        #print(nom_fic)
        traite_1_1fic(nom_fic)
        nb_fic = nb_fic+1
    
    ecriture_csv()
    close_global_log_dict()
    
    print( end_time-start_time, "secondes d'executions")
    print(nb_fic, "fichiers analyses")
    
    #print(global_log_dict)
    
    os.system("pause") # On met le programme en pause pour Ã©viter qu'il ne se referme (Windows)
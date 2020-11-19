# -*-coding:Latin-1 -*
'''
Created on 6 nov. 2020

@author: blood
'''
import os
import json
import time



to_integrate_Msg_bin = False
to_integrate_Msg_raw = False
to_integrate_Msg_cnt = False



chemin_base = 'H:/Boulot/Boulot Jeje/Main/Ican/Extract_traces_FTP/TempDownAWSS3/'
#chemin_base = 'D:/Boulot/Main/Ican/Extract_traces_FTP/TempDownAWSS3/'
#chemin_base = 'D:/temp/DWLD msg Bastides/'
path_sortie = 'D:/temp/'
prefixe_nom_sortie = 'Msg_IMEI_'

current_IMEI = str('rien')
current_dict_messages = dict()

def listdirectory(path): 
    liste_fichier=[] 
    #for root, dirs, files in os.walk(path): 
    for root, dirs, files in os.walk(path): 
        for i in files: 
            liste_fichier.append(os.path.join(root, i)) 
    return liste_fichier


def traite_1_1fic(nom_fic_msg): 
    #print("fichier en cours: ", path)
    #print("fichier en cours: ", os.path.basename(path))
    current_msg = dict()
    global current_IMEI
    global current_dict_messages
    
    with open(nom_fic_msg) as json_file2:
        data = json.load(json_file2)
        #print(data['tim'], data['int'])
        #print(data['evt'], data['eid'])
        #print(os.path.basename(path), data['ime'], data['tim'], data['int'], ecart_reception, data['evt'], data['eid'])
        #chaine = str(os.path.basename(path))+ " " + str(data['ime'])+ " " + str(data['tim'])+ " " + str(data['int'])+ " " + str(ecart_reception)+ " " + str(data['evt'])+ " " + str(data['eid'])+ '\n'
        fic_IMEI = str(data['ime'])
        #if (fic_IMEI != current_IMEI):
        if (fic_IMEI != current_IMEI):
            #Changement d'IMEI, on sauvegarde les données courrantes avant d'ouvrir les données du nouvel IMEI
            ecrire_dictionnaire_messages(path_sortie+prefixe_nom_sortie, current_IMEI)
            current_IMEI = fic_IMEI
            lire_dictionnaire_messages(path_sortie+prefixe_nom_sortie, current_IMEI)
            
        #incrémentation des compteurs
        current_dict_messages["NB_Msg"] += 1
        if (str(data['evt']) == '102'):
            current_dict_messages["NB_Journey"] += 1
        else:
            if (str(data['eid']) == '2A'):
                current_dict_messages["NB_Heartbeat"] += 1
        
        #remplissage du dictionnaire du message courrant
        current_msg['Typ_Msg'] = str(data['evt'])
        current_msg['Typ_Evt'] = str(data['eid'])
        current_msg['Timestamp_serveur'] = str(data['int'])
        current_msg['Timestamp_msg'] = str(data['tim'])
        current_msg['Delai_GSM'] = (data['int']-data['tim'])/1000
        current_msg['VIN'] = str(data['vin'])
        
        if current_msg['VIN'] not in current_dict_messages["VIN_list"]:
            current_dict_messages["VIN_list"].append(current_msg['VIN'])
        
        if to_integrate_Msg_bin:
            current_msg['Msg_brut'] = str(data['bin'])
        if to_integrate_Msg_cnt:
            current_msg['Msg_traduit_auto_cnt'] = dict()
            current_msg['Msg_traduit_auto_cnt'] = data['cnt'].copy()
        if to_integrate_Msg_raw:
            current_msg['Msg_traduit_auto_raw'] = data['raw']
        
        #ajout du message courrant dans la liste de messages du boitier
        current_dict_messages["Msg_list"].append(dict(current_msg))
    current_msg.clear()

def lire_dictionnaire_messages(chemin, strIMEI):
    global current_dict_messages
    nom_fic = chemin + strIMEI + '.json'
    current_dict_messages.clear()
    if os.path.isfile(nom_fic):
        with open(nom_fic, 'r') as json_file_result:
            current_dict_messages = json.load(json_file_result)
        pass
    if not "IMEI" in current_dict_messages:
        current_dict_messages["IMEI"] = strIMEI
        current_dict_messages["NB_Journey"] = 0
        current_dict_messages["NB_Msg"] = 0
        current_dict_messages["NB_Heartbeat"] = 0
        current_dict_messages["VIN_list"] = list()
        current_dict_messages["FW_list"] = list()
        current_dict_messages["Mapping_OBD_list"] = list()
        current_dict_messages["Mapping_Diag_list"] = list()
        current_dict_messages["Account_Number"] = ''
        current_dict_messages["Msg_list"] = list()

def ecrire_dictionnaire_messages(chemin, strIMEI):
    global current_dict_messages
    nom_fic = chemin + strIMEI + '.json'
    if "NB_Msg" in current_dict_messages:
        if current_dict_messages["NB_Msg"] > 0:
            #il y a des informations à sauvegarder
            with open(nom_fic, 'w') as json_file_result:
                json.dump(current_dict_messages, json_file_result)
            pass
            current_dict_messages.clear()

def efface_dictionnaire_messages(chemin, prefixe):
    debut_nom_fichier = chemin+prefixe
    for root, dirs, files in os.walk(chemin): 
        for i in files: 
            nom_fic = os.path.join(root, i)
            if debut_nom_fichier in nom_fic:
                os.remove(nom_fic)


if __name__ == "__main__":
    print("coucou")
    liste_fichiers = list()

    time1 = time.process_time()
    liste_fichiers = listdirectory(chemin_base)
    nb_fic = 0
    
    efface_dictionnaire_messages(path_sortie,prefixe_nom_sortie)
    
    for nom_fic in liste_fichiers:
        traite_1_1fic(nom_fic)
        nb_fic = nb_fic+1
    
   
    ecrire_dictionnaire_messages(path_sortie+prefixe_nom_sortie, current_IMEI)

    time2 = time.process_time()
    print( time2-time1, "secondes d'executions")
    print (nb_fic, "fichiers analyses")
    
    os.system("pause") # On met le programme en pause pour Ã©viter qu'il ne se referme (Windows)
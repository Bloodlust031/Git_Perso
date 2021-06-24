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
import Telech_AWS_Json

prefixe_nom_sortie = 'Msg_IMEI_'

current_IMEI = str('rien')
current_dict_messages = dict()
global_log_dict = dict()
start_time = 0
end_time = 0
last_liste_fichier = list()
Mode_ecrasement = False


def listdirectory(path): 
    liste_fichier=[] 
    #for root, dirs, files in os.walk(path): 
    for root, dirs, files in os.walk(path): 
        for i in files: 
            if i.endswith(".json"):
                if i not in last_liste_fichier:
                    liste_fichier.append(os.path.join(root, i))
                    last_liste_fichier.append(i)
    liste_fichier.sort()    #Les messages sont traités dans l'ordre chronologique.
    #liste_fichier.sort(reverse = True)    #Les messages sont traités dans l'ordre anti-chronologique.
    return liste_fichier


def traite_1_1fic(nom_fic_msg): 
    #print("fichier en cours: ", nom_fic_msg)
    #print("fichier en cours: ", os.path.basename(path))
    current_msg = dict()
    current_msg_decompose = dict()
    global current_IMEI
    global current_dict_messages
    
    
    with open(nom_fic_msg) as json_file2:
        data = json.load(json_file2)
        fic_IMEI = str(data['ime'])
        if (fic_IMEI != current_IMEI):
            #Changement d'IMEI, on sauvegarde les données courrantes avant d'ouvrir les données du nouvel IMEI
            ecrire_dictionnaire_messages(current_IMEI)
            current_IMEI = fic_IMEI
            lire_dictionnaire_messages(current_IMEI)
            
        #traitement du nom du fichier
        current_msg['NomFichier_Msg'] = os.path.basename(nom_fic_msg)
        str_temp = str(os.path.dirname(nom_fic_msg))
        str_temp = str_temp.replace("\\","/")
        current_msg['AdresseFichier_Msg'] = str_temp
            
        #incrémentation des compteurs
        current_dict_messages["NB_Msg"] += 1
        global_log_dict['NB_Msg']+=1
        if (str(data['evt']) == '102'):
            current_dict_messages["NB_Journey"] += 1
            global_log_dict['NB_Journey']+=1
        else:
            if (str(data['eid']) == '2A'):
                current_dict_messages["NB_Heartbeat"] += 1
        #remplissage du dictionnaire du message courrant
        current_msg['Typ_Msg'] = str(data['evt'])
        current_msg['Typ_Evt'] = str(data['eid'])
        current_msg['Timestamp_serveur'] = str(data['int'])
        current_msg['Timestamp_msg'] = str(data['tim'])
        current_msg['Delai_GSM'] = (data['int']-data['tim'])/1000
        set_Dstrib_delais_GSM(current_msg['Delai_GSM'])
        current_msg['VIN'] = str(data['vin'])
        
        current_dict_messages['Raw_cumulated_size'] += int(len(data['bin'])/2)
        global_log_dict['Raw_cumulated_size'] += int(len(data['bin'])/2)
        
        if current_msg['VIN'] not in current_dict_messages["VIN_list"]:
            current_dict_messages["VIN_list"].append(current_msg['VIN'])
        
        if "20033" in data['cnt']:
            str_temp =  data['cnt']['20033']
            current_msg['FW'] = str_temp
            if str_temp not in current_dict_messages["FW_list"]:
                current_dict_messages["FW_list"].append(str_temp)

        if "160" in data['cnt']:
            str_temp =  data['cnt']['160']
            if (str_temp != "0"): 
                current_dict_messages["Account_Number"] = str_temp
        
        current_msg["Params"] = dict()
        current_msg["Params"] = data['cnt'].copy()

        #décomposition du message brut
        current_msg_decompose = decomposition_fichier_brut(str(data['bin']))
        if(len(current_msg_decompose)>0):
            param_non_traduits = list()
            for cle,valeur in current_msg_decompose.items():
                if not cle in data['cnt']:
                    current_msg["Params"][cle] = valeur
                    param_non_traduits.append(cle)
                    if not cle in global_log_dict[Configuration.lbl_msg_Dic_Params_NonD2Hub]:
                        global_log_dict[Configuration.lbl_msg_Dic_Params_NonD2Hub].append(cle)
            if (len(param_non_traduits)>0):
                current_msg[Configuration.lbl_msg_Dic_Params_NonD2Hub] = param_non_traduits.copy()
            param_non_traduits.clear()
        
        #Comparaison des CRC
        str_temp = ''
        if '20250' in data['cnt']:
            str_temp = data['cnt']['20250']
        else:
            if '20250' in current_msg_decompose:
                str_temp = str(Boite_Outils.convert_Hex_decimal(current_msg_decompose['20250'], True))
        if (len(str_temp)>1):
            current_msg['CRC_List'] = list()
            current_msg['CRC_List'].append(str_temp)
            str_temp = ''
            if '20251' in data['cnt']:
                str_temp = data['cnt']['20251']
            else:
                if '20251' in current_msg_decompose:
                    str_temp = str(Boite_Outils.convert_Hex_decimal(current_msg_decompose['20251'], True))
            current_msg['CRC_List'].append(str_temp)
            #calcul du CRC
            str_temp = str(Boite_Outils.calc_CRC(data['bin'][:-32]))
            current_msg['CRC_List'].append(str_temp)

        if 'CRC_List' in current_msg:
            if ((current_msg['CRC_List'][0] == current_msg['CRC_List'][1]) and (current_msg['CRC_List'][0] == current_msg['CRC_List'][2])):
                current_msg['CRC_State'] = "CRC_OK"
                del current_msg['CRC_List']
            else:
                current_msg['CRC_State'] = "CRC_KO"
        else: 
            current_msg['CRC_State'] = "CRC_vide"

        #ajout du message courrant dans la liste de messages du boitier
        current_dict_messages["Msg_list"].append(dict(current_msg))
    current_msg.clear()

  
  
def decomposition_fichier_brut(raw_data):
    Liste_param = dict()
    fini = False
    str_raw = raw_data[22:]
    taille = Boite_Outils.convert_Hex_decimal(str_raw[0:8], True)  #taille globale du message
    str_raw = str_raw[8:]
    while not fini:
        ID_Param = str(Boite_Outils.convert_Hex_decimal(str_raw[0:4], True))
        Type_Param = Boite_Outils.convert_Hex_decimal(str_raw[4:8], True)
        Taille_Param = Boite_Outils.convert_Hex_decimal(str_raw[8:12], True)
        st_Valeur_Param = str_raw[12:(12+(Taille_Param*2))]
        Liste_param[ID_Param] = st_Valeur_Param
        str_raw = str_raw[(12+(Taille_Param*2)):]
        if len(str_raw) < 7:
            fini = True
    return Liste_param

def get_nom_fic_sortie(strIMEI = ''):
    if (len(strIMEI)> 2):
        nom = Configuration.Chemin_json_predigestmsg + prefixe_nom_sortie + strIMEI + '.json'
    else:
        nom = Configuration.Chemin_json_predigestmsg + '__Global_log.json'
    return nom

def lire_dictionnaire_messages(strIMEI):
    global current_dict_messages
    nom_fic = get_nom_fic_sortie(strIMEI)
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
        current_dict_messages["Raw_cumulated_size"] = 0
        current_dict_messages["VIN_list"] = list()
        current_dict_messages["FW_list"] = list()
        current_dict_messages["Mapping_OBD_list"] = list()  #TODO
        current_dict_messages["Mapping_Diag_list"] = list() #TODO
        current_dict_messages["Account_Number"] = ''
        init_Distrib_delais_GSM()
        current_dict_messages["Msg_list"] = list()

def ecrire_dictionnaire_messages(strIMEI):
    global current_dict_messages
    nom_fic = get_nom_fic_sortie(strIMEI)
    if "NB_Msg" in current_dict_messages:
        if current_dict_messages["NB_Msg"] > 0:
            #il y a des informations à sauvegarder
            if not current_IMEI in global_log_dict['List_IMEI']:
                global_log_dict['List_IMEI'][current_IMEI] = dict()
            global_log_dict['List_IMEI'][current_IMEI]["NB_Journey"] = current_dict_messages["NB_Journey"]
            global_log_dict['List_IMEI'][current_IMEI]["NB_Msg"] = current_dict_messages["NB_Msg"]
            global_log_dict['List_IMEI'][current_IMEI]["NB_Heartbeat"] = current_dict_messages["NB_Heartbeat"]
            global_log_dict['List_IMEI'][current_IMEI]["Raw_cumulated_size"] = current_dict_messages['Raw_cumulated_size']
            global_log_dict['List_IMEI'][current_IMEI]["FW_list"] = current_dict_messages["FW_list"].copy()
            global_log_dict['List_IMEI'][current_IMEI]["Dist_delay_GSM"] = current_dict_messages["Dist_delay_GSM"].copy()
            
            with open(nom_fic, 'w') as json_file_result:
                json.dump(current_dict_messages, json_file_result, indent="\t")
            pass
            current_dict_messages.clear()

def save_last_liste_fichier():
    with open(Configuration.Chemin_json_predigestmsg + '__Liste_msg_traites.json', 'w') as json_file_result:
        json.dump(last_liste_fichier, json_file_result, indent="\t")
    pass

def get_last_liste_fichier():
    global last_liste_fichier
    with open(Configuration.Chemin_json_predigestmsg + '__Liste_msg_traites.json', 'r') as json_file_result:
        last_liste_fichier  = json.load(json_file_result)
    pass

def get_last_global_log_dict():
    global global_log_dict
    with open(Configuration.Chemin_json_predigestmsg + '__Global_log.json', 'r') as json_file_result:
        global_log_dict  = json.load(json_file_result)
    pass

def efface_dictionnaire_messages():
    liste_fic = os.listdir(Configuration.Chemin_json_predigestmsg)
    
    for file1 in liste_fic:
        if fnmatch.fnmatch(file1, prefixe_nom_sortie + '*.json'):
            os.remove(Configuration.Chemin_json_predigestmsg+file1)    

def init_global_log_dict():
    global global_log_dict
    global start_time
    start_time = time.process_time()
    global_log_dict['Start Process Time'] = time.asctime(time.localtime())
    global_log_dict['End Process Time'] = ''
    global_log_dict['Process Duration'] = 0
    global_log_dict['NB_Msg'] = 0
    global_log_dict['NB_Journey'] = 0
    global_log_dict['Raw_cumulated_size'] = 0
    taille = len(Configuration.distribution_delais_GSM) + 1
    global_log_dict['Dist_delay_GSM'] = list()
    global_log_dict[Configuration.lbl_msg_Dic_Params_NonD2Hub] = list()
    for taille in range(0, taille):
        global_log_dict['Dist_delay_GSM'].append(0)
    global_log_dict['NB_IMEI'] = 0
    global_log_dict['List_IMEI'] = dict()
    
    
def close_global_log_dict():
    global global_log_dict
    global start_time
    global end_time
    end_time = time.process_time()
    global_log_dict['End Process Time'] = time.asctime(time.localtime())
    global_log_dict['Process Duration'] = end_time - start_time
    global_log_dict['NB_IMEI'] = len(global_log_dict['List_IMEI'])

    nom_fic = get_nom_fic_sortie()
    with open(nom_fic, 'w') as json_file_result:
        json.dump(global_log_dict, json_file_result, indent="\t")
    pass


def init_Distrib_delais_GSM():
    global current_dict_messages
    taille = len(Configuration.distribution_delais_GSM) + 1
    current_dict_messages['Dist_delay_GSM'] = list()
    for taille in range(0, taille):
        current_dict_messages['Dist_delay_GSM'].append(0)
    
def set_Dstrib_delais_GSM(delai):
    global current_dict_messages
    taille = len(Configuration.distribution_delais_GSM) + 1
    i = 0
    
    while i < taille:
        if i == (taille-1):
            #On est dans la derniere case
            current_dict_messages['Dist_delay_GSM'][i] += 1
            global_log_dict['Dist_delay_GSM'][i] += 1
        else:
            if delai < Configuration.distribution_delais_GSM[i]:
                current_dict_messages['Dist_delay_GSM'][i] += 1
                global_log_dict['Dist_delay_GSM'][i] += 1
                i = taille
        i+=1
        
def telech_msg():
    print("Lancement du Téléchargement")
    Telech_AWS_Json.telech(Date_list = ['2021-03-08', '2021-03-12'], IMEI_list = ['868996033815168'])
    print("Attendre la fin des téléchargements")
    bretour = False
    txt_input = input("Voulez vous supprimer les messages Event (O pour oui) ?")
    try:
        if ((txt_input[0] == "O") or (txt_input[0] == "o")):
            bretour = True
    except:
        bretour = False
    if bretour:
        Telech_AWS_Json.Supprim_Event_msg()

    
def mode_normal():
    global last_liste_fichier
    global liste_fichiers
    
    last_liste_fichier.clear()
    
    Configuration.init_config()
    
    #telech_msg()
    
    liste_fichiers = list()


    bretour = False
    txt_input = input("Voulez vous conserver les pré-analyses précédentes (O pour oui) ?")
    try:
        if ((txt_input[0] == "O") or (txt_input[0] == "o")):
            bretour = True
    except:
        bretour = False
    if bretour:
        get_last_liste_fichier()
        get_last_global_log_dict()
    else:
        try:
            efface_dictionnaire_messages()
            os.remove(Configuration.Chemin_json_predigestmsg + '__Liste_msg_traites.json')
            os.remove(Configuration.Chemin_json_predigestmsg + '__Global_log.json')
        except:
            pass
        init_global_log_dict()


    #liste_fichiers = listdirectory(Configuration.Chemin_json_msg)
    liste_fichiers = listdirectory(Configuration.Chemin_json_msg_IMEI_SORTED)
    #liste_fichiers = listdirectory('D:\Temp_JSON\IMEI_SORTED')
    nb_fic = 0
    
    print(str(len(liste_fichiers)) + " fichiers a analyser")
    
    for nom_fic in liste_fichiers:
        #print(nom_fic)
        traite_1_1fic(nom_fic)
        nb_fic = nb_fic+1
    
   
    ecrire_dictionnaire_messages(current_IMEI)
    close_global_log_dict()
    save_last_liste_fichier()
    
    print( end_time-start_time, "secondes d'executions")
    print(nb_fic, "fichiers analyses")
    print("fini")
    #print(global_log_dict)


if __name__ == "__main__":
    print("coucou")
    mode_normal()
    os.system("pause") # On met le programme en pause pour Ã©viter qu'il ne se referme (Windows)
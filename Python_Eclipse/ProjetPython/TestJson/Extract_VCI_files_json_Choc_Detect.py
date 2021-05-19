# -*-coding:Latin-1 -*
'''
Created on 6 nov. 2020

@author: blood
'''
import os
import json
import Configuration
import Boite_Outils
import Telech_AWS_Json


prefixe_nom_sortie = 'Msg_IMEI_'

current_IMEI = str('rien')
global_log_dict = dict()
list_distribution_choc = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 3.0]

str_Date_list = ['2021-05-01', '2021-05-18']
#str_IMEI_list = ['868997035961331'] #ellectramobilys
str_IMEI_list = ["864504031666486","864504039671660","867322038021580","868996033847682","868996033832148","868996033813734","867322038574737","868996033832155","868996033818816","868996033818824","868996033841008","868996033839960","868996033837634","868997035954773","867322034104968","868997035954708","868996033847690","868996033833401","867322034113324","868996033846692","868996033843129","868996033849365","868996033818360","868996033847625","867322038041828","868996033815655","867322038060984","868996033839697","864504039699729","868996033813197","865794031378062","867322034095505","865794031463005","867322038051033","867322034106906","864504031156249","869103026251605","867322038016408","865794031339080","864504039673575","865794031485925","864504031771799","864504039683657","865794031485420","864504031156355","865794031325014","864504031605948","865794031486477","864504031239631","864504031263466","865794031212766","864504031624451","864504039695289","865794031323217","868996033851304","863977036491129","864504031827815","867322034116418","867322038007985","868997035945326","867322038021036","864504031491620","864504031618826","864504031308253","863977036412687","864504031132208","864504031619147","864504031430644","864504031198308","865794031460100","869103026392326","865794031430806","865794031342522","864504039683285","864504031230036","865794031466412","865794031289236","864504031783141","864504031650852","864504031712058","864504039651472","865794031462791","865794031470307","864504031791342","865794031437785","864504031710649","865794031474978","864504039662206","865794031381579","864504031909134","867322034096933","867322034118224","864504039722075","868996033837923","868997035954104","867322038578183","864504031779263","862010038903809","865794031481585","868996033815358","865794031486188","869103026520330","869103026311219","868996033837733","867322038612974","867322034096180","864504031619105","864504031908359","864504039710583","864504039674698","864504031182104","864504039672403","864504031444173","864504039696873","864504031664101","868996033817479"] #VU 

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

def init_Distrib_Choc(dictionnaire):
    taille = len(list_distribution_choc) + 1
    dictionnaire['Distrib_Alertes'] = list()
    for i in range(0, taille-1):
        dictionnaire['Distrib_Alertes'].append(0)
    
def set_Distrib_Choc(str_IMEI, valeur):
    global global_log_dict
    taille = len(list_distribution_choc) + 1
    i = 0
    
    while i < taille:
        if i == (taille-1):
            #On est dans la derniere case
            global_log_dict["ByIMEI"][str_IMEI]['Distrib_Alertes'][i] += 1
            global_log_dict["Total"]['Distrib_Alertes'][i] += 1
        else:
            if valeur < list_distribution_choc[i]:
                global_log_dict["ByIMEI"][str_IMEI]['Distrib_Alertes'][i] += 1
                global_log_dict["Total"]['Distrib_Alertes'][i] += 1
                i = taille
        i+=1

def reconstruction_propre_Distrib_Choc():
    global global_log_dict
    taille = len(list_distribution_choc) + 1
    i = 0
    dico = dict()
    
    dico.clear()
    for i in range(0, taille-1):
        if i == 0:
            strseuil = "X < " + str(list_distribution_choc[i])
        else:
            if i == taille-2:
                strseuil = "X >= " + str(list_distribution_choc[i-1])
            else:
                strseuil = str(list_distribution_choc[i-1]) + " <= X < " + str(list_distribution_choc[i])
        dico[strseuil] = global_log_dict["Total"]['Distrib_Alertes'][i]
    del global_log_dict["Total"]['Distrib_Alertes']
    global_log_dict["Total"]['Distrib_Alertes'] = dico.copy()

    for str_IMEI in global_log_dict["ByIMEI"]:
        dico.clear()
        for i in range(0, taille-1):
            if i == 0:
                strseuil = "X < " + str(list_distribution_choc[i])
            else:
                if i == taille-2:
                    strseuil = "X >= " + str(list_distribution_choc[i-1])
                else:
                    strseuil = str(list_distribution_choc[i-1]) + " <= X < " + str(list_distribution_choc[i])
            dico[strseuil] = global_log_dict["ByIMEI"][str_IMEI]['Distrib_Alertes'][i]
        del global_log_dict["ByIMEI"][str_IMEI]['Distrib_Alertes']
        global_log_dict["ByIMEI"][str_IMEI]['Distrib_Alertes'] = dico.copy()
        
        if global_log_dict["ByIMEI"][str_IMEI]['NB Alertes'] == 0:
            del global_log_dict["ByIMEI"][str_IMEI]['Distrib_Alertes']
            del global_log_dict["ByIMEI"][str_IMEI]['Seuil Alerte']
            del global_log_dict["ByIMEI"][str_IMEI]['Alerte Max']
            del global_log_dict["ByIMEI"][str_IMEI]['Liste Alertes']
        del global_log_dict["ByIMEI"][str_IMEI]["NB iCAN"]  #inutile dans les equipements
    for str_IMEI in global_log_dict["ByModel"]:
        dico.clear()
        for i in range(0, taille-1):
            if i == 0:
                strseuil = "X < " + str(list_distribution_choc[i])
            else:
                if i == taille-2:
                    strseuil = "X >= " + str(list_distribution_choc[i-1])
                else:
                    strseuil = str(list_distribution_choc[i-1]) + " <= X < " + str(list_distribution_choc[i])
            dico[strseuil] = global_log_dict["ByModel"][str_IMEI]['Distrib_Alertes'][i]
        del global_log_dict["ByModel"][str_IMEI]['Distrib_Alertes']
        global_log_dict["ByModel"][str_IMEI]['Distrib_Alertes'] = dico.copy()
        
        if global_log_dict["ByModel"][str_IMEI]['NB Alertes'] == 0:
            try:
                del global_log_dict["ByModel"][str_IMEI]['Distrib_Alertes']
            except: 
                pass
            try:
                del global_log_dict["ByModel"][str_IMEI]['Alerte Max']
            except: 
                pass
            try:
                del global_log_dict["ByModel"][str_IMEI]['Liste Alertes']
            except: 
                pass
    
        
def Init_equipment_dico(parent_dico, str_IMEI):
    parent_dico[str_IMEI] = dict()
    parent_dico[str_IMEI]["Model"] = ""
    parent_dico[str_IMEI]["Distance"] = 0
    parent_dico[str_IMEI]["NB Alertes"] = 0
    parent_dico[str_IMEI]["Seuil Alerte"] = 0
    parent_dico[str_IMEI]["Alerte Max"] = 0
    parent_dico[str_IMEI]["Liste Alertes"] = list()
    parent_dico[str_IMEI]["Liste Alertes"].clear()
    init_Distrib_Choc(parent_dico[str_IMEI])
    parent_dico[str_IMEI]["NB iCAN"] = 0

    
    
def traite_1_1fic(nom_fic_msg): 
    #print("fichier en cours: ", nom_fic_msg)
    global global_log_dict
    
    with open(nom_fic_msg) as json_file2:
        data = json.load(json_file2)
            
        str_IMEI = str(data['ime'])
        if (str(data['evt']) == "100"):
            #message Event
            if str(data['eid']) == '43':
                #message detection de choc
                if str_IMEI not in global_log_dict["ByIMEI"]:
                    Init_equipment_dico(global_log_dict["ByIMEI"], str_IMEI)
                    global_log_dict["Total"]["NB iCAN"] += 1
                if "20279" in data['cnt']:
                    global_log_dict["ByIMEI"][str_IMEI]["Seuil Alerte"] = data['cnt']['20279']
                if "20278" in data['cnt']:
                    Val_alerte = float(data['cnt']['20278'])
                    if global_log_dict["ByIMEI"][str_IMEI]["Alerte Max"] < Val_alerte:
                        global_log_dict["ByIMEI"][str_IMEI]["Alerte Max"] = Val_alerte
                    global_log_dict["ByIMEI"][str_IMEI]["Liste Alertes"].append(Val_alerte)
                    global_log_dict["Total"]["Liste Alertes"].append(Val_alerte)
                    global_log_dict["ByIMEI"][str_IMEI]["NB Alertes"] += 1
                    global_log_dict["Total"]["NB Alertes"] += 1
                    set_Distrib_Choc(str_IMEI, Val_alerte)
        if (str(data['evt']) == "102"):
            #message Journey
            if str_IMEI not in global_log_dict["ByIMEI"]:
                Init_equipment_dico(global_log_dict["ByIMEI"], str_IMEI)
                global_log_dict["Total"]["NB iCAN"] += 1
            if "2010" in data['cnt']:
                dist = float(data['cnt']['2010']) / 1000
                global_log_dict["ByIMEI"][str_IMEI]["Distance"] += dist
                global_log_dict["Total"]["Distance"] += dist
        
def stat_by_veh():
    with open(Configuration.path_json_D2Hub_info_total) as json_file3:
        equipment_dico = json.load(json_file3)
        for str_IMEI in global_log_dict["ByIMEI"]:
            if str_IMEI in equipment_dico:
                if "VEH_Model" in equipment_dico[str_IMEI]:
                    global_log_dict["ByIMEI"][str_IMEI]["Model"] = equipment_dico[str_IMEI]["VEH_Model"]
    
    for str_IMEI in global_log_dict["ByIMEI"]:
        if "Model" in global_log_dict["ByIMEI"][str_IMEI]:
            strModel = global_log_dict["ByIMEI"][str_IMEI]["Model"]
            if len(strModel)<=1:
                strModel = "Autre"
        else:
            strModel = "Autre" 
        pass
        if strModel not in global_log_dict["ByModel"]:
            Init_equipment_dico(global_log_dict["ByModel"], strModel)
            del global_log_dict["ByModel"][strModel]["Model"]
            del global_log_dict["ByModel"][strModel]["Seuil Alerte"]
            del global_log_dict["ByModel"][strModel]["Liste Alertes"]
        global_log_dict["ByModel"][strModel]["Distance"] += global_log_dict["ByIMEI"][str_IMEI]["Distance"]
        global_log_dict["ByModel"][strModel]["NB Alertes"] += global_log_dict["ByIMEI"][str_IMEI]["NB Alertes"]
        global_log_dict["ByModel"][strModel]["NB iCAN"] += 1
        if (global_log_dict["ByModel"][strModel]["Alerte Max"] < global_log_dict["ByIMEI"][str_IMEI]["Alerte Max"]): 
            global_log_dict["ByModel"][strModel]["Alerte Max"] = global_log_dict["ByIMEI"][str_IMEI]["Alerte Max"]
        
        taille = len(list_distribution_choc) + 1
        i = 0
        for i in range(0, taille-1):
            global_log_dict["ByModel"][strModel]['Distrib_Alertes'][i] += global_log_dict["ByIMEI"][str_IMEI]['Distrib_Alertes'][i]
        
        
@Boite_Outils.print_temps    
def analyse_json_choc():
    global global_log_dict
    Configuration.init_config()

    #téléchargement des messages
    print("Lancement du Téléchargement")
    Telech_AWS_Json.telech(Date_list = str_Date_list, IMEI_list = str_IMEI_list)
    os.system("pause") # On met le programme en pause pour Ã©viter qu'il ne se referme (Windows)

    #traitement
    liste_fichiers = list()
    global_log_dict["Total"] = dict()
    global_log_dict["Total"]["Distance"] = 0
    global_log_dict["Total"]["NB iCAN"] = 0
    global_log_dict["Total"]["NB Alertes"] = 0
    global_log_dict["Total"]["Liste Alertes"] = list()
    global_log_dict["Total"]["Liste Alertes"].clear()
    global_log_dict["ByIMEI"] = dict()
    global_log_dict["ByIMEI"].clear()
    global_log_dict["ByModel"] = dict()
    global_log_dict["ByModel"].clear()
    
    init_Distrib_Choc(global_log_dict["Total"])
     
    liste_fichiers = listdirectory(Configuration.Chemin_json_msg)
    nb_fic = 0
    print(str(len(liste_fichiers)) + " fichiers a analyser")
    for nom_fic in liste_fichiers:
        #print(nom_fic)
        traite_1_1fic(nom_fic)
        nb_fic = nb_fic+1
    
    stat_by_veh()
    
    #sauvegarde du résultat
    reconstruction_propre_Distrib_Choc()
    nom_fic = Configuration.path_sortie_Stat + "Stat_Choc.json"
    with open(nom_fic, 'w') as json_file_result:
        json.dump(global_log_dict, json_file_result, indent=4)

if __name__ == "__main__":
    print("coucou")
    
    Configuration.init_config()
    analyse_json_choc()
    

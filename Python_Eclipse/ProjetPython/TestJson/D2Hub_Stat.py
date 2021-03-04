# -*-coding:utf-8 -*
'''
Created on 30 janv. 2021

@author: blood
'''

import Configuration
import json
import Import_D2HUB_Info

account_dico = dict()

def Set_Account_List_():
    global account_dico
    
    account_dico.clear()
    children_account = dict()
    children_list = list()
    children_list.clear()
    master_account = dict()
    with open(Configuration.path_json_D2Hub_account) as json_file2:
        data = json.load(json_file2)
        #recherche des comptes maitres
        for current_item in data:
            if current_item["parentName"] == "ADMIN_ROOT":
                master_account.clear()
                master_account["uuid"] = current_item["uuid"]
                master_account["name"] = current_item["accountName"]
                master_account["children_list"] = list()
                account_dico[current_item["uuid"]] = master_account.copy()
            else:
                #c'est un enfant => on le mete de côté pour le moment
                children_account.clear()
                children_account["name"] = current_item["accountName"]
                children_account["uuid"] = current_item["uuid"]
                children_account["parentUuid"] = current_item["parentUuid"]
                children_list.append(children_account.copy())
                
        for current_item in children_list:
            if current_item["parentUuid"] in account_dico:
                account_dico[current_item["parentUuid"]]["children_list"].append(current_item.copy())
                children_list.remove(current_item)

        #remplissage des comptes enfants dans les comptes parents
        '''while (len(children_list)>1):
            for current_item in children_list:
                if current_item["parentUuid"] in account_dico:
                    account_dico[current_item["parentUuid"]]["children_list"].append(current_item.copy())
                    children_list.remove(current_item)
                else:
                    for master_account in account_dico:
                        for i in range(len(master_account["children_list"])):
                            if children_account["uuid"] == master_account["children_list"][i]["uuid"]:
                                master_account["children_list"].append(current_item.copy())
                                children_list.remove(current_item)
                            
                            
                        for children_account in master_account["children_list"]:
                            if children_account["uuid"] == current_item["uuid"]:
                                master_account["children_list"].append(current_item.copy())
                                children_list.remove(current_item)'''

def gen_stat()
    txt_input = input("Voulez-vous mettre à jour les données d'entrées (O pour oui) ?")
    try:
        if ((txt_input[0] == "O") or (txt_input[0] == "o")):
            bretour = True
            Import_D2HUB_Info.Extract_infos_from_D2Hub()
    except:
        bretour = False
    
    

if __name__ == '__main__':
    #mise � jour des informations depuis D2Hub
    #Import_D2HUB_Info.Extract_infos_from_D2hHub()
    #Import_D2HUB_Info.Get_D2Hub_Account_list()
    
    
    Set_Account_List_()
    print (account_dico)
    
    pass
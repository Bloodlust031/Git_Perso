# -*-coding:Latin-1 -*
'''
Created on 5 déc. 2020

@author: blood
'''

import os
import Configuration

item_list = list()

def Import_from_ImportD2HUB():
    liste_lignes = list()
    with open(Configuration.path_ImportD2HUB, 'r')as mon_fichier:
        liste_lignes = mon_fichier.readlines()
        for ligne in liste_lignes:
            print (ligne)
    
def Import_from_ExportD2HUB():
    liste_lignes = list()

            
if __name__ == '__main__':
    Import_from_ImportD2HUB()
    pass
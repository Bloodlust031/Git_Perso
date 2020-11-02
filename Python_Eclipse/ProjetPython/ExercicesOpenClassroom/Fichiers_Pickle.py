# -*-coding:Latin-1 -*
'''Created on 15 oct. 2020

@author: blood

Enregistrement de variables et objets dans un fichier binaire
'''

import os
import pickle

nombre = 50

def ecriture_variable_fichier(nomfic):
    score = {
        "joueur 1":    5,
        "joueur 2":   35,
        "joueur 3":   20,
        "joueur 4":    2,
    }
    chaine = "tototititatatete"
    with open(nomfic, 'wb')as mon_fichier:
        mon_pickler = pickle.Pickler(mon_fichier)
        mon_pickler.dump(score)
        mon_pickler.dump(chaine)

def lecture_variable_fichier(nomfic):
    global nombre
    with open(nomfic, 'rb')as mon_fichier:
        mon_depickler = pickle.Unpickler(mon_fichier)
        score_recup = mon_depickler.load()
        chaine_recup = mon_depickler.load()
    print(chaine_recup)
    for cle,valeur in score_recup.items():
        print ("la clé {} a la valeur {}.".format(cle,valeur))
    nombre = nombre*2
    print (nombre)

if __name__ == '__main__':
    os.chdir("D:/temp")
    print (nombre)
    ecriture_variable_fichier('mesdonnees')
    lecture_variable_fichier('mesdonnees')
    print (nombre)
    os.system("pause") # On met le programme en pause pour Ã©viter qu'il ne se referme (Windows)
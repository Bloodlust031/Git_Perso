# -*-coding:Latin-1 -*
'''
Created on 15 oct. 2020

@author: blood
'''


import os
import pickle


liste_scores = {}

def lire_scores():
    global liste_scores
    try:
        with open('fic_scores', 'rb')as mon_fichier:
            mon_depickler = pickle.Unpickler(mon_fichier)
            liste_scores = mon_depickler.load()
    except:
        liste_scores = {}

def get_score_joueur(nom_joueur):
    score = 0
    if (len(liste_scores) == 0):
        lire_scores()
    try :
        score = liste_scores[nom_joueur]
    except:
        score = 0
    return score

def ecrire_scores():
    global liste_scores
    with open('fic_scores', 'wb')as mon_fichier:
        mon_pickler = pickle.Pickler(mon_fichier)
        mon_pickler.dump(liste_scores)    

def ecrire_score_joueur(nom_joueur, points):
    global liste_scores
    liste_scores[nom_joueur] = points
    ecrire_scores()

def ajouter_score_joueur(nom_joueur, points):
    global liste_scores
    score = get_score_joueur(nom_joueur)
    liste_scores[nom_joueur] = score + points
    ecrire_scores()

def get_nom_joueur():
    txt_input = input("Veuillez saisir votre nom:")
    txt_input = txt_input.capitalize()
    return txt_input

def get_confirmation():
    bretour = False
    txt_input = input("Veuillez confirmer (O pour oui):")
    try:
        if ((txt_input[0] == "O") or (txt_input[0] == "o")):
            bretour = True
    except:
        bretour = False
    return bretour

def get_1_lettre():
    bretour = False
    while not bretour:
        txt_input = input("Veuillez saisir une lettre:")
        if len(txt_input)!= 1:
            print("Veuillez saisir une lettre et une seule")
        else:
            if(txt_input.isalpha()):
                bretour = True
            else:
                print("Veuillez saisir une lettre")
    return txt_input

def is_lettre_in_mot(lettre, mot):
    if lettre.lower() in mot.lower():
        bretour = True
    else:
        bretour = False
    return bretour

def recompose_mot_courrant(lettre, mot_cherche, mot_compose):
    mot2 = ""
    
    for i in range (0, len(mot_cherche)):
        if (lettre.lower()== mot_cherche[i]):
            mot2 += lettre.lower()
        else:
            mot2 += mot_compose[i]
    return mot2

def fini_mot_courrant(mot_compose):
    fini = True
    
    for i in range (0, len(mot_compose)):
        if (mot_compose[i] == "*"):
            fini = False 
    return fini

if __name__ == '__main__':
    lire_scores()
    #print ("taille liste:" , len(liste_scores))
    for cle,valeur in liste_scores.items():
        print ("la clé {} a la valeur {}.".format(cle,valeur))
        
    ecrire_score_joueur("toto", 6)
    ecrire_score_joueur("titi", 7)
    ajouter_score_joueur("toto", 2)
    for cle,valeur in liste_scores.items():
        print ("la clé {} a la valeur {}.".format(cle,valeur))
        
        
        
    i = is_lettre_in_mot("E", "nomadise")
    print (i)
    i = is_lettre_in_mot("R", "nomadise")
    print (i)
    pass
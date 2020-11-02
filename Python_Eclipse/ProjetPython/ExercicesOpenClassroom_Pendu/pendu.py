'''
Created on 15 oct. 2020

@author: blood
'''

from donnees import *
from fonctions import *

mot_recherche = ""
mot_courrant = ""
nom_joueur = ""
Chances_restantes = 0
mot_trouve = False

def debut_partie():
    global mot_recherche
    global nom_joueur
    global mot_courrant
    global Chances_restantes
    
    bjoueur_OK = False
    mot_recherche = get_un_mot()
    mot_courrant = ""
    
    Chances_restantes = get_nb_essais_max()
    for i in range (0, len(mot_recherche)):
        mot_courrant = mot_courrant + "*"
        
    while not bjoueur_OK:
        nom_joueur = get_nom_joueur()
        score_debut = get_score_joueur(nom_joueur)
        print("Joueur", nom_joueur, "-", score_debut, "points")
        bjoueur_OK = get_confirmation()
    

def milieu_partie():
    global Chances_restantes
    global mot_courrant
    
    
    print("Chances_restantes:" , Chances_restantes)
    print("mot_courrant:" , mot_courrant)
    lettre_courrante = get_1_lettre()
    if is_lettre_in_mot(lettre_courrante, mot_recherche):
        print ("correct")
        mot_courrant = recompose_mot_courrant(lettre_courrante, mot_recherche, mot_courrant)
        fini = fini_mot_courrant(mot_courrant)
    else:
        Chances_restantes-=1
        fini = False
        print ("Erreur!")
    return fini


if __name__ == '__main__':

    debut_partie()
    print ("mot:", mot_recherche)
    while ((not (mot_trouve)) and (Chances_restantes > 0)):
        mot_trouve = milieu_partie()
    if mot_trouve:
        print("Trouve:", mot_recherche)
        ajouter_score_joueur(nom_joueur, Chances_restantes)
    pass
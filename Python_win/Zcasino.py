# -*-coding:Latin-1 -*

import Outils.Boite_outils
import os
import math
import random


#pour arrondir � l'entier sup�rieur: ceil
#pour tirer un nombre au hazard randrange(50)

cagnote = 50
mise_courrante = 0
case_choisie = 0
case_tiree = 0

def recup_mise():
    #demande de la case
    case_choisie = Outils.Boite_outils.demande_valeur_numerique("Sur quelle case voulez-vous miser?", 0, 49)
    #demande de la mise
    mise_courrante = Outils.Boite_outils.demande_valeur_numerique("Combien voulez-vous miser?", 1, cagnotte)
    
def tirage_roulette():
    case_tiree = randrange(50)
    print ("La boule s'est arr�t�e sur le " + case_tiree)
    
def calcul_gain():
    if (case_tiree == case_choisie):
        print ("F�licitationssLa boule s'est arr�t�e sur le " + case_tiree)
    
    
if __name__ == "__main__":
    print ("Bienvenue au casino.")
    print ("Votre cagnote de d�part est de " + cagnote + "$")
    while (cagnote > 0):
        recup_mise()
        tirage_roulette()
        calcul_gain()
    print ("perdu")
            
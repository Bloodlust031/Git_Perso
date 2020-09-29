# -*-coding:Latin-1 -*

#import Outils.Boite_outils.py
import Boite_outils
import os
import math
import random


#pour arrondir à l'entier supérieur: ceil
#pour tirer un nombre au hazard randrange(50)

cagnote = 50
mise_courrante = 0
case_choisie = 0
case_tiree = 0

def recup_mise():
    global case_choisie
    global mise_courrante
    global cagnote
    
    #demande de la case
    case_choisie = Boite_outils.demande_valeur_numerique("Sur quelle case voulez-vous miser?", 0, 49)
    #demande de la mise
    mise_courrante = Boite_outils.demande_valeur_numerique("Combien voulez-vous miser?", 1, cagnote)
    
def tirage_roulette():
    global case_tiree
    case_tiree = random.randrange(50)
    print ("La boule s'est arrétée sur le ", case_tiree)
    
def calcul_gain():
    global case_tiree
    global case_choisie
    global mise_courrante
    global cagnote
    
    if (case_tiree == case_choisie):
        print ("Félicitations La boule s'est arrétée sur le ", case_tiree)
        cagnote = cagnote + (mise_courrante*3)
    elif((case_tiree%2) == (case_choisie%2)):
        cagnote = cagnote + math.ceil(mise_courrante/2)
    else:
        cagnote = cagnote - mise_courrante
    
if __name__ == "__main__":
    print ("Bienvenue au casino.")
    print ("Votre cagnote de départ est de " , cagnote , "$")
    while (cagnote > 0):
        recup_mise()
        tirage_roulette()
        calcul_gain()
        print ("Vous avez maintenant " , cagnote , "$")
    print ("perdu")
            
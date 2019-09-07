# -*-coding:Latin-1 -*

import os
import math
import random

def rempli_liste(nb_valeurs, val_max=10):
    liste_a_remplir = list()
    val_courrante = int()
    
    for i in range(1, nb_valeurs+1):
        val_courrante = random.randrange(val_max)
        liste_a_remplir.append(val_courrante)     
    return liste_a_remplir

def tri_ancienne():
    nb_val = 30
    
    liste_a_trier = rempli_liste(nb_val)
    print("avant tri", liste_a_trier)
    
    for j in range(0, nb_val-1):
        for i in range(0, nb_val-1):
            if liste_a_trier[i] > liste_a_trier[i+1]:
                liste_a_trier[i],liste_a_trier[i+1] = liste_a_trier[i+1],liste_a_trier[i] 
    print("apres tri", liste_a_trier)

def tri_2_listes():
    nb_val = 30
    
    liste_a_trier = rempli_liste(nb_val,20)
    liste_triee = list()
    print("avant tri", liste_a_trier)
    
    #tri en conservant les doublons
    j=0
    for val_courrante in liste_a_trier:
        i=0
        place = False
        while place == False:
            if i >= j:
                liste_triee.append(val_courrante)
                place = True
            else:
                if liste_triee[i]>val_courrante:
                    liste_triee.insert(i,val_courrante)
                    place = True
            i += 1
        j += 1
    print("apres tri", liste_triee)

    liste_triee.clear()
    
    
    #tri en supprimant les doublons
    j=0
    for val_courrante in liste_a_trier:
        i=0
        place = False
        while place == False:
            if i >= j:
                liste_triee.append(val_courrante)
                j += 1
                place = True
            else:
                if liste_triee[i]==val_courrante:
                    place = True
                else:
                    if liste_triee[i]>val_courrante:
                        liste_triee.insert(i,val_courrante)
                        j += 1
                        place = True
            i += 1
        
    print("apres tri sans doublons", liste_triee)


def tri_1_liste():
    nb_val = 30
    trouve = False
    
    liste_a_trier = rempli_liste(nb_val,20)
    liste_a_trier2 = liste_a_trier.copy()

    print("avant tri", liste_a_trier)
    
    #tri en conservant les doublons
    
    for i in range(1, nb_val):
        val_courrante = liste_a_trier[i]
        if val_courrante >= liste_a_trier[i-1]:
            #rien a faire
            trouve = True
        else:
            trouve = False
            j= 0
            while trouve == False:
                if val_courrante < liste_a_trier[j]:
                    liste_a_trier.insert(j, val_courrante)
                    trouve = True
                j += 1
            del liste_a_trier[i+1]

    print("apres tri", liste_a_trier)

    #tri en supprimant les doublons
    i=1
    while i < len(liste_a_trier2):
        val_courrante = liste_a_trier2[i]
        trouve = False
        for j in range (0, i):
            if val_courrante == liste_a_trier2[j]:
                del liste_a_trier2[i]
                trouve = True
        if trouve == False:
            if val_courrante > liste_a_trier2[i-1]:
                #rien a faire
                trouve = True
                i += 1
            else:
                trouve = False
                j= 0
                while trouve == False:
                    if val_courrante == liste_a_trier2[j]:
                        del liste_a_trier2[i]
                        trouve = True
                    if val_courrante < liste_a_trier2[j]:
                        liste_a_trier2.insert(j, val_courrante)
                        
                        trouve = True
                        del liste_a_trier2[i+1]
                    j += 1
                i+=1

    print("apres tri sans doublons", liste_a_trier2)


if __name__ == "__main__":
    print("---------tri a l'ancienne---------")
    tri_ancienne()

    print("---------tri avec 2 listes---------")
    tri_2_listes()
    
    print("---------tri avec 1 liste---------")
    tri_1_liste()
    
    # On met le programme en pause pour éviter qu'il ne se referme (Windows)
    os.system("pause")
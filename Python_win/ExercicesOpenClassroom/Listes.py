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

def affiche_float(val_float, nb_dec = 3):
    if type(val_float) == float:
        str_float = str(val_float)
        partie_entiere, partie_decimale = str_float.split(".")
        str_conv = ",".join([partie_entiere,partie_decimale[:nb_dec]])
        print(str_conv)
    else:
        print("pas un flottant")

def afficher(*parametres, sep=' ', fin='\n'):
    """Fonction chargée de reproduire le comportement de print.
    
    Elle doit finir par faire appel à print pour afficher le résultat.
    Mais les paramètres devront déjà avoir été formatés. 
    On doit passer à print une unique chaîne, en lui spécifiant de ne rien mettre à la fin :

    print(chaine, end='')"""
    
    # Les paramètres sont sous la forme d'un tuple
    # Or on a besoin de les convertir
    # Mais on ne peut pas modifier un tuple
    # On a plusieurs possibilités, ici je choisis de convertir le tuple en liste
    parametres = list(parametres)
    # On va commencer par convertir toutes les valeurs en chaîne
    # Sinon on va avoir quelques problèmes lors du join
    for i, parametre in enumerate(parametres):
        parametres[i] = str(parametre)
    # La liste des paramètres ne contient plus que des chaînes de caractères
    # À présent on va constituer la chaîne finale
    chaine = sep.join(parametres)
    # On ajoute le paramètre fin à la fin de la chaîne
    chaine += fin
    # On affiche l'ensemble
    print(chaine, end='')
        
def tri_liste():
    inventaire = [("pommes", 22),("melons", 4),("poires", 18),("fraises", 76),("prunes", 51),]
    inventaire2 =  [(nb,nom) for nom,nb in inventaire]
    inventaire2.sort(reverse = True)
    inventaire3 =  [(nom,nb) for nb,nom in inventaire2]
    print (inventaire3)

def tri_liste2():
    inventaire = [("pommes", 22),("melons", 4),("poires", 18),("fraises", 76),("prunes", 51),]
    # On change le sens de l'inventaire, la quantité avant le nom
    inventaire_inverse = [(qtt, nom_fruit) for nom_fruit,qtt in inventaire]
    # On n'a plus qu'à trier dans l'ordre décroissant l'inventaire inversé
    # On reconstitue l'inventaire trié
    inventaire = [(nom_fruit, qtt) for qtt,nom_fruit in sorted(inventaire_inverse, reverse=True)]
    print (inventaire)

if __name__ == "__main__":
    print("---------tri a l'ancienne---------")
    tri_ancienne()

    print("---------tri avec 2 listes---------")
    tri_2_listes()
    
    print("---------tri avec 1 liste---------")
    tri_1_liste()

    print("---------conversion 1.123456789---------")
    affiche_float(1.123456789,6)

    print("---------test print_like---------")
    afficher("toto", "titi",1.25, "tata")
    
    print("---------tri_liste---------------")
    tri_liste()
    tri_liste2()
    
    
    # On met le programme en pause pour éviter qu'il ne se referme (Windows)
    os.system("pause")
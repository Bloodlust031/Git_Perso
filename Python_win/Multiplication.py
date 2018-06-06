# -*-coding:Latin-1 -*

import Boite_outils
import os

def affich_table_Multiplication(nombre, max=10):
    """
        Fonction d'affichage de table de multiplication.
        Le second parametre optionnel donne la limite de la table de multiplications.
    """
    i=0
    while i <max:
        print(i+1, " * ", nombre, " = ", ((i+1)*nombre))
        i+=1

def affich_table_Multiplication2(nombre, max=10, multiple=0):
    """
        Fonction d'affichage de table de multiplication.
        Le second parametre optionnel donne la limite de la table de multiplications.
        Le troisième parametre optionnel permet de savoir si le résultat de la multiplication est un multiple de cette valeur.
        Cette fonction est identique Ã  affich_table_Multiplication sauf qu'elle utilise une boucle for
    """
    for i in range(1, max+1):
        ch_resultat = "%s * %s = %s" % (i,nombre,(i*nombre))
        if (multiple > 0):
            if (((i*nombre)%multiple) == 0):
                ch_resultat = ch_resultat + "*"
        print(ch_resultat)

def PGCD(nombre1, nombre2):
    
    if Boite_outils.is_integer(nombre1):
        a = int(nombre1)
    else:
        return "erreur - premier nombre non numerique"
    if Boite_outils.is_integer(nombre2):
        b = int(nombre2)
    else:
        return "erreur - second nombre non numerique"
    if ((a<=0) or (b<=0)):
        return "erreur - une valeur est nulle ou négative"
    if a == b :
        return a
    if a > b :
        a,b = b,a   # a partir de là, a est plus petit que b

    ch_resultat = "Le PGCD de %s et %s est " % (a,b)
    i = b
    j = a
    k = (i%j)
    while (k>0):    #méthode de la division euclidienne
        i,j,k = j,k,(j%k)
    ch_resultat = ch_resultat + "%s" % (j)
    return ch_resultat
        
def PPCM(nombre1, nombre2):
    
    if Boite_outils.is_integer(nombre1):
        a = int(nombre1)
    else:
        return "erreur - premier nombre non numerique"
    if Boite_outils.is_integer(nombre2):
        b = int(nombre2)
    else:
        return "erreur - second nombre non numerique"
    if ((a<=0) or (b<=0)):
        return "erreur - une valeur est nulle ou négative"
    if a == b :
        return a
    if a > b :
        a,b = b,a   # a partir de là, a est plus petit que b
    ch_resultat = "Le PPCM de %s et %s est " % (a,b)
    return ch_resultat

if __name__ == "__main__":
    nombre =  Boite_outils.demande_valeur_numerique("Entrez une valeur")

    #Affichage en utilisant la boucle while
    affich_table_Multiplication(nombre, 20)
    #Idem mais sans passer le paramÃ¨tre optionnel
    affich_table_Multiplication(nombre)
    #Affichage en utilisant la boucle for
    affich_table_Multiplication2(nombre, 15)

    #demande d'aide sur la fonction affich_table_Multiplication()
    help(affich_table_Multiplication)

    os.system("pause")

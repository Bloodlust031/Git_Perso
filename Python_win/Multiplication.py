# -*-coding:Latin-1 -*

from Outils import Boite_outils
import os

def print_fibonacci(nb_val):
    """
    Fonction d'affichage de nb_val de la suite de Fibonacci.
    """
    a,b,c =1,1,0
    while (c < nb_val):
        print(b)
        a,b,c = b,a+b,c+1

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
    iresult = a * b / PGCD(a, b)

    ch_resultat = "Le PPCM de %s et %s est " % (a,b)
    return ch_resultat

def convert_secondes(nbsecondes):
    """
    Cette fonction sert à convertir un nobre de secondes en années/mois/jours/heures/secondes
    """
    val_to_affich = False
    temp = nbsecondes
    nb_s = temp%60
    temp = temp//60
    nb_m = temp%60
    temp = temp//60
    nb_h = temp%24
    temp = temp//24
    #a partir de là, temp donne un nombre entier de jours
    nb_a = temp//365
    temp = temp%365
    nb_M = temp//30
    nb_j = temp%30
    resultat = "%s secondes équivaut à %s années, %s mois, %s jours, %s heures, %s minutes et %s secondes" % (nbsecondes, nb_a, nb_M, nb_j, nb_h, nb_m, nb_s)
    if(nb_a > 0):
        resultat = resultat & "% années" % (nb_a)
        val_to_affich = True
    if((nb_M > 0) or (val_to_affich)): 
        resultat = resultat & "% mois" % (nb_M)
        val_to_affich = True
    if((nb_M > 0) or (val_to_affich)): 
        resultat = resultat & "% mois" % (nb_M)
        val_to_affich = True
    if((nb_M > 0) or (val_to_affich)): 
        resultat = resultat & "% mois" % (nb_M)
        val_to_affich = True
    if((nb_M > 0) or (val_to_affich)): 
        resultat = resultat & "% mois" % (nb_M)
        val_to_affich = True
    if((nb_M > 0) or (val_to_affich)): 
        resultat = resultat & "% mois" % (nb_M)
        val_to_affich = True
    
    
    print(resultat)
    print("toto")
    

if __name__ == "__main__":
    #nombre =  Boite_outils.demande_valeur_numerique("Entrez une valeur")

    #Affichage en utilisant la boucle while
    #affich_table_Multiplication(nombre, 20)
    #Idem mais sans passer le paramÃ¨tre optionnel
    #affich_table_Multiplication(nombre)
    #Affichage en utilisant la boucle for
    #affich_table_Multiplication2(nombre, 15)

    #demande d'aide sur la fonction affich_table_Multiplication()
    #help(affich_table_Multiplication)

    convert_secondes(365001567)


    os.system("pause")

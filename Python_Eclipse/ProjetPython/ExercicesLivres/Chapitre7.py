# -*-coding:Latin-1 -*

'''
Created on 7 nov. 2020

@author: blood
'''

from turtle import *
from dessins_tortue import *

import os
import math

    
def suite_carre():
    up()
    goto(-150, 50)
    i=0
    while i<10:
        down()
        carre(25, 'red',45)
        up()
        forward(30)
        i=i+1

def suite_carre_triangle():
    up()
    goto(-150, 50)
    i=0
    taille = 25
    while i<5:
        down()
        carre(taille, 'red')
        up()
        forward(taille+5)
        down()
        triangle(taille, 'green')
        up()
        forward(taille+5)
        taille = taille + 10
        i=i+1
    
def suite_etoiles():    
    up()
    goto(-150, 50)
    taille = 30
    for i in range(0, 9):
        down()
        etoile5(taille, 'red')
        up()
        forward(taille+5)
        if i<4:
            taille = taille + 10
        else:
            taille = taille - 10
    pass

def suite_carre_etoile6():    
    up()
    goto(-150, 50)
    taille = 30
    for i in range(0, 5):
        down()
        carre(taille, 'red')
        up()
        forward(taille+5)
        down()
        etoile6(taille, 'red')
        up()
        forward(taille+5)
        if i<2:
            taille = taille + 10
        else:
            taille = taille - 10
    pass
    
def suite_carre_etoiles_triangles():    
    up()
    goto(-150, 50)
    taille = 40
    for i in range(0, 9):
        down()
        carre(taille, 'red')
        up()
        forward(taille+5)
        down()
        etoile6(taille, 'red')
        up()
        forward(taille+5)
        down()
        triangle(taille, 'red')
        up()
        forward(taille+5)
        down()
        etoile5(taille, 'red')
        up()
        forward(taille+5)
        taille = taille - 4
    pass
    
    
def ligneCar (n, ca):
    #ecriture d'une ligne de n fois le/les caract�re ca
    i=0
    chaine = ""
    while i<n:
        chaine = chaine+ca
        i=i+1
    print (chaine)

def surfCercle(R):
    #renvoie la surface d'un cercle
    surface = math.pi * R*R
    return surface

def volBoite(x1, x2, x3):
    #renvoie le volume d'une boite dont les dimensions sont pass�es en parametre
    volume = x1*x2*x3
    return volume

def volBoite2(x1=10, x2=10, x3=10):
    #renvoie le volume d'une boite dont les dimensions sont pass�es en parametre
    volume = x1*x2*x3
    return volume

def volBoite3(x1=-1, x2=-1, x3=-1):
    #renvoie le volume d'une boite dont les dimensions sont pass�es en parametre
    if (x1>=0) and (x2>=0) and (x3>=0):
        volume = x1*x2*x3   #Parall�l�pip�de
    elif (x1>=0) and (x2>=0) and (x3<0):
        volume = x1*x1*x2 #Prisme � base carr�e
    elif (x1>=0) and (x2<0) and (x3<0):
        volume = x1*x1*x1   #cube
    else:
        volume = -1

    return volume


def maximum(val1, val2, val3):
    #renvoie la valeur max entre 3 valeurs
    if (val1>val2):
        max = val1
    else:
        max = val2
    if (val3>max):
        max = val3
    return max
        
def compteCar(ca,ch):
    #renvoi le nombre de caract�re ca dans la chaine ch
    nombre = 0
    for i in range (0, len(ch)):
        if ch[i]== ca:
            nombre = nombre+1
    pass
    
    return nombre

def indexMax(suite):
    #envoi la position du plus gros nombre d'une s�rie pass�e en param�tres
    index= 0
    for i in range (0, len(suite)):
        if (suite[i]>suite[index]):
            index = i
    pass
    return index

def nomMois(numero):
    #renvoi le nom du mois correspondant � un numero
    liste_mois = ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Decembre']
    if (numero < 1) or (numero > 12):
        return 'erreur'
    else:
        return liste_mois[numero-1]

def inverse(ch):
    taille = len(ch)
    ch_sortie = ""
    for i in range (0, taille):
        ch_sortie = ch_sortie + ch[taille-i-1]
    return ch_sortie

def compteMots(ph):
    #renvoie le nombre de mots dans une phrase
    nb_mots = 0
    deja_compte = False
    for i in range (0, len(ph)):
        caract= ph[i]
        if(caract.isalpha()):
            if (deja_compte == False):
                deja_compte = True
                nb_mots = nb_mots+1
        else:
            deja_compte = False
    return nb_mots

def changeCar(ch, ca1, ca2, debut = 0, fin = -1):
    #remplace le caract�re ca1 d'une phrase ch par le caract�re ca2 � partir de l'indice debut et jusqu'� l'indice fin
    phrase = ""
    caract=""
    
    if (fin == -1):
        fin = len(ch)
    
    for i in range(0, len(ch)):
        caract = ch[i]
        if (caract == ca1) and (i >= debut) and (i <= fin):
            phrase = phrase + ca2
        else:
            phrase = phrase + caract
        
    return phrase

def eleMax(liste,debut = 0,fin = -1):
    #renvoie la valeur maximale d'une liste � partir de l'indice debut et jusqu'� l'indice fin
    if (fin == -1) or (fin > len(liste)):
        fin = len(liste)
    if(debut>fin):
        valMax = -1000000
    else:
        valMax = liste[debut]
        for i in range(debut, fin):
            if ( valMax < liste[i]):
                valMax = liste[i]
    return valMax

if __name__ == '__main__':
    #suite_carre()
    
    #exercice 7.2
    #ligneCar (6, "de")
    
    #exercice 7.3
    #print(surfCercle(2.5))
    
    #exercice 7.4
    #print(volBoite(5.2, 7.7, 3.3))
    
    #exercice 7.5
    #print(maximum(2,5,4))
    #print(maximum(5,4,2))
    #print(maximum(4,2,5))
    
    #exercice 7.6
    #suite_carre_triangle()
    
    #exercice 7.7
    #suite_etoiles()
    
    #exercice 7.8
    #suite_carre_etoiles()
    #suite_carre_etoiles_triangles()
    
    #exercice 7.9
    #print(compteCar('e','Cette phrase est un exemple'))
     
    #exercice 7.10
    #serie = [5,8,2,1,9,3,6,7]
    #print(indexMax(serie))
    
    #exercice 7.11
    #print(nomMois(4))
     
    #exercice 7.12
    #print(inverse('Tenet'))
    #print(inverse('Coucou'))

    #exercice 7.13
    #print(compteMots("Coucou, je vais bien"))
    #print(compteMots("Je lit l'avenir."))
    #print(compteMots("..Je lit l'avenir "))
    #print(compteMots("Et toi?"))
    
    #exercice 7.14
    #print(volBoite2())
    #print(volBoite2(5.2))
    #print(volBoite2(5.2,3))

    #exercice 7.15
    #print(volBoite3())
    #print(volBoite3(5.2))
    #print(volBoite3(5.2,3))
    #print(volBoite3(5.2,3,7.4))
    
    #exercice 7.16
    #phrase = 'Ceci est une toute petite phrase.'
    #print(changeCar(phrase, ' ', '*'))
    #print(changeCar(phrase, ' ', '*',8,12))
    #print(changeCar(phrase, ' ', '*',12))
    #print(changeCar(phrase, ' ', '*',fin=12))
    
    #exercice 7.17
    serie = [9,3,6,1,7,5,4,8,2]
    print(eleMax(serie))
    print(eleMax(serie,2,5))
    print(eleMax(serie,2))
    print(eleMax(serie,fin=3,debut=1))
    
    os.system("pause") # On met le programme en pause pour éviter qu'il ne se referme (Windows)

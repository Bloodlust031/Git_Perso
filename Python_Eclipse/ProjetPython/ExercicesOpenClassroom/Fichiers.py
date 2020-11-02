# -*-coding:Latin-1 -*
'''
Created on 13 oct. 2020

@author: blood

Manipulation de fichiers textes
'''
import os

def methode1():
    mon_fichier = open("log_tata.txt", "r") #ouverture en mode read
    contenu = mon_fichier.read()
    print(contenu)
    mon_fichier.close()
    mon_fichier = open("log_tata.txt", "a") #ouverture en mode ajout 
    mon_fichier.write("coucou\n")
    mon_fichier.close()
    mon_fichier = open("log_tata.txt", "r")
    contenu = mon_fichier.read()
    print(contenu)
    mon_fichier.close()

def methode2():
    with open("log_tata.txt", "r") as mon_fichier:
        contenu = mon_fichier.read()
        print(contenu)
    with open("log_tata.txt", "a") as mon_fichier:
        mon_fichier.write("coucou\n")
    with open("log_tata.txt", "r") as mon_fichier:
        contenu = mon_fichier.read()
        print(contenu)


if __name__ == '__main__':
    
    os.chdir("D:/temp")
    
    methode2()


    os.system("pause") # On met le programme en pause pour éviter qu'il ne se referme (Windows)
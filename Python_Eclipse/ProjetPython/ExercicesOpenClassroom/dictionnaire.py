# -*-coding:Latin-1 -*

import os

def dico():
    fruits = {"pommes":21, "melons":3, "poires":31}
    print ("cl�s:")
    for cle in fruits.keys():
        print (cle)
    print ("valeurs:")
    for valeur in fruits.values():
        print (valeur)

    print ("contenu du dico")
    for cle,valeur in fruits.items():
        print ("la cl� {} a la valeur {}.".format(cle,valeur))

if __name__ == "__main__":
    print("---------affichage dictionnaire---------")
    dico()

    
    # On met le programme en pause pour �viter qu'il ne se referme (Windows)
    os.system("pause")
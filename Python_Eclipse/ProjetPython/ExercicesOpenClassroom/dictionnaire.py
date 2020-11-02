# -*-coding:Latin-1 -*

import os

def dico():
    fruits = {"pommes":21, "melons":3, "poires":31}
    print ("clés:")
    for cle in fruits.keys():
        print (cle)
    print ("valeurs:")
    for valeur in fruits.values():
        print (valeur)

    print ("contenu du dico")
    for cle,valeur in fruits.items():
        print ("la clé {} a la valeur {}.".format(cle,valeur))

if __name__ == "__main__":
    print("---------affichage dictionnaire---------")
    dico()

    
    # On met le programme en pause pour éviter qu'il ne se referme (Windows)
    os.system("pause"),
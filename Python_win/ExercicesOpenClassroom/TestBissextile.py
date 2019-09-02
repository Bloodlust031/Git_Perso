# -*-coding:Latin-1 -*

import Boite_outils
import os

def b_test_bissextile(ivalue):
    bretour = False
    if ((ivalue % 4) == 0) :
        #c'est peut �tre bissextile
        if ((ivalue % 400) == 0) :
            bretour = True
        elif((ivalue % 100) == 0) :
            bretour = False
        else:
            bretour = True
    return bretour


if __name__ == "__main__":
    iannee = Boite_outils.demande_valeur_numerique("Entrez une ann�e",-4000,100000)

    b_bissextile = b_test_bissextile(iannee)

    if b_bissextile == True:
        print("c'est bissextile")
    else:
        print("ce n'est pas bissextile")
    
    # On met le programme en pause pour éviter qu'il ne se referme (Windows)
    os.system("pause")


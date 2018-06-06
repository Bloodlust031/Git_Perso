# -*-coding:Latin-1 -*

import os # On importe le module os qui dispose de variables 
          # et de fonctions utiles pour dialoguer avec votre 
          # système d'exploitation

# Programme testant si une année, saisie par l'utilisateur, est bissextile ou non

def demande_valeur_numerique(texte):
    """
        Cette fonction permet de demander à l'utilisateur de saisir une valuer numérique et vérifie que le résultat soit bien un entier
        Le texte en parametre sera affiché à l'utilisateur avant sa saisie.
    """
    bvaleur_OK = False
    txt_affich = texte + ": "
    ivaleur = 0
    while not bvaleur_OK:
        txt_input = input(txt_affich)
        try:
            ivaleur =  int(txt_input)
            bvaleur_OK = True
        except:
            print("Valeur non numérique. Veuillez ré-essayer.")
    return ivaleur

def is_integer(texte):
    bvaleur_OK = False
    try:
        ivaleur =  int(texte)
        bvaleur_OK = True
    except:
        bvaleur_OK = False
    return bvaleur_OK
        

def recup_voyelles(texte):
    """
        Cette extrait les voyelles d'un texte
    """
    texte_result = ""
    for lettre in texte:
        if lettre in "AEIOUYaeiouy": # lettre est une voyelle
            texte_result = texte_result + lettre
    return texte_result  

if __name__ == "__main__":
    print("---------test demande_valeur_numerique()---------")
    toto = demande_valeur_numerique("Pour test - entrez une valeur au choix")
    print("valeur numérique:", toto)
    
    print("---------test recup_voyelles()-------------------")
    toto2 = input("Pour test - saisissez un texte:")
    toto2 = recup_voyelles(toto2)
    print("chaine avec que les voyelles:", toto2)
    
    # On met le programme en pause pour �viter qu'il ne se referme (Windows)
    os.system("pause")
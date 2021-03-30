# -*-coding:Latin-1 -*
'''
Created on 23 janv. 2021

@author: blood
'''

class TableauNoir:
    """Classe définissant une surface sur laquelle on peut écrire,
    que l'on peut lire et effacer, par jeu de méthodes. L'attribut modifié
    est 'surface'"""

    
    def __init__(self):
        """Par défaut, notre surface est vide"""
        self.surface = ""
        
    def ecrire(self, message_a_ecrire):
        """Méthode permettant d'écrire sur la surface du tableau.
        Si la surface n'est pas vide, on saute une ligne avant de rajouter
        le message à écrire"""
        if self.surface != "":
            self.surface += "\n"
        self.surface += message_a_ecrire
        
    def lire(self):
        """Cette méthode se charge d'afficher, grâce à print,
        la surface du tableau"""
        print(self.surface)

    def effacer(self):
        """Cette méthode permet d'effacer la surface du tableau"""
        self.surface = ""


if __name__ == '__main__':
    tab = TableauNoir()
    tab.ecrire("Coooool ! Ce sont les vacances !")
    tab.ecrire("Joyeux Noël !")
    tab.lire()
    tab.effacer()
    pass
        
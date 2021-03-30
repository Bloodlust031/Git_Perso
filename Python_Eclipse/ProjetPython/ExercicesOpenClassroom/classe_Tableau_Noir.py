# -*-coding:Latin-1 -*
'''
Created on 23 janv. 2021

@author: blood
'''

class TableauNoir:
    """Classe d�finissant une surface sur laquelle on peut �crire,
    que l'on peut lire et effacer, par jeu de m�thodes. L'attribut modifi�
    est 'surface'"""

    
    def __init__(self):
        """Par d�faut, notre surface est vide"""
        self.surface = ""
        
    def ecrire(self, message_a_ecrire):
        """M�thode permettant d'�crire sur la surface du tableau.
        Si la surface n'est pas vide, on saute une ligne avant de rajouter
        le message � �crire"""
        if self.surface != "":
            self.surface += "\n"
        self.surface += message_a_ecrire
        
    def lire(self):
        """Cette m�thode se charge d'afficher, gr�ce � print,
        la surface du tableau"""
        print(self.surface)

    def effacer(self):
        """Cette m�thode permet d'effacer la surface du tableau"""
        self.surface = ""


if __name__ == '__main__':
    tab = TableauNoir()
    tab.ecrire("Coooool ! Ce sont les vacances !")
    tab.ecrire("Joyeux No�l !")
    tab.lire()
    tab.effacer()
    pass
        
# -*-coding:Latin-1 -*
'''
Created on 2 avr. 2021

@author: blood
'''

class Duree:
    """Classe contenant des durées sous la forme d'un nombre de minutes
    et de secondes"""
    
    def __init__(self, min=0, sec=0):
        """Constructeur de la classe"""
        self.min = min # Nombre de minutes
        self.sec = sec # Nombre de secondes
    def __str__(self):
        """Affichage un peu plus joli de nos objets"""
        return "{0:02}:{1:02}".format(self.min, self.sec)
    
    def __add__(self, objet_a_ajouter):
        """L'objet à ajouter est un entier, le nombre de secondes"""
        nouvelle_duree = Duree()
        # On va copier self dans l'objet créé pour avoir la même durée
        nouvelle_duree.min = self.min
        nouvelle_duree.sec = self.sec
        # On ajoute la durée
        nouvelle_duree.sec += objet_a_ajouter
        # Si le nombre de secondes >= 60
        if nouvelle_duree.sec >= 60:
            nouvelle_duree.min += nouvelle_duree.sec // 60
            nouvelle_duree.sec = nouvelle_duree.sec % 60
        # On renvoie la nouvelle durée
        return nouvelle_duree
    
'''Sachez que sur le même modèle, il existe les méthodes :
    __sub__: surcharge de l'opérateur-;
    __mul__: surcharge de l'opérateur*;
    __truediv__: surcharge de l'opérateur/;
    __floordiv__: surcharge de l'opérateur//(division entière) ;
    __mod__: surcharge de l'opérateur%(modulo) ;
    __pow__: surcharge de l'opérateur**(puissance) ;'''
    
def __iadd__(self, objet_a_ajouter):
        """L'objet à ajouter est un entier, le nombre de secondes"""
        # On travaille directement sur self cette fois
        # On ajoute la durée
        self.sec += objet_a_ajouter
        # Si le nombre de secondes >= 60
        if self.sec >= 60:
            self.min += self.sec // 60
            self.sec = self.sec % 60
        # On renvoie self
        return self 

    
    
if __name__ == '__main__':
    d1 = Duree(12, 8)
    print(d1)
    d2 = d1 + 54 # d1 + 54 secondes
    print(d2)

    d2 += 6
    print(d2)
    
    pass
    
    
    
            
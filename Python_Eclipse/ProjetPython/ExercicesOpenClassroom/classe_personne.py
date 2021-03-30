# -*-coding:Latin-1 -*
'''
Created on 23 janv. 2021

@author: blood
'''

class Personne:
    """Classe d�finissant une personne caract�ris�e par :
    - son nom
    - son pr�nom
    - son �ge
    - son lieu de r�sidence"""

    objets_crees = 0
    
    def __init__(self, nom, prenom):
        """Constructeur de notre classe"""
        self.nom = nom
        self.prenom = prenom
        self.age = 33
        self.lieu_residence = "Paris"
        Personne.objets_crees += 1
        
    
    def _get_lieu_residence(self):
        '''M�thode qui sera appel�e quand on souhaitera acc�der en lecture � l'attribut 'lieu_residence' '''
        print("On acc�de � l'attribut lieu_residence !")
        return self._lieu_residence
    
    def _set_lieu_residence(self, nouvelle_residence):
        '''M�thode appel�e quand on souhaite modifier le lieu de r�sidence'''
        print("Attention, il semble que {} d�m�nage � {}.".format( \
                self.prenom, nouvelle_residence))
        self._lieu_residence = nouvelle_residence
    # On va dire � Python que notre attribut lieu_residence pointe vers une
    # propri�t�
    lieu_residence = property(_get_lieu_residence, _set_lieu_residence)

if __name__ == '__main__':
    bernard = Personne("Micado", "Bernard")
    print (bernard.age)
    jean = Personne("Micado", "Jean")
    print (jean.lieu_residence)
    jean.lieu_residence = "Berlin"
    print (jean.lieu_residence)
    
    pass
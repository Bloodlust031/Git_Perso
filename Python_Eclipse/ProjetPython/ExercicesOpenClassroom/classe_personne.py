# -*-coding:Latin-1 -*
'''
Created on 23 janv. 2021

@author: blood
'''

class Personne:
    """Classe définissant une personne caractérisée par :
    - son nom
    - son prénom
    - son âge
    - son lieu de résidence"""

    objets_crees = 0
    
    def __init__(self, nom, prenom):
        """Constructeur de notre classe"""
        self.nom = nom
        self.prenom = prenom
        self.age = 33
        self.lieu_residence = "Paris"
        Personne.objets_crees += 1
        
    
    def _get_lieu_residence(self):
        '''Méthode qui sera appelée quand on souhaitera accéder en lecture à l'attribut 'lieu_residence' '''
        print("On accède à l'attribut lieu_residence !")
        return self._lieu_residence
    
    def _set_lieu_residence(self, nouvelle_residence):
        '''Méthode appelée quand on souhaite modifier le lieu de résidence'''
        print("Attention, il semble que {} déménage à {}.".format( \
                self.prenom, nouvelle_residence))
        self._lieu_residence = nouvelle_residence
    # On va dire à Python que notre attribut lieu_residence pointe vers une
    # propriété
    lieu_residence = property(_get_lieu_residence, _set_lieu_residence)

if __name__ == '__main__':
    bernard = Personne("Micado", "Bernard")
    print (bernard.age)
    jean = Personne("Micado", "Jean")
    print (jean.lieu_residence)
    jean.lieu_residence = "Berlin"
    print (jean.lieu_residence)
    
    pass
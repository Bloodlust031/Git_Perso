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
        self._lieu_residence = "Paris"
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
        
    def __str__(self):
        '''m�thode pour pourvoir imprimer la classe personne'''
        return "{} {}, ag� de {} ans habitant � {}".format(self.prenom, self.nom, self.age, self._lieu_residence)
        
    def __getattr__(self, nom):
        """Si Python ne trouve pas l'attribut nomm� nom, il appelle
        cette m�thode. On affiche une alerte"""
        print("Alerte ! Il n'y a pas d'attribut {} ici !".format(nom))        
        
#    def __setattr__(self, nom_attr, val_attr):
#        """M�thode appel�e quand on fait objet.nom_attr = val_attr.
#        On se charge d'enregistrer l'objet"""
#        object.__setattr__(self, nom_attr, val_attr)
#        self.enregistrer()        

    def __add__(self, objet_a_ajouter):
        """L'objet � ajouter est un entier, le nombre de secondes"""
        nouvelle_personne = Personne(self.nom,self.prenom)
        nouvelle_personne.age = self.age + objet_a_ajouter
        nouvelle_personne._lieu_residence = self._lieu_residence
        return nouvelle_personne
        
        
    # On va dire � Python que notre attribut lieu_residence pointe vers une propri�t�
    lieu_residence = property(_get_lieu_residence, _set_lieu_residence)

if __name__ == '__main__':
    bernard = Personne("Micado", "Bernard")
    print (bernard.age)
    jean = Personne("Micado", "Jean")
    print (jean.lieu_residence)         #appel � accesseur
    jean.lieu_residence = "Berlin"      #appel au mutateur
    print (jean.lieu_residence)         #appel � accesseur
    
    print(bernard)                      #appel � la m�thode str
    print(jean)
    print(jean.chien)                   #exemple de  __getattr__
     #jean.chien = "cookie"
    print(jean.chien)                   #exemple de  __getattr__
    
    Jeannot = jean + 5
    print(Jeannot)
    
    
    pass
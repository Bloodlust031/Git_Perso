# -*-coding:Latin-1 -*
'''
Created on 4 avr. 2021

@author: blood
'''

class Personne:
    """Classe repr�sentant une personne"""
    def __init__(self, nom):
        """Constructeur de notre classe"""
        self.nom = nom
        self.prenom = "Martin"
    def __str__(self):
        """M�thode appel�e lors d'une conversion de l'objet en cha�ne"""
        return "{0} {1}".format(self.prenom, self.nom)

class AgentSpecial(Personne):
    """Classe d�finissant un agent sp�cial.
    Elle h�rite de la classe Personne"""
    
    def __init__(self, nom, matricule):
        """Un agent se d�finit par son nom et son matricule"""
        # On appelle explicitement le constructeur de Personne :
        Personne.__init__(self, nom)
        self.matricule = matricule
    def __str__(self):
        """M�thode appel�e lors d'une conversion de l'objet en cha�ne"""
        return "Agent {0}, matricule {1}".format(self.nom, self.matricule)
    
    
if __name__ == '__main__':
    agent = AgentSpecial("Fisher", "18327-121")
    print(agent)
    print(agent.prenom)

    
    pass      
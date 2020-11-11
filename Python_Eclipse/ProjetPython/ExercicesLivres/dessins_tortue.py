# -*-coding:Latin-1 -*

'''
Created on 8 nov. 2020

@author: blood
'''

from turtle import *

def carre(taille, couleur, angle=0):
    color(couleur)
    c=0
    right(angle)
    while c<4:
        forward(taille)
        right(90)
        c=c+1

def triangle(taille, couleur, angle=0):
    color(couleur)
    c=0
    right(angle)
    while c<3:
        forward(taille)
        right(120)
        c=c+1

def etoile5(taille, couleur, angle=0):
    color(couleur)
    c=0
    right(angle)
    while c<5:
        forward(taille)
        right(144)
        c=c+1
        
def etoile6(taille, couleur, angle=0):
    triangle(taille, couleur, 0)
    up()
    forward(taille/3)
    left(60)
    forward(taille/3)
    right(120)
    down()
    triangle(taille, couleur, 0)
    

if __name__ == '__main__':
    #etoile5(50, 'red')
    
    etoile6(50, 'red')
    pass
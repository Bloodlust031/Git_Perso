# -*-coding:Latin-1 -*
'''
Created on 16 avr. 2021

@author: blood
'''

import re

def test_rexex(expression, chaine):
    if re.match(expression, chaine):
        print ("la chaine: " + chaine + " contient l'expression: " + expression)
    else:
        print ("la chaine: " + chaine + " ne contient pas l'expression: " + expression)
    
def test_numero_telephone(chaine):
    expression = "^0[0-9]([ .-]?[0-9]{2}){4}$"
    if re.match(expression, chaine):
        print ("la chaine: " + chaine + " est bien un numéro de téléphone valide")
    else:
        print ("la chaine: " + chaine + " n'est pas un numéro de téléphone valide")
        
def taper_numero_telephone():
    chaine = ""
    expression = "^0[0-9]([ .-]?[0-9]{2}){4}$"
    while re.search(expression, chaine) is None:
        chaine = input("Saisissez un numéro de téléphone (valide) :")
    print ("OK: " + chaine)
    


if __name__ == '__main__':
    test_numero_telephone('0609101547')
    test_numero_telephone('06 09 10 15 47')
    test_numero_telephone('06.09.10.15.47')
    
    taper_numero_telephone()
    
    pass
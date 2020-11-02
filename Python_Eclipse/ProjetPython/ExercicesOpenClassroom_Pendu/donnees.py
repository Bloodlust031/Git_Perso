# -*-coding:Latin-1 -*
'''
Created on 15 oct. 2020

@author: blood
'''

import random

liste_mots=['crawlera', 'nomadise', 'preposes', 'fetaient', 'coincees', 'mameluke', 'eventrai', 'engueula', 'cajolait', 'nimbates', 'envasais', 'foliaire', 'cachasse', 'aspirees', 'postiers', 'magister', 'traduits', 'defibree', 'variante', 'pointant', 'licheras', 'cuivreux', 'hisseras', 'troubade', 'egailles', 'salopait', 'tordeuse', 'redorees', 'deterrez', 'aboulons', 'realigne', 'pontasse', 'signales', 'concedat', 'surarmer', 'dussions', 'dejouent', 'parodias', 'enrhumes', 'deferrai', 'noisette', 'secouons', 'eglefins', 'amandaie', 'briffent', 'elidates', 'enfichez', 'ratelais', 'bougnats', 'suririez', 'evitions', 'saccadee', 'rouvrant', 'vanadium', 'routards', 'aveulira', 'procures', 'feutrent', 'manettes', 'globales', 'explosat', 'eclipsez', 'ebrouant', 'colliges', 'relavais', 'gouverna', 'tressera', 'surfondu', 'derasant', 'plaidiez', 'exprimez', 'ruffians', 'recouvra', 'flattons', 'chamoise', 'cithares', 'cokefiez', 'blablata', 'ectasies', 'festonna', 'fervents', 'airerons', 'alteriez', 'lanceuse', 'gringuez', 'reculera', 'remettes', 'plaquera', 'ebaudira', 'pasquins', 'hermines', 'rotateur', 'ramendas', 'pupitres', 'malaxait', 'overdose', 'sacagnas', 'abregent', 'depulpes', 'enfleure', 'compares', 'pausames', 'poignent', 'sterides', 'ironiste', 'gambadez', 'reparait', 'subsiste', 'recriant', 'chapeler', 'flottage', 'enjugues', 'becherai', 'peaucier', 'treuille', 'rembinat', 'pariasse', 'declamai', 'sulfones', 'solistes', 'guidames', 'confinez', 'muteriez', 'ramassez', 'epaulais', 'agreasse', 'abouches', 'etalasse', 'vaccines', 'tassette', 'ancrages', 'enlignee', 'sommerez', 'taurines', 'outrages', 'bedonner', 'chapelat', 'eteignit', 'coupleur', 'engainez', 'incendie', 'fregatez', 'rouvieux', 'calterai', 'minuties', 'redirais', 'pareille', 'moquette', 'renvoyas', 'revoulue']
nb_essais = 15

def get_un_mot():
    mot = ""
    nb_mots = len(liste_mots)
    num_mot = random.randrange(nb_mots)
    mot = liste_mots[num_mot]
    return mot

def get_nb_essais_max():
    return nb_essais

if __name__ == '__main__':
    
    for i in range(0, 400):
        toto = get_un_mot()
        print (toto)
    
    pass
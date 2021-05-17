# -*-coding:Latin-1 -*


'''
Created on 8 mai 2021

@author: blood
'''
import numpy as np

def panda():
    un_panda_numpy = np.array([100, 5, 20, 80]) #Ici, notre panda a des pattes de 100cm, des poils de 5cm en moyenne, une queue de 20cm et un ventre de 80cm de diamètre.
    k = 2
    un_bebe_panda_numpy = un_panda_numpy / k
    print ("un_panda_numpy", un_panda_numpy) 
    print ("un_bebe_panda_numpy", un_bebe_panda_numpy) 


    '''famille_panda = [
        np.array([100, 5  , 20, 80]), # maman panda
        np.array([50 , 2.5, 10, 40]), # bébé panda
        np.array([110, 6  , 22, 80]), # papa panda
    ]'''
    famille_panda = [
        [100, 5  , 20, 80], # maman panda
        [50 , 2.5, 10, 40], # bébé panda
        [110, 6  , 22, 80], # papa panda
    ]
    famille_panda_numpy = np.array(famille_panda)
    print("famille_panda ", famille_panda)
    print("taille des pattes de papa panda ", famille_panda_numpy[2, 0])
    pattes = famille_panda_numpy[:, 0]
    print("taille des pattes de la famille ", pattes) 
    print("somme des tailles des pattes de la famille ", pattes.sum())
    



if __name__ == '__main__':
    panda()
    pass
# -*-coding:Latin-1 -*

'''
Created on 11 nov. 2020

@author: blood
'''

import os
from tkinter import *


def affiche_coucou():
    fen1 = Tk()
    tex1 = Label(fen1, text='Bonjour tout le  monde !',fg='red')
    tex1.pack()
    bou1= Button(fen1,text="Quitter", command = fen1.destroy)
    bou1.pack()
    fen1.mainloop()

    

if __name__ == '__main__':
    affiche_coucou()
    
    os.system("pause") # On met le programme en pause pour éviter qu'il ne se referme (Windows)

# -*-coding:Latin-1 -*

import os
import Outils.Boite_outils
import Multiplication
import math


if __name__ == "__main__":
    #Multiplication.affich_table_Multiplication2(10,20,3)
    
    result = Multiplication.PGCD(56,20)
    print(result)
    result = Multiplication.PGCD(198,256)
    print(result)
    result = Multiplication.PGCD(1236,12)
    print(result)
    result = Multiplication.PGCD(546,23)
    print(result)
    result = Multiplication.PGCD(12,105)
    print(result)
    result = Multiplication.PGCD(15489,156)
    print(result)
    result = Multiplication.PGCD(1723,5)
    print(result)
    result = Multiplication.PGCD(96,76)
    print(result)
    
    Multiplication.print_fibonacci(5)
    
    #help(math.ceil)
    
    
    
    
    #os.system("pause") # On met le programme en pause pour �viter qu'il ne se referme (Windows)
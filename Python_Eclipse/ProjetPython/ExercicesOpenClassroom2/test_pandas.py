# -*-coding:Latin-1 -*

'''
Created on 8 mai 2021

@author: blood
'''

import pandas as pd
import numpy as np

def famille_panda():
    famille_panda = [
        [100, 5  , 20, 80], # maman panda
        [50 , 2.5, 10, 40], # bébé panda
        [110, 6  , 22, 80], # papa panda
    ]
    
    famille_panda_df = pd.DataFrame(famille_panda)
    print("famille_panda_df", famille_panda_df)
    
def famille_panda2():
    
    famille_panda = [
        [100, 5  , 20, 80], # maman panda
        [50 , 2.5, 10, 40], # bébé panda
        [110, 6  , 22, 80], # papa panda
    ]
    famille_panda_numpy = np.array(famille_panda)
    
    famille_panda_df = pd.DataFrame(famille_panda_numpy,
                                    index = ['maman', 'bebe', 'papa'],
                                    columns = ['pattes', 'poil', 'queue', 'ventre'])
    
    print("famille_panda_df", famille_panda_df)
    
    print(famille_panda_df.ventre)
    print(famille_panda_df["ventre"])
    print(famille_panda_df["ventre"].values)
    
    for ligne in famille_panda_df.iterrows():
        index_ligne = ligne[0]
        contenu_ligne = ligne[1]
        print("Voici le panda %s :" % index_ligne)
        print(contenu_ligne)
        print("--------------------")
    


if __name__ == '__main__':
    
    
    famille_panda2()
    
    pass
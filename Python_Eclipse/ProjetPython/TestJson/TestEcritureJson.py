# coding: utf-8

'''
Created on 6 nov. 2020

@author: blood
'''

import os
import json
import time

fichier_log = 'D:/temp/JsonOut.json'

users_data = [
    ("101", "Zorro", "Danseur"),
    ("102", "Hulk", "Footballeur"),
    ("103", "Zidane", "Star"),
    ("104", "Beans", "Epicier"),
    ("105", "Batman", "Veterinaire"),
    ("106", "Spiderman", "Veterinaire"),
    ]

person_dict = {"name": "Bob",
    "languages": ["English", "Fench"],
    "married": True,
    "age": 32
    }

if __name__ == '__main__':
    with open(fichier_log, 'w') as json_file:
        json.dump(users_data, json_file)
        json.dump(person_dict, json_file)
    pass
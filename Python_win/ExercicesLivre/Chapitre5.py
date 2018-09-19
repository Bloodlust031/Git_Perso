# -*-coding:Latin-1 -*

import math

def conversion_degres_radians(degres, minutes ,secondes):
    #1 radian = 180/Pi degrés
    #1 degre = Pi/180 radians
    val_deg = 0.0
    val_deg = secondes
    val_deg = val_deg/60 + minutes
    val_deg = val_deg/60 + degres
    val_rad = val_deg * math.pi /180
    print (val_rad)


if __name__ == "__main__":
    print("chapitre 5: principaux types de données")
    print("5.1: Conversion en radians d'un angle donné en degrés, minutes et secondes")
    conversion_degres_radians(180,0,0)
    print("")
    print("5.2: Conversion en degrés, minutes et secondes d'un angle donné en radians")
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
    print ("un angle de ", degres, "°", minutes, "'", secondes, "'' vaut", val_rad, "radians")

def conversion_radians_degres(val_radians):
    val_angle = val_radians * 180 / math.pi
    val_deg = val_angle // 1
    val_angle = (val_angle - val_deg) * 60
    val_min = val_angle // 1
    val_angle = (val_angle - val_min) * 60
    val_sec = val_angle // 1
    print("un angle de", val_radians, "radians vaut", val_deg, "°", val_min, "' et", val_sec, "''")

def conversion_temperature_Celsius_Fahreinheit(val_cel):
    val_fah = val_cel * 1.8 + 32
    print("une temperature de", val_cel, "°C vaut", val_fah, "°F") 

def conversion_temperature_Fahreinheit_Celsius(val_fah):
    val_cel = (val_fah-32) / 1.8
    print("une temperature de", val_fah, "°F vaut", val_cel, "°C") 

def calcul_interets(val_somme, taux_interets, duree):
    resultat = val_somme
    for i in range(1, duree+1):
        resultat = resultat * (100 + taux_interets) / 100
    resultat = resultat - val_somme
    print("calculs des interets de", val_somme, "euros placés pendant", duree, "ans à ", taux_interets, "%: ", resultat, "euros")
    return resultat

if __name__ == "__main__":
    print("chapitre 5: principaux types de données")
    print("5.1: Conversion en radians d'un angle donné en degrés, minutes et secondes")
    conversion_degres_radians(180,0,0)
    conversion_degres_radians(114.59,0,0)
    conversion_degres_radians(1,0,0)
    conversion_degres_radians(90,0,0)
    conversion_degres_radians(1000,0,0)
    print("")
    print("5.2: Conversion en degrés, minutes et secondes d'un angle donné en radians")
    conversion_radians_degres(math.pi)
    conversion_radians_degres(6)
    conversion_radians_degres(3)
    conversion_radians_degres(2)
    conversion_radians_degres(1)
    print("")
    print("5.3: Conversion en degrés celsius une température en degrés Fahreinheit")
    #Tf = Tc*1.8+32
    conversion_temperature_Celsius_Fahreinheit(0)
    conversion_temperature_Celsius_Fahreinheit(10)
    print("5.3bis: Conversion en degrés Fahreinheit une température en degrés celsius")
    conversion_temperature_Fahreinheit_Celsius(0)
    conversion_temperature_Fahreinheit_Celsius(10)
    print("5.4: Calcul interets")
    calcul_interets(100,4.3,1)
    calcul_interets(100,4.3,2)
    calcul_interets(100,4.3,3)
    calcul_interets(100,4.3,4)
    calcul_interets(100,4.3,5)
    calcul_interets(100,4.3,10)
    calcul_interets(100,4.3,20)
    
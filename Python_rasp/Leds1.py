import time   

# Affichage de texte
print("\n+------------------/ Blink LED /------------------+")
print("|                                                 |")
print("| La LED doit etre reliee au GPIO 18 du Raspberry |")
print("|                                                 |")
print("+-------------------------------------------------+\n")

nbrBlink = int(input("Combien de fois la LED doit clignoter ?\n"))          # Utilisation de la fonction input pour acquerir des informations
tempsAllume = int(input("Combien de temps doit-elle rester allumee ?\n"))
tempsEteint = int(input("Combien de temps doit-elle rester eteinte ?\n"))

i = 0                                                                  # Definition d'une variable type compteur

while i < nbrBlink :
    #GPIO.output(18, True)                                              # Mise a 1 du GPIO 18 (+5V)
    time.sleep(tempsAllume)                                            # On attend le temps defini
    #GPIO.output(18, False)                                             # Mise a zero du GPIO 18 (GND)
    time.sleep(tempsEteint)                                            # ...
    i = i+1
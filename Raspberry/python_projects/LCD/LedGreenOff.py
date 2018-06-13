import RPi.GPIO as GPIO                                               # Importation des librairies qui gerent les ports
import time                                                           # Importation de la librairie temps

GPIO.setwarnings(False)                                               # Mettre sur OFF les alertes (qui sont inutiles)
GPIO.setmode(GPIO.BCM)                                                # BCM : Numero des GPIO (GPIO 18)
GPIO.setup(25, GPIO.OUT)                                              # Definition du port en sortie

GPIO.output(25, False)                                             # Mise a zero du GPIO 18 (GND)


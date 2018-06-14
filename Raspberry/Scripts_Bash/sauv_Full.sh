#!/bin/bash

#script de sauvegarde du répertoire personnel

#Le nom du fichier de sauvegarde est la date du jour au format AAAAMMJJhhmmss
#La clé USB est montée dans le répertoire /media/pi/CLE_RASP

#enregistrement de la date dans la variable DATE en précisant le format
DATE=$(date +"%Y%m%d%H%M%S")

#répertoire personnel de l'utilisateur
REP_PERSONNEL="/home/pi"
echo "Debut de la sauvegarde"
echo "======================"

#Création de l'archive avec compression des fichiers
#la commande tar crée un fichier contenant tous les fichiers du répertoire
#l'option j indique que l'archive doit être compressée
#l'option v indique le mode bavard
#l'option f indique que le nom du fichier suit les options
#l'option c indique qu'il faut créer un nouveau fichier d'archive
tar -cjvf /media/pi/CLE_RASP/Sauvergardes/Full_$DATE.tar.bz2 $REP_PERSONNEL

echo "Sauvegarde terminee" 
echo "======================"

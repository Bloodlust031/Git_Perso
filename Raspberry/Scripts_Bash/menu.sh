#!/bin/bash

#let nombre="99"
sudo python /home/pi/python_projects/Gestled/LedGreenOn.py

until [ "$nombre" = "0" ]; do
echo "Bonjour,"
echo "0.Sortir"
echo "1.MAJ"
echo "2.Lire Temperature"
echo "3.Verif bande passante"
echo "4.Monter les lecteurs Freebox"
echo "5.Sauvegarde complete"
echo "6.Sauvegarde partielle"
#until [ "$nombre" =~ ^[0-6]$ ]; do
#read -t 1 -n 10000 discard
echo "Votre choix?"
read nombre 
#done
if [ $nombre = "0" ]
then
	echo bye
elif [ $nombre = "1" ]
then
	sudo python /home/pi/python_projects/Gestled/LedRedOn.py

	let nombre="99"
	echo "-------------Update---------------"
	sudo apt-get update
	echo "-------------Upgrade--------------"
	sudo apt-get upgrade
	echo "-------------Dist-Upgrade---------"
	sudo apt-get dist-upgrade

	sudo python /home/pi/python_projects/Gestled/LedRedOff.py
elif [ $nombre = "2" ]
then
	let nombre="99"
	/opt/vc/bin/vcgencmd measure_temp
	cat /sys/class/thermal/thermal_zone0/temp
elif [ $nombre = "3" ]
then
	sudo python /home/pi/python_projects/Gestled/LedRedOn.py
	let nombre="99"
	sudo speedtest-cli --simple
	sudo ./speedtest.sh
	sudo python /home/pi/python_projects/Gestled/LedRedOff.py
elif [ $nombre = "4" ]
then
	let nombre="99"
	sudo mount -a
elif [ $nombre = "5" ]
then
	let nombre="99"
	sudo ./sauv_Full.sh
elif [ $nombre = "6" ]
then
	let nombre="99"
	sudo ./sauv_Part.sh
fi
#echo "nombre: $nombre"
#read -t 1 -n 10000 discard
done

sudo python /home/pi/python_projects/Gestled/LedGreenOff.py


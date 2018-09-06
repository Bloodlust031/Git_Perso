# -*-coding:Latin-1 -*




def volume_parallelepipede(longueur, largeur, hauteur):
    retour = 0
    retour = longueur * largeur * hauteur
    return retour

def conversion_secondes(nb_sec):
    print("conversion de", nb_sec, "secondes")
    isec = 0
    imin = 0
    ihour = 0
    ijour = 0
    imois = 0
    iannee = 0
    itemp = nb_sec
    if (itemp > 0):
        isec = itemp % 60
        itemp = itemp // 60
    if (itemp > 0):
        imin = itemp % 60
        itemp = itemp // 60
    if (itemp > 0):
        ihour = itemp % 24
        itemp = itemp // 24
    if (itemp > 0):
        ijour = itemp % 30
        itemp = itemp // 30
    if (itemp > 0):
        imois = itemp % 12
    if (itemp > 0):
        iannee = itemp % 365

    resultat = ""
    if (iannee > 0):
        resultat = resultat  + "années:" + str(iannee)
    if (imois > 0):
        resultat = resultat  + "mois:" + str(imois)
    if (ijour > 0):
        resultat = resultat  + "jours:" + str(ijour)
    if (ihour > 0):
        resultat = resultat  + "heures:" + str(ihour)
    if (imin > 0):
        resultat = resultat  + "minutes:" + str(imin)
    if (isec > 0):
        resultat = resultat  + "secondes:" + str(isec)
    print(resultat)
    
def affich_etoiles(nb_etoiles):
    for i in range(1, nb_etoiles+1):
        resultat = ""
        for j in range(1, i+1):
            resultat = resultat + " *"
        print(resultat)

if __name__ == "__main__":
    resultat = volume_parallelepipede(1,2,3)
    print(resultat)
    
    conversion_secondes(70)
    conversion_secondes(70000)
    
    affich_etoiles(5)
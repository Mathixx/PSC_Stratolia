"""
Premiere étape de ce programme est de determiner à altitude fixée et en partant de certaines coordonnées, la position finale 
après un temps de parcours t
"""
import math
import sys

import pickle
with open("objet_wind_data_2020.pickle", "rb") as f:
    wind_data = pickle.load(f)

#wind_data['data'] contient le tableau numpy 4D

#print(wind_data['metadata'])

"""
for cle in wind_data.keys():
    print(cle)
"""

#print(wind_data['data'])

#for cle in wind_data.keys():
#    print(cle)

"""
Premiere étape de ce programme est de determiner à altitude fixée et en partant de certaines coordonnées, la position finale 
après un temps de parcours t
CF le readMe pour la description de wind_data
Données de vent u (en m.s-1) du sud au nord
Données de vent v (en m.s-1) d'oust en est

ATTENTION, wind_data est un dictionnaire, le tableau qui nous interesse est disponible dans wind_data['data']
"""

def parcours_a_Z(longitude : (int,int), latitude : (int,int), pression : int, tab_vent : dict, tempsI : int, duree : int) -> ((int, int),(int, int))  :
    temps = tempsI
    long = longitude[0]
    lat = latitude[0]
    # ensuite vienne les position au sien de cette enormes cases
    longDetaille = longitude[1]
    latDetaille = latitude[1]

    #echelle d'une case a l'autre (pas sur de la valeur)
    echelle_temp = 6
    while (duree > temps-tempsI) :
        print("je suis passe par la ")
        #on verifie qu'on n'est pas sorti du tableau et si c'est le cas on se remet au bon endroit (ca fait un tour complet)
        long = long%len(tab_vent['data'][0])
        lat = lat%len(tab_vent['data'][0][0])

        # on regarde alors les données de vent en m.s-1
        try:
            ventU = tab_vent['data'][temps][long][lat][pression][0]
        except IndexError as e:
            print(f"Erreur d'index : {e}")
            print("long =", long, "lat =", lat, "pression =", pression, "temps =", temps)
        try:
            ventV = tab_vent['data'][temps][long][lat][pression][1]
        except IndexError as e:
            print(f"Erreur d'index : {e}")
            print("long =", long, "lat =", lat, "pression =", pression, "temps =", temps)

        #je calcule ici le temps necessaire pour passer a l'autre case en focntion des vents
        if (ventU > 0) :
            tempsU =  (280000-latDetaille)/ventU if ventU > 0 else (-latDetaille)/ventU
            tempsU =  math.ceil(tempsU)
        else :
            tempsU = sys.maxsize
        if (ventV > 0) :
            tempsV =  (280000-longDetaille)//ventU if ventU > 0 else (-longDetaille)//ventU
            tempsV =  math.ceil(tempsV)
        else :
            tempsV = sys.maxsize


        if (echelle_temp < min(tempsU,tempsV)) :
            #on a pas change de grosse pendant le temps d'une mesure temporelle
            longDetaille = longDetaille + echelle_temp*ventV
            latDetaille = latDetaille + echelle_temp*ventU

            temps += echelle_temp

        elif (tempsU < tempsV) :
            #on est passé sur une autre case en latitude
            lat = lat+1 if ventU>0 else lat-1
            latDetaille = 0 if ventU>0 else 280000
            #on a quand meme evolué du point de vue de la longitude
            longDetaille = longDetaille + echelle_temp*ventV

            temps += tempsU

        elif (tempsV < tempsU) :
            #on est passé sur une autre case en longitude
            long = long+1 if ventV>0 else long-1
            longDetaille = 0 if ventV>0 else 280000
            #on a quand meme evolué du point de vue de la latitude
            latDetaille = latDetaille + echelle_temp*ventU

            temps += tempsV

        else :
            #cas ou on chnage de case du point de vue de la latitude et de la longtiude en meme temps
            # pas sur que ca arrive un jour mais vasy

            #on est passé sur une autre case en latitude
            lat = lat+1 if ventU>0 else lat-1
            latDetaille = 0 if ventU>0 else 280000
            #on est passé sur une autre case en longitude
            long = long+1 if ventV>0 else long-1
            longDetaille = 0 if ventV>0 else 280000

            temps += tempsV
        
    return ((long, longDetaille), (lat, latDetaille))

def test() :
    #ca c'est completement random
    #il nous faudrait un truc qui donne l'altitude en fonction de la pression et inversement
    pression = 10

    longitudeInit = 45
    latitudeInit = 30
    duree = 3*24
    temps_dep = 0

    print(parcours_a_Z((longitudeInit,longitudeInit), (latitudeInit,latitudeInit), pression, wind_data, temps_dep, duree))
test()






import math
import sys
from parcours import *
from makeTree import *
from Affichage import animation
from datetime import datetime, timedelta


import pickle
with open("objet_wind_data_2020.pickle", "rb") as f:
    wind_data = pickle.load(f)

"""
Coordonnées du 73 boulevard des maréchaux : 
longitude ->  2.211653
latitude -> 48.709859

cela donne dans le tableau : 
longitude : (0, 247705.136)
latitude : (55, 135504.20799999937)


https://www.coordonnees-gps.fr
"""

"""
OBJECTIF : Hippo doit rentrer chez lui ! MAIS il a mal au pied et n'a qu'un ballon stratosphérique à disposition
Trouvons quand partir et affihcons la demarche a suivre !

"""

def hippo_from_cube_to_house(): 
    t = 0
    while True :
        res = Tree_Largeur((2.291007,48.8648915),Node(2.211653,48.709859,(t,0),10,None),24,3*3600,1000,50000,wind_data)
        if res[0] == True :
            print("un chemin a été trouvé :")
            #affichage(res[1])
            break
        t +=1

    coords = []
    for i in range(len(res[1])):
        n = res[1][i]
        coords.append((n.long, n.lat, convPression_altitude(n.p)))

    heure_depart = datetime(2021, 1, 1, 8, 0, 0)
    animation(coords, heure_depart, timedelta(minutes=30) )

hippo_from_cube_to_house()






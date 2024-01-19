#########################
## MODULES NÉCESSAIRES ##
#########################


import math
import sys
from parcours import parcours_a_Z
import pickle
with open("objet_wind_data_2020.pickle", "rb") as f:
    wind_data = pickle.load(f)


class Node :
    def __init__(self, longitude, latitude, temps, pression, prev):
        self.long = longitude
        self.lat = latitude
        self.t = temps
        self.p = pression
        self.prev = prev
    
"""
Programme qui détermine si on peut aller d'un point à un autre et qui renvoie le chemin dans le cas échéant

Entrée :
- position de la destination : longitude, latitude
- position intiale : longitude, latitude, temps, pression
Attention : on commence toujours sur un temps rond (au sens des données de vent ie temps[1] = 0)
- durée de l'exploration (en heures)
Attention : on impose que la durée d'exploration soit un multiple de 6 heures !
- fréquence temporelle des changements de niveau de pression (en secondes)
Attention : on impose que le temps des changements de niveau de pression divise 6 heures !
- précisison (distance à la destination voulue en m)
- limite d'éloignement (distance à la destination à partir de laquelle on abandonne ce chemin). 

Sortie :
- un booléen qui indique si un chemin a été trouvé
- une liste de noeuds qui décrit le chemin trouvé (ou vide sinon)
"""


def Tree_Largeur(destination : (float,float), depart : Node, duree : int, temps_chgmt_pression : int, precision : int, limite_eloignement : int) -> (bool, list(Node)) :

    # On vérifie que le noeud de départ n'a pas de parent.
    if not(depart.prev == None):
        print("Erreur : le point de départ ne doit pas avoir de parent.")
        return 

    # On vérifie qu'on commence sur un temps 'rond'.
    if not(depart.t[1] == 0):
        print("Erreur : on doit commencer sur un temps 'rond', ie temps[1]=0.")
        return 

    # On vérifie que la durée d'exploration est un multiple de six heures.
    if not(duree%6 == 0):
        print("Erreur : la durée d'exploration doit être un multiple de six heures.")
        return

    # On vérifie que le temps des changements de niveau de pression divise six heures.
    if not(21600%temps_chgmt_pression == 0):
        print("Erreur : le temps des changements de niveau de pression doit diviser six heures.")
        return

    # On vérifie que la limite d'éloignement choisie est suffisamment grande pour que l'algorithme fonctionne correctement.
    if distance_destination(destination, depart.long, depart.lat)<limite_eloignement:
        print("Erreur : la limite d'éloignement est inférieure à la distance entre le point de départ et la destination.")
        return 

    # On initialise la liste des points que nous explorons.
    listeP = [depart]

    while True : 
        # On initialise la liste des points qu'on va atteindre.
        listeF = list()
        for point in listeP :
            
            distance = distance_destination(destination, point.long, point.lat)

            # Premier cas : si on est trop loin de la destination on abandonne l'exploration à partir de ce point.
            if distance > limite_eloignement :
                continue

            # Deuxième cas : si on a dépassé la durée d'exploration on arrête et on renvoie False (si le temps est 
            # écoulé pour un point il l'est aussi pour tous les points de la liste). Attention : l'échelle de temps
            # du tableau de vent est de 6 heures. 
            if point.t[0] > temps[0] + duree/6 :
                return False, []

            # Troisième cas : on continue l'exploration. On appelle parcours à Z pour tous les niveaux de pression
            # correspondant à notre point.
            for i in range(0, 17) :

                (a_rencontre_destination, pointF) = parcours_a_Z(destination, Node(point.long, point.lat, point.t, i, point), temps_chgmt_pression, precision, tab_vent)

                # Si on a rencontré la destination, on remonte l'arbre pour reconstituer le chemin complet.
                if a_rencontre_destination:
                    res = [pointF]
                    p = pointF
                    while p.prev != None :
                        p = p.prev
                        res.append(p)
                    return (True, res)
                # Sinon on ajoute le nouveau point à la liste des futurs points. 
                listeF.append(pointF)

        listeP = listeF




'''
Fonction donnant la distance (en m) entre un point donné et la destination

Entrée :
- destination (longitude, latitude)
- position : longitude, latitude

Sortie :
- distance entre le point et la destination (en m)
'''


def distance_destination(destination : (float,float), longitude : float, latitude : float) -> int :
    return 6371000*math.sqrt(((math.cos(destination[1]))*(destination[0]-longitude))**2 + (destination[1]-latitude)**2)





###########
## TESTS ##
###########
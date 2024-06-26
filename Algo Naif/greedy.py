#########################
## MODULES NÉCESSAIRES ##
#########################


import math
import sys

from parcours import parcours_a_Z
from parcours_interpolate import *
from parcours_noise import *
from Node import *
from data_vent import *



#########################
## FONCTION PRINCIPALE ##
#########################


"""
Programme qui détermine si on peut aller d'un point à un autre et qui renvoie le chemin dans le cas échéant.
Approche greedy : on garde à chaque étape temporelle le point le plus proche de la destination.

Entrée :
- position de la destination : longitude, latitude
- position intiale : noeud
Attention : on commence toujours sur un temps rond (temps % 21600 = 0)
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


def greedy(destination : (float,float), depart : Node, duree : int, temps_chgmt_pression : int, precision : int, tab_vent : dict) -> (bool, int, list) :

    # On vérifie que le noeud de départ n'a pas de parent.
    if not(depart.prev == None):
        raise ValueError("Le point de départ ne doit pas avoir de parent.")
        
    # On vérifie qu'on commence sur un temps 'rond'.
    if not(depart.t%21600 == 0):
        raise ValueError("On doit commencer sur un temps 'rond', ie mutliple de six heures.")
    
    temps_initial = case_tps(depart.t)

    # On vérifie que la durée d'exploration est un multiple de six heures.
    if not(duree%6 == 0):
        raise ValueError("La durée d'exploration doit être un multiple de six heures.")
    
    # On vérifie que le temps des changements de niveau de pression divise six heures.
    if not(21600%temps_chgmt_pression == 0):
        raise ValueError("Le temps des changements de niveau de pression doit diviser six heures.")
    
    nombre_d_iterations = (duree//6)*(21600//temps_chgmt_pression)

    # On initialise la liste des points que nous explorons.
    point = depart

    # On initialise le point le plus proche trouvé
    closest_ever = depart
    distance_closest_ever = distance_destination(destination, depart.long, depart.lat)
  
    for count in range(nombre_d_iterations) : 

        # On explore à partir du point actuel.
        for i in range(0, 17) :

                (a_rencontre_destination, point_atteint) = parcours_a_Z_interpolate(destination, Node(point.long, point.lat, point.t, i, point), temps_chgmt_pression, precision, tab_vent)

                # Si on a rencontré la destination, on remonte l'arbre pour reconstituer le chemin complet.
                if a_rencontre_destination:
                    liste = chemin(point_atteint)
                    #affichage_liste(liste)
                    #print("La robustesse du chemin est environ de "+str(robust_dist(liste, destination, temps_chgmt_pression, precision))+" kilomètres")
                    return (True, precision, liste)
                # Sinon on met à jour le point le plus proche atteint.
                if i==0:
                    closest = point_atteint
                    distance_closest = distance_destination(destination, point_atteint.long, point_atteint.lat)
                else:
                    distance_atteint = distance_destination(destination, point_atteint.long, point_atteint.lat)
                    if distance_atteint < distance_closest:
                        closest = point_atteint
                        distance_closest = distance_atteint
        
        # On met à jour le nouveau point d'exploration
        point = closest

        # On met à jour le point le plus proche atteint.
        if (distance_closest < distance_closest_ever):
            closest = point
            distance_closest_ever = distance_closest

    # Dans ce cas on a dépassé la limite temporelle d'exploration.
    #print("On a atteint la limite temporelle d'exploration. Voici le meilleur chemin trouvé : ")
    #print("Distance de la destination = "+str(distance_closest//1000)+ " km.")
    #print("Point final : "+str(point))
    #print("Meilleure distance atteinte = "+str(distance_closest_ever//1000)+ " km.")
    #print("Point le plus proche : "+str(closest_ever)) 
    liste = chemin(point)
    return (False, distance_closest, liste)




###########################
## FONCTIONS AUXILIAIRES ##
###########################







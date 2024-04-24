#########################
## MODULES NÉCESSAIRES ##
#########################


import math
from data_vent import *
import sys
from Node import *


#########################
## FONCTION PRINCIPALE ##
#########################


"""
Ce programme détermine l'évolution du ballon supposé à altitude fixée pendant une fenêtre de temps données. Si pendant cette évolution
le ballon rencontre la destination, on s'arrête et on le signale.

Entrée : 
- destination : longitude, latitude
- position initiale : longitude, latitude, temps, pression
- durée de l'évolution (en secondes)
- précisison (distance à la destination voulue en m)
- données de vent

Sortie :
- booléen indiquant si on a rencontré la destination
- position finale : longitude, latitude, temps, pression
"""


def parcours_a_Z_noise(destination : (float,float), n : Node, temps_chgmt_pression : int, precision : int, tab_vent : dict) -> (bool,Node)  :
    long = n.long
    lat = n.lat
    pression = n.p
    temps = n.t
    temps_restant = temps_chgmt_pression

    # On utilise la précision pour déterminer la fréquence à laquelle on vérifie si on a atteint la destination (temps en secondes). 
    # On estime arbitrairement la vitesse des vents.
    vitesse_moyenne_vents = 7
    temps_test_arrivee = math.ceil(precision/vitesse_moyenne_vents)

     # Constante utile : (rayon de la Terre en m et conversion degrés en radians)
    k = 1000 * 6371 * math.pi / 180

    while(temps_restant>0):

        # On s'assure que les valeurs de longitude et latitude soient dans le bon intervalle.
        (long, lat) = mod(long, lat)

        # On vérifie si on a atteint la destination. Si oui on renvoie notre position.
        if distance_destination(destination,long,lat) <= precision:
            return (True, Node(long, lat, temps+temps_chgmt_pression-temps_restant, pression, n))
        
        # On récupère les données de vent (en m.s-1). Grâce aux hypothèses sur les temps on sait qu'on reste dans la même case temporelle.
        (ventU, ventV) = ventU_ventV_noise(long, lat, temps+temps_chgmt_pression-temps_restant, pression, tab_vent)

        # On met à jour les valeurs de longitude et latitude.
        temps_evolution = min(temps_restant, temps_test_arrivee)
        lat += (temps_evolution*ventV)/k
        long += (temps_evolution*ventU)/k
        temps_restant -= temps_evolution

    # On s'assure que les valeurs de longitude et latitude soient dans le bon intervalle.
    (long, lat) = mod(long, lat)
        
    # On renvoie notre position finale sachant qu'on a pas rencontré la destination. 
    return (False, Node(long, lat, temps+temps_chgmt_pression, pression, n))




########################################
### ROBUSTESSE DES CHEMINS TROUVÉS #####
########################################


'''
Fonction qui évalue la meilleure proximité atteinte par un chemin donné, où chemin signifie choix successifs de niveaux de pression
Entrée : liste de Node, destination
Sortie : meilleure distance atteinte en km
'''


def robust_dist(liste : list, destination : (float,float), temps_chgmt_pression, precision) -> int:
    point = liste[0]
    # On moyenne sur N tests
    N = 1 # À modifier
    somme_best_dist = 0
    for i in range(N):
        best_dist = distance_destination(destination, point.long, point.lat)
        for i in range(len(liste)-1):
            # On fait le choix de pression qui a été fait dans le chemin
            a_atteint_destination, point = parcours_a_Z_noise(destination, Node(point.long, point.lat, point.t, liste[i].p, point), temps_chgmt_pression, precision, wind_data)
            if a_atteint_destination:
                return precision
            else:
                dist = distance_destination(destination, point.long, point.lat)
                best_dist = min(best_dist, dist)
        affichage_liste(chemin(point))
        somme_best_dist += best_dist
    return somme_best_dist/(1000*N)

def heuristique(liste : list, destination : (float,float), temps_chgmt_pression, precision, indice) -> list:
    point = liste[0]
    # On moyenne sur N tests
    N = 1 # À modifier
    somme_best_dist = 0
    for i in range(N):
        best_dist = distance_destination(destination, point.long, point.lat)
        for i in range(len(liste)-1):
            # On fait le choix de pression qui a été fait dans le chemin
            a_atteint_destination, point = parcours_a_Z_noise(destination, Node(point.long, point.lat, point.t, liste[i].p, point), temps_chgmt_pression, precision, wind_data)
            if a_atteint_destination:
                return precision
            else:
                dist = distance_destination(destination, point.long, point.lat)
                best_dist = min(best_dist, dist)
        affichage_liste(chemin(point))
        somme_best_dist += best_dist
    return somme_best_dist/(1000*N)
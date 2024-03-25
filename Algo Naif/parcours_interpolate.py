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


def parcours_a_Z_interpolate(destination : (float,float), n : Node, temps_chgmt_pression : int, precision : int, tab_vent : dict) -> (bool,Node)  :
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
        (ventU, ventV) = ventU_ventV_interpolate(long, lat, temps+temps_chgmt_pression-temps_restant, pression, tab_vent)

        # On met à jour les valeurs de longitude et latitude.
        temps_evolution = min(temps_restant, temps_test_arrivee)
        lat += (temps_evolution*ventU)/k
        long += (temps_evolution*ventV)/k
        temps_restant -= temps_evolution

    # On s'assure que les valeurs de longitude et latitude soient dans le bon intervalle.
    (long, lat) = mod(long, lat)
        
    # On renvoie notre position finale sachant qu'on a pas rencontré la destination. 
    return (False, Node(long, lat, temps+temps_chgmt_pression, pression, n))




##########
## TEST ##
##########


def test_parcours_a_Z_interpolate():
    # Demander à l'utilisateur d'entrer les données d'entrée
    longInit = float(input("Veuillez entrer la longitude du point de départ : "))
    latInit = float(input("Veuillez entrer la latitude du point de départ : "))
    destination_long = float(input("Veuillez entrer la longitude de la destination : "))
    destination_lat = float(input("Veuillez entrer la latitude de la destination : "))
    temps_I = int(input("Veuillez entrer le temps de départ du parcours : "))
    pression = int(input("Veuillez entrer la pression (entier compris entre 0 et 16 inclus) : "))

    # Paramètres de test
    destination = (destination_long, destination_lat)
    n = Node(longitude=longInit, latitude=latInit, temps=temps_I*21600, pression=pression, prev=None)
    temps_chgmt_pression = 6*3600  # Remplacez par la durée du changement de pression souhaitée
    precision = 1000  # Précision de la destination

    # Exécution de la fonction
    result, final_node = parcours_a_Z_interpolate(destination, n, temps_chgmt_pression, precision, wind_data)

    # Affichage des résultats
    if result:
        print("Destination atteinte. Position finale :")
        print(final_node)
    else:
        print("Destination non atteinte. Position finale :")
        print(final_node)

# Exécution du test
#test_parcours_a_Z_interpolate()
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


def parcours_a_Z(destination : (float,float), n : Node, temps_chgmt_pression : int, precision : int, tab_vent : dict) -> (bool,Node)  :
    long = n.long
    lat = n.lat
    pression = n.p
    temps = n.t
    temps_init = case_tps(temps)
    temps_case = n.t%21600
    temps_restant = temps_chgmt_pression
   
    # On utilise la précision pour déterminer la fréquence à laquelle on vérifie si on a atteint la destination (temps en secondes). 
    # On estime arbitrairement la vitesse des vents.
    vitesse_moyenne_vents = 7
    temps_test_arrivee = math.ceil(precision/vitesse_moyenne_vents)
    
    # Constante utile : (rayon de la Terre en m et conversion degrés en radians)
    k = 1000 * 6371 * math.pi / 180

    while (temps_restant > 0) :

        # On s'assure que les valeurs de longitude et latitude soient dans le bon intervalle.
        (long, lat) = mod(long, lat)

        # On vérifie si on a atteint la destination. Si oui on renvoie notre position.
        if distance_destination(destination,long,lat)<=precision:
            return (True, Node(long, lat, temps+temps_chgmt_pression-temps_restant, pression, n))

        # On récupère les données de vent (en m.s-1). Grâce aux hypothèses sur les temps on sait qu'on reste dans la même case temporelle.
        (ventU, ventV) = ventU_ventV(long, lat, temps_init, pression, tab_vent)

        # On calcule le temps nécessaire pour changer de case.
        tempsU, tempsV = tempsU_tempsV(long, lat, ventU, ventV)
        
        temps_evolution = min(temps_restant, temps_test_arrivee)

        case_longitude, case_latitude = case(long, lat)

        # Cas particulier : on est à la limite entre deux case

        # Sous-cas 1 : limite de case en longitude
        if long%2.5 == 0:
            # On regarde les données de vent dans la case adjacente.
            case_longitude_adj = case_longitude -1 if case_longitude>0 else 143
            (ventU_adj, ventV_adj) = ventU_ventV(case_longitude_adj, case_latitude, temps_init, pression, tab_vent)
            if (ventV_adj >= 0 and ventV <= 0) or ventV_adj*ventV == 0:
                # La longitude finale sera celle de la limite de case. On se ramène au cas général en ajustant ventV à 0.
                ventV = 0
                tempsV = sys.maxsize
                if ventU_adj >=0 and ventU <= 0:
                    # On sera au même point à la fin de l'exploration.
                    break
            else:
                # On ajuste simplement le calcul de tempsV et on revient dans le cas général.
                tempsV =  maj_tempsV(long, lat, ventV, ventV_adj)

        # Sous-cas 2 : limite de case en latitude
        if lat%2.5 == 0:
            # On regarde les données de vent dans la case adjacente.
            case_latitude_adj = case_latitude -1 if case_latitude>0 else 0
            (ventU_adj, ventV_adj) = ventU_ventV(case_longitude, case_latitude_adj, temps_init, pression, tab_vent)
            if (ventU_adj >=0 and ventU <= 0) or ventU_adj*ventU == 0:
                # La latitude finale sera celle de la limite de case. On se ramène au cas général en ajustant ventU à 0.
                ventU = 0
                tempsU = sys.maxsize
                if ventV_adj >=0 and ventV <= 0:
                    # On sera au même point à la fin de l'exploration.
                    break
            else:
                # On ajuste simplement le calcul de tempsU et on revient dans le cas général.
                tempsU =  maj_tempsU(long, lat, ventU, ventU_adj)

        # Cas général.

        if (temps_evolution < min(tempsU,tempsV)) :
            lat += (temps_evolution*ventU)/k
            long += (temps_evolution*ventV)/k

            temps_restant -= temps_evolution

        # Deuxième cas : on a changé de case en latitude.
        elif (tempsU < tempsV) :
            # Attention au cas où on passe le pôle Nord (d'où le %72).
            lat = -90 + 2.5*(case_latitude+1) if ventU>0 else -90 + 2.5*case_latitude
            # Il faut quand même mettre à jour la longitude.
            long += (tempsU*ventV)/k

            temps_restant -= tempsU

        # Troisième cas : on a changé de case en longitude.
        elif (tempsV < tempsU) :
            # Attention au cas où on passe le méridien 0 (d'où le %144).
            long = 2.5*(case_longitude+1) if ventV>0 else 2.5 * case_longitude

            # Il faut quand même mettre à jour la latitude.
            lat += (tempsV*ventU)/k

            temps_restant -= tempsV

        # Quatrième cas : on change de case en latitude et en longitude simultanément (très peu probable).
        else :
            lat = -90 + 2.5*(case_latitude+1) if ventU>0 else -90 + 2.5*case_latitude
            long = 2.5*(case_longitude+1) if ventV>0 else 2.5 * case_longitude

            temps_restant -= tempsU


    # On s'assure que les valeurs de longitude et latitude soient dans le bon intervalle.
    (long, lat) = mod(long, lat)
        
    # On renvoie notre position finale sachant qu'on a pas rencontré la destination. 
    return (False, Node(long, lat, temps+temps_chgmt_pression, pression, n))
    



###########################
## FONCTIONS AUXILIAIRES ##
###########################




'''
Fonction qui détermine le temps nécessaire pour changer de case en fonction des données de vent.
Entrée : 
- longitude et latitude
- cases de longitude et de latitude
- vent U et ventV associés
Sortie :
- temps nécessaire pour changer de case
'''


def tempsU_tempsV(long, lat, ventU, ventV) -> (int, int):
    (case_longitude, case_latitude) = case(long, lat)
    # Constante utile : (rayon de la Terre en m et conversion degrés en radians)
    k = 1000 * 6371 * math.pi / 180
    # Ce calcul n'est valable que dans le cas où l'on est pas à une limite de case.
    if (ventU != 0) :
            tempsU = math.ceil(k*(-90+2.5*(case_latitude+1)-lat)/ventU if ventU > 0 else -k*(lat-(-90+2.5*case_latitude))/ventU)
    else :
            tempsU = sys.maxsize
    if (ventV != 0) :
        tempsV =  math.ceil(k*math.cos(lat*math.pi/180)*(2.5*(case_longitude+1)-long)/ventV if ventV > 0 else -k*math.cos(lat*math.pi/180)*(long-2.5*case_longitude)/ventV)
    else :
        tempsV = sys.maxsize
    return (tempsU, tempsV)



'''
Mise à jour de la valeur de tempsU quand on est dans un cas précis
'''

def maj_tempsU(long : float, lat : float, ventU : float, ventU_adj : float) -> int:
    (case_longitude, case_latitude) = case(long, lat)
    # Constante utile : (rayon de la Terre en m et conversion degrés en radians)
    k = 1000 * 6371 * math.pi / 180
    return math.ceil(k*(-90+2.5*(case_latitude+1)-lat)/ventU if ventU > 0 else -k*(lat-(-90+2.5*(case_latitude-1)))/ventU_adj)


'''
Mise à jour de la valeur de tempsU quand on est dans un cas précis
'''

def maj_tempsV(long : float, lat : float, ventV : float, ventV_adj : float) -> int:
    (case_longitude, case_latitude) = case(long, lat)
    # Constante utile : (rayon de la Terre en m et conversion degrés en radians)
    k = 1000 * 6371 * math.pi / 180
    return math.ceil(k*math.cos(lat*math.pi/180)*(2.5*(case_longitude+1)-long)/ventV if ventV > 0 else -k*math.cos(lat*math.pi/180)*(long-2.5*(case_longitude-1))/ventV_adj)






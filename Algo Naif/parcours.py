#########################
## MODULES NÉCESSAIRES ##
#########################


import math
import sys
# For test purposes only
import time


import pickle
with open("objet_wind_data_2020.pickle", "rb") as f:
    wind_data = pickle.load(f)

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
    temps = n.t
    pression = n.p
    temps_init = temps[0]
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
            return (True, Node(long, lat, (temps_init,temps[1]+temps_chgmt_pression-temps_restant), pression, n))

        # On récupère les données de vent (en m.s-1). Grâce aux hypothèses sur les temps on sait qu'on reste dans la même case temporelle.
        (ventU, ventV) = ventU_ventV(long, lat, temps_init, pression, tab_vent)

        (case_longitude, case_latitude) = case(long, lat)


        # On calcule le temps nécessaire pour changer de case.
        if (ventU != 0) :
            tempsU = math.ceil(k*(-90+2.5*(case_latitude+1)-lat)/ventU if ventU > 0 else -k*(lat-(-90+2.5*case_latitude))/ventU)
        else :
            tempsU = sys.maxsize
        if (ventV != 0) :
            tempsV =  math.ceil(k*math.cos(lat*math.pi/180)*(2.5*(case_longitude+1)-long)/ventV if ventV > 0 else -k*math.cos(lat*math.pi/180)*(long-2.5*case_longitude)/ventV)
        else :
            tempsV = sys.maxsize
        

        temps_evolution = min(temps_restant, temps_test_arrivee)

        # Cas particulier : on est à la limite entre deux case

        # Sous-cas 1 : limite de case en longitude
        if long%2.5 == 0:
            # On regarde les données de vent dans la case adjacente.
            (ventU_adj, ventV_adj) = ventU_ventV_adj_long(long, lat, temps_init, pression, tab_vent)
            if (ventV_adj >= 0 and ventV <= 0) or ventV_adj*ventV == 0:
                # La longitude finale sera celle de la limite de case. On se ramène au cas général en ajustant ventV à 0.
                ventV = 0
                tempsV = sys.maxsize
                if ventU_adj >=0 and ventU <= 0:
                    # On sera au même point à la fin de l'exploration.
                    break
            else:
                # On ajuste simplement le calcul de tempsV et on revient dans le cas général.
                tempsV =  math.ceil(k*math.cos(lat*math.pi/180)*(2.5*(case_longitude+1)-long)/ventV if ventV > 0 else -k*math.cos(lat*math.pi/180)*(long-2.5*(case_longitude-1))/ventV)

        # Sous-cas 2 : limite de case en latitude
        if lat%2.5 == 0:
            # On regarde les données de vent dans la case adjacente.
            (ventU_adj, ventV_adj) = ventU_ventV_adj_lat(long, lat, temps_init, pression, tab_vent)
            if (ventU_adj >=0 and ventU <= 0) or ventU_adj*ventU == 0:
                # La latitude finale sera celle de la limite de case. On se ramène au cas général en ajustant ventU à 0.
                ventU = 0
                tempsU = sys.maxsize
                if ventV_adj >=0 and ventV <= 0:
                    # On sera au même point à la fin de l'exploration.
                    break
            else:
                # On ajuste simplement le calcul de tempsU et on revient dans le cas général.
                tempsU =  math.ceil(k*(-90+2.5*(case_latitude+1)-lat)/ventU if ventU > 0 else -k*(lat-(-90+2.5*(case_latitude-1)))/ventU)
                

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
        
    # On renvoie notre position finale sachant qu'on a pas rencontré la destination. On vérifie si on a atteint une nouvelle 
    # fenêtre de six heures.
    if temps[1]+temps_chgmt_pression>=21600:
        return (False, Node(long, lat, (temps_init+1, 0), pression, n))
    return (False, Node(long, lat, (temps_init, temps[1]+temps_chgmt_pression), pression, n))
    


###########################
## FONCTIONS AUXILIAIRES ##
###########################


'''
Fonction donnant la distance (en m) entre un point donné et la destination

Entrée :
- destination (longitude, latitude)
- position : longitude, latitude

Sortie :
- distance entre le point et la destination (en m)
'''


def distance_destination(destination : (float,float), long : float, lat : float) -> int:
    # Convertir les coordonnées degrés en radians
    dest_lat, dest_long, lat, long = map(math.radians, [destination[1], destination[0], lat, long])

    # Calcul des différences de coordonnées
    ecart_lat = lat - dest_lat
    ecart_long = long - dest_long

    # Formule de la haversine pour calculer la distance
    a = math.sin(ecart_lat/2)**2 + math.cos(dest_lat) * math.cos(lat) * math.sin(ecart_long/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    # Rayon de la Terre en mètres (environ 6371 km)
    rayon = 6371000

    # Calcul de la distance et conversion en entier
    distance = int(rayon * c)

    return distance




'''
Fonction auxiliaire qui détermine la case dans laquelle on se trouve en fonction de la longitude et de la latitude.

Entrée :
- position : longitude, latitude

Sortie :
- coordoonées de la case dans laquelle on se situe
'''


def case(longitude : float, latitude : float) -> (int, int):
    return (int(longitude/2.5), int((latitude+90)/2.5))


'''
Fonction auxiliare qui récupère les données de vent

Entrée :
- position : longitude, latitude, temps, pression
- données de vent

Sortie :
- vent sud-nord (ventU) en m.s-1
- vent ouest-est (ventV) en m.s-1
'''


def ventU_ventV(longitude : float, latitude : float, temps : int, pression : int, tab_vent: dict) -> (int,int):
    (case_longitude, case_latitude) = case(longitude, latitude)
    try:
        ventU = tab_vent['data'][temps][pression][case_longitude][case_latitude][0]
    except IndexError as e:
        print(f"Erreur d'index : {e}")
        print("long =", case_longitude, "lat =", case_latitude, "temps =", temps,"pression =", pression)
    try:
        ventV = tab_vent['data'][temps][pression][case_longitude][case_latitude][1]
    except IndexError as e:
        print(f"Erreur d'index : {e}")
        print("long =", case_longitude, "lat =", case_latitude, "temps =", temps, "pression =", pression)
    return (ventU,ventV)



'''
Fonction qui récupère les données de vent dans la case adjacente en latitude.
Entrée :
- position : longitude, latitude, temps, pression
- données de vent

Sortie :
- vent sud-nord (ventU) en m.s-1
- vent ouest-est (ventV) en m.s-1
'''


def ventU_ventV_adj_lat(longitude : float, latitude : float, temps : int, pression : int, tab_vent: dict) -> (int,int):
    (case_longitude, case_latitude) = case(longitude, latitude)
    # On va chercher la case située en dessous pour la latitude.
    case_latitude = case_latitude -1 if case_latitude>0 else 0
    try:
        ventU = tab_vent['data'][temps][pression][case_longitude][case_latitude][0]
    except IndexError as e:
        print(f"Erreur d'index : {e}")
        print("long =", case_longitude, "lat =", case_latitude, "temps =", temps,"pression =", pression)
    try:
        ventV = tab_vent['data'][temps][pression][case_longitude][case_latitude][1]
    except IndexError as e:
        print(f"Erreur d'index : {e}")
        print("long =", case_longitude, "lat =", case_latitude, "temps =", temps, "pression =", pression)
    return (ventU,ventV)



'''
Fonction qui récupère les données de vent dans la case adjacente en longitude.
Entrée :
- position : longitude, latitude, temps, pression
- données de vent

Sortie :
- vent sud-nord (ventU) en m.s-1
- vent ouest-est (ventV) en m.s-1
'''


def ventU_ventV_adj_long(longitude : float, latitude : float, temps : int, pression : int, tab_vent: dict) -> (int,int):
    (case_longitude, case_latitude) = case(longitude, latitude)
    # On va chercher la case située en dessous pour la longitude.
    case_longitude = case_longitude -1 if case_latitude>0 else 143
    try:
        ventU = tab_vent['data'][temps][pression][case_longitude][case_latitude][0]
    except IndexError as e:
        print(f"Erreur d'index : {e}")
        print("long =", case_longitude, "lat =", case_latitude, "temps =", temps,"pression =", pression)
    try:
        ventV = tab_vent['data'][temps][pression][case_longitude][case_latitude][1]
    except IndexError as e:
        print(f"Erreur d'index : {e}")
        print("long =", case_longitude, "lat =", case_latitude, "temps =", temps, "pression =", pression)
    return (ventU,ventV)

'''
Fonction qui recentre les valeurs de long et lat dans les bons intervalles
Entrée : long, lat
Sortie : long, lat
'''

def mod(long: float, lat : float) -> (float, float):
    if lat<-90:
        lat = -180-lat
    if lat>90:
        lat = 180-lat
    return ((long+360)%360,lat)


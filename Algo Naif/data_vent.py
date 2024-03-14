#########################
## MODULES NÉCESSAIRES ##
#########################


import pickle
import math
import random


############################
## EXTRACTION DES DONNÉES ##
############################


with open("objet_wind_data_2020.pickle", "rb") as f:
    wind_data = pickle.load(f)



###########################
## FONCTIONS PRINCIPALES ##
###########################



'''
Fonction auxiliare qui récupère les données de vent

Entrée :
- position : longitude, latitude, temps, pression
- données de vent

Sortie :
- vent sud-nord (ventU) en m.s-1
- vent ouest-est (ventV) en m.s-1
'''


def ventU_ventV(long : float, lat : float, temps : int, pression : int, tab_vent: dict) -> (float,float):
    (case_longitude, case_latitude) = case(long, lat)
    case_temps = case_tps(temps)
    try:
        ventU = tab_vent['data'][case_temps][pression][case_longitude][case_latitude][0]
    except IndexError as e:
        print(f"Erreur d'index : {e}")
        print("long =", case_longitude, "lat =", case_latitude, "case_temps =", case_temps,"pression =", pression)
    try:
        ventV = tab_vent['data'][case_temps][pression][case_longitude][case_latitude][1]
    except IndexError as e:
        print(f"Erreur d'index : {e}")
        print("long =", case_longitude, "lat =", case_latitude, "case_temps =", case_temps, "pression =", pression)
    return (ventU,ventV)




'''
Fonction auxiliare qui récupère les données de vent avec interpolation linéaire des données dans les huit cases autour. Les vents renvoyés sont
tronqués à la deuxième décimale.

Entrée :
- position : longitude, latitude, temps, pression
- données de vent

Sortie :
- vent ouest-est (ventU) en m.s-1
- vent sud-nord (ventV) en m.s-1
'''


def ventU_ventV_interpolate(long : float, lat : float, temps : int, pression : int, tab_vent: dict) -> (float,float):
    (case_longitude, case_latitude) = case(long, lat)
    case_temps = case_tps(temps)
    dest = (long, lat) 

    LG = [case_longitude*2.5, case_long(mod_long(long + 2.5))*2.5]
    LT = [-90+case_latitude*2.5, -90+case_lat(mod_lat(lat + 2.5))*2.5]
    TPS = [case_temps, case_temps+1]

    numU = 0
    numV = 0
    den = 0

    for lg in LG:
        for lt in LT:
            for tps in TPS:
                ventU, ventV = ventU_ventV(lg, lt, tps, pression, wind_data)
                dist = distance_destination(dest, lg, lt)
                numU += dist*ventU
                numV += dist*ventV
                den += dist
    
    return math.floor(numU/den * 100) / 100, math.floor(numV/den * 100) / 100



'''
Fonction qui donne des données de vent interpolées mais perturbées par une gaussienne de paramètres fixés.
Entrée :
- position : longitude, latitude, temps, pression
- données de vent

Sortie :
- vent ouest-est (ventU) en m.s-1
- vent sud-nord (ventV) en m.s-1
'''
    

def ventU_ventV_noise(long : float, lat : float, temps : int, pression : int, tab_vent: dict) -> (float,float):
    noiseU = random.normalvariate(0, 1) # Paramètres à modifier !!!
    noiseV = random.normalvariate(0, 1) # Paramètres à modifier !!!
    ventU, ventV = ventU_ventV_interpolate(long, lat, temps, pression, wind_data)
    return ventU+noiseU, ventV+noiseV






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
    return (case_long(longitude), case_lat(latitude))

def case_long(longitude : float) -> int:
    return int(longitude/2.5)

def case_lat(latitude : float) -> int:
    return int((latitude+90)/2.5)

def case_tps(temps : int) -> int:
    return temps//21600


'''
Fonction qui recentre les valeurs de long et lat dans les bons intervalles
Entrée : long, lat
Sortie : long, lat
'''

def mod(long: float, lat : float) -> (float, float):
    return (mod_long(long), mod_lat(lat))

def mod_long(long : float) -> float:
    return (long+360)%360

def mod_lat(lat : float) -> float:
    if lat<-90:
        lat = -180-lat
    if lat>90:
        lat = 180-lat
    return lat



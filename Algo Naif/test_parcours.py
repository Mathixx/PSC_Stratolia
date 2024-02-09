#########################           ##################
## MODULES NÉCESSAIRES ##           ## VERSION TEST ##
#########################           ##################


import math
import sys
import time


import pickle
with open("objet_wind_data_2020.pickle", "rb") as f:
    wind_data = pickle.load(f)

from Node import *


#########################           ##################
## FONCTION PRINCIPALE ##           ## VERSION TEST ##       
#########################           ##################


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
        time.sleep(0.1)

        (long, lat) = ajuste(long, lat)

        # On récupère les données de vent (en m.s-1). Grâce aux hypothèses sur les temps on sait qu'on reste dans la même case temporelle.
        (ventU, ventV) = ventU_ventV(long, lat, temps_init, pression, tab_vent)

        # TEST
        print("temps_test_arrivee : "+str(temps_test_arrivee) )
        print("vent U : "+str(ventU)+", vent V : "+str(ventV))


        
        print("long :",long," et lat : ",lat)
        # On vérifie si on a atteint la destination. Si oui on renvoie notre position.
        if distance_destination(destination,long,lat)<=precision:
            return (True, Node(long, lat, (temps_init,temps[1]+temps_chgmt_pression-temps_restant), pression, n))

        
        (case_longitude, case_latitude) = case(long, lat)
        
        # On calcule le temps nécessaire pour changer de case.
        # ATTENTION : Disjoncion de cas : Quand on souhaite calculer tempsU/tempsV et que l'on se situe deja sur une limite de case
        if (ventU != 0) :
            if (lat%2.5) != 0 :
                tempsU = k*(-90+2.5*(case_latitude+1)-lat)/ventU if ventU > 0 else -k*(lat-(-90+2.5*case_latitude))/ventU
            else :
                tempsU =  k*(-90+2.5*(case_latitude+1)-lat)/ventU if ventU > 0 else -k*(lat-(-90+2.5*(case_latitude-1)))/ventU
            tempsU =  math.ceil(tempsU)
        else :
            tempsU = sys.maxsize
        if (ventV != 0) :
            if (long%2.5) != 0:
                tempsV =  k*math.cos(lat*math.pi/180)*(2.5*(case_longitude+1)-long)/ventV if ventV > 0 else -k*math.cos(lat*math.pi/180)*(long-2.5*case_longitude)/ventV
            else :
                tempsV =  k*math.cos(lat*math.pi/180)*(2.5*(case_longitude+1)-long)/ventV if ventV > 0 else -k*math.cos(lat*math.pi/180)*(long-2.5*(case_longitude-1))/ventV
            tempsV =  math.ceil(tempsV)
        else :
            tempsV = sys.maxsize

       
        # Premier cas : on a pas changé de case pendant le temps d'évolution.
        temps_evolution = min(temps_restant, temps_test_arrivee)

        # A supprimer utile pour les tests seulemet:
        print("temps evolution : "+str(temps_evolution))
        print("temps U : " +str(tempsU))
        print("temps V : " +str(tempsV))

        if (temps_evolution < min(tempsU,tempsV)) :
            print(1)
            lat += (temps_evolution*ventU)/k
            long += (temps_evolution*ventV)/k

            temps_restant -= temps_evolution

        # Deuxième cas : on a changé de case en latitude.
        elif (tempsU < tempsV) :
            print(2)
            # Attention au cas où on passe le pôle Nord (d'où le %72).
            lat = -90 + 2.5*((case_latitude+1)%72) if ventU>0 else -90 + 2.5*case_latitude
            # Il faut quand même mettre à jour la longitude.
            long += (tempsU*ventV)/k

            temps_restant -= tempsU

        # Troisième cas : on a changé de case en longitude.
        elif (tempsV < tempsU) :
            print(3)
            # Attention au cas où on passe le méridien 0 (d'où le %144).
            long = 2.5*((case_longitude+1)%144) if ventV>0 else 2.5 * case_longitude

            # Il faut quand même mettre à jour la latitude.
            lat += (tempsV*ventU)/k

            temps_restant -= tempsV

            

        # Quatrième cas : on change de case en latitude et en longitude simultanément (très peu probable).
        else :
            # print(4)
            lat = -90 + 2.5*((case_latitude+1)%72) if ventU>0 else -90 + 2.5*case_latitude
            long = 2.5*((case_longitude+1)%144) if ventV>0 else 2.5 * case_longitude

            temps_restant -= tempsU

        
    # On renvoie notre position finale sachant qu'on a pas rencontré la destination. On vérifie si on a atteint une nouvelle 
    # fenêtre de six heures.
    if temps[1]+temps_chgmt_pression>=21600:
        return (False, Node(long, lat, (temps_init+1, 0), pression, n))
    return (False, Node(long, lat, (temps_init, temps[1]+temps_chgmt_pression), pression, n))




###########################         ##################
## FONCTIONS AUXILIAIRES ##         ## VERSION TEST ##
###########################         ##################



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
Fonction qui ajuste la valeur de la longitude et de la latitude dans le cas où on est passé par un pôle ou le méridien zéro.
Entrée et sortie : longitude(float), latitude(float)
'''


def ajuste(long : float, lat : float) -> (float, float):
    # On ajuste si on est passé par un pôle ou le méridien 0.
        if (long<0):
            long += 360
        if (long>360):
            long -= 360
        if (lat < -90):
            lat = -180 - lat
        if (lat > 90):
            lat = 180 - lat
        return (long, lat)




###########
## TESTS ##       
###########



def test_parcours_a_Z():
    # Demander à l'utilisateur d'entrer les données d'entrée
    longInit = float(input("Veuillez entrer la longitude du point de départ : "))
    latInit = float(input("Veuillez entrer la latitude du point de départ : "))
    destination_long = float(input("Veuillez entrer la longitude de la destination : "))
    destination_lat = float(input("Veuillez entrer la latitude de la destination : "))
    temps_I = int(input("Veuillez entrer le temps de départ du parcours : "))
    temps_sec = int(input("Veuillez entrer le temps de départ du parcours au sein de la case temporelle : "))
    pression = int(input("Veuillez entrer la pression (entier compris entre 0 et 16 inclus) : "))

    # Paramètres de test
    destination = (destination_long, destination_lat)
    n = Node(longitude=longInit, latitude=latInit, temps=(temps_I, temps_sec), pression=pression, prev=None)
    temps_chgmt_pression = 3*3600  # Remplacez par la durée du changement de pression souhaitée
    precision = 1000  # Précision de la destination

    # Exécution de la fonction
    result, final_node = parcours_a_Z(destination, n, temps_chgmt_pression, precision, wind_data)

    # Affichage des résultats
    if result:
        print("Destination atteinte. Position finale :")
        print(final_node)
    else:
        print("Destination non atteinte. Position finale :")
        print(final_node)

# Exécution du test
test_parcours_a_Z()







    



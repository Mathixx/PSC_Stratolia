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
    # Pour les conventions : cf. README.
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


    #MODIF TOI TU LE METS LA, MOI JE LE MET DANS LA BOUCLE 
    # CAR JE CONSIDERE QU'ON ARRETE PAS LA RECHERCHE APRES UNE ITERATION DE LA BOUCLE
    # On récupère les données de vent (en m.s-1).
    (ventU, ventV) = ventU_ventV(long, lat, temps_init, pression, tab_vent)

    # Grace aux conventions faites sur les temps de changement de pression, on sait qu'on ne va pas passer dans une nouvelle 
    # fenêtre de six heures au cours du parcours. Ainsi, sauf changement de case, il ne faut pas récupérer de nouvelles données de 
    # vent.

    while (temps_restant > 0) :
        #time.sleep(0.1)

        # On récupère les données de vent (en m.s-1).
        (ventU, ventV) = ventU_ventV(long, lat, temps_init, pression, tab_vent)

        #A supprimer utile pour les tests seulemet:
        # print("temps_test_arrivee : "+str(temps_test_arrivee) )
        # print("vent U : "+str(ventU)+", vent V : "+str(ventV))


        
        # print("long :",long," et lat : ",lat)
        # On vérifie si on a atteint la destination. Si oui on renvoie notre position.
        if distance_destination(destination,long,lat)<=precision:
            return (True, Node(long, lat, (temps_init,temps[1]+temps_chgmt_pression-temps_restant), pression, n))

        # On calcule le temps nécessaire (en secondes) pour passer à une autre case en fonction des vents. 
        # cf README pour les valeurs numériques.
        (case_longitude, case_latitude) = case(long, lat)
        

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
        # print("temps evolution : "+str(temps_evolution))
        # print("temps U : " +str(tempsU))
        # print("temps V : " +str(tempsV))

        if (temps_evolution < min(tempsU,tempsV)) :
            # print(1)
            lat += (temps_evolution*ventU)/k
            long += (temps_evolution*ventV)/k

            temps_restant -= temps_evolution

        # Deuxième cas : on a changé de case en latitude.
        elif (tempsU < tempsV) :
            # print(2)
            # Attention au cas où on passe le pôle Nord (d'où le %72).
            lat = -90 + 2.5*((case_latitude+1)%72) if ventU>0 else -90 + 2.5*case_latitude
            # Il faut quand même mettre à jour la longitude.
            long += (tempsU*ventV)/k

            temps_restant -= tempsU

        # Troisième cas : on a changé de case en longitude.
        elif (tempsV < tempsU) :
            # print(3)
            # Attention au cas où on passe le méridien 0 (d'où le %144).
            long = 2.5*((case_longitude+1)%144) if ventV>0 else 2.5 * case_longitude

            # Il faut quand même mettre à jour la latitude.
            lat += (tempsV*ventU)/k

            temps_restant -= tempsV

            # A supprimer utile pour les tests seulemet:
            # print("nouvelle longitude : "+ str(long))
            # print("nouvelle latitude : "+ str(lat))

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
    


'''
Fonction donnant la distance (en m) entre un point donné et la destination

Entrée :
- destination (longitude, latitude)
- position : longitude, latitude

Sortie :
- distance entre le point et la destination (en m)
'''


def distance_destination(destination : (float,float), long : float, lat : float) -> int :
    # Constante utile : (rayon de la Terre en m et conversion degrés en radians)
    k = 1000 * 6371 * math.pi / 180
    
    dest_long = destination[0]
    dest_lat = destination[1]
    return int(k*math.sqrt(((math.cos(math.pi*dest_lat/180))*(dest_long-long))**2 + (dest_lat-lat)**2))


def check_type(arg):
    if isinstance(arg, float):
        print("It's a float!")
    elif isinstance(arg, int):
        print("It's an int!")
    elif isinstance(arg, str):
        print("It's a string!")
    elif isinstance(arg, tuple):
        print("It's a tuple")
    else:
        print("It's some other type!")


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
        ventU = tab_vent['data'][temps][case_longitude][case_latitude][pression][0]
    except IndexError as e:
        print(f"Erreur d'index : {e}")
        print("long =", case_longitude, "lat =", case_latitude, "temps =", temps,"pression =", pression)
    try:
        ventV = tab_vent['data'][temps][case_longitude][case_latitude][pression][1]
    except IndexError as e:
        print(f"Erreur d'index : {e}")
        print("long =", case_longitude, "lat =", case_latitude, "temps =", temps, "pression =", pression)
    return (ventU,ventV)



###########
## TESTS ##       A MODIFIER !!!!!
###########



def test1_parcours_a_Z() :
    # Test de base
    # Paramètres modifiables au besoin
    print(parcours_a_Z((1.5,50),Node(2.211653,48.709859,(50,0),10,None),3*3600,5000,wind_data))

# test1_parcours_a_Z()

#print(case(2.5, 48.7))
#print(case(3, 48.7))

'''
Palaiseau
2.211653
48.709859
'''
"""
print(ventU_ventV(2.5, 48.7, 0, 10, wind_data))
print(ventU_ventV(3, 48.7, 0, 10, wind_data))
"""

def test2_parcours_a_Z() :
    # Test de trajectoires approfondi
    # Choix des paramètres libres
    longInit = input("Veuillez entrer la longitude du point de départ (int) : ")
    longInit = int(longInit)
    latInit = input("Veuillez entrer la latitude (y) de la case de départ (int) : ")
    latInit = int(latInit)
    longDetailleeInit = input("Veuillez entrer la longitude détaillée (y) (float - doit correspondre avec la case) : ")
    longDetailleeInit = int(longDetailleeInit)
    latDetailleeInit = input("Veuillez entrer la latitude détaillée (y) (float - doit correspondre avec la case) : ")
    latDetailleeInit = int(latDetailleeInit)
    pression = input("Veuillez entrer la pression (int compris entre 0 et 16 inclus) : ")
    pression = int(pression)
    duree = input("Veuillez entrer la durée du parcours (int) : ")
    duree = int(duree)
    temps_I = input("Veuillez entrer le temps de départ du parcours (int) : ")
    temps_I = int(temps_I)
    temps_sec = input("Veuillez entrer le temps de départ du parcours au sein de la case temporelle (int compris entre 0 et 21599) : ")
    temps_sec = int(temps_I)

    


#print(wind_data['metadata'])
print(len(wind_data['data']))

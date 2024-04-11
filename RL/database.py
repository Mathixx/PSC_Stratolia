#########################
## MODULES NECESSAIRES ##
#########################

import datetime as dt
import sys

sys.path.append('/Users/mathiasperez/Documents/GitHub/PSC_Stratolia/Algo Naif')
from data_vent import *
from villes import *
from exploration import *
from greedy import *
from selection_search import *
from Node import *

import math
import pickle
import random
import csv

############################
## EXTRACTION DES DONNÉES ##
############################


with open("objet_wind_data_2020.pickle", "rb") as f:
   wind_data = pickle.load(f)


############################
## FONCTIONS AUXILIAIRES  ##
############################

def generate_random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + dt.timedelta(days=random_number_of_days)
    hr  = random.randrange(0, 24, 6)
    random_time = dt.time(hour=hr, minute=0, second=0, microsecond=0, tzinfo=None, fold=0)
    return dt.datetime.combine(random_date, random_time)

####################################
## CREATION DE LA BASE DE DONNÉES ##
####################################

def random_path(liste_villes) :
    """
    Fonction qui génère un chemin aléatoire entre 2 villes prise au hasard de la liste
    """
    path = []
    ville_depart = choisir_ville_au_hasard(liste_villes)
    ville_destination = choisir_ville_au_hasard(liste_villes)

    distance_max = 5000000 # 5000 km

    while(ville_destination.nom == ville_depart.nom or distance_destination((ville_destination.long, ville_destination.lat), ville_depart.long, ville_depart.lat) > distance_max):
        ville_destination = choisir_ville_au_hasard(liste_villes)
    
    temps = (generate_random_date(dt.datetime(2020, 1, 1), dt.datetime(2020, 10, 30))-dt.datetime(2020, 1, 1)).total_seconds()
    #Convert it in an integer
    temps = int(temps)
    depart = Node(ville_depart.long, ville_depart.lat, temps, 16, None) #long, lat, temps, pression, None


    print("Ville de départ : ", ville_depart.nom)
    print("Ville de destination : ", ville_destination.nom)
    ville_arr = ville_destination
    ville_destination = (ville_destination.long, ville_destination.lat)
    
    technique = random.choice(["greedy"])
    #print(technique)
    if technique == "greedy":
        duree = 120
        temps_chgmt_pression = 3600
        precision = 10000

        found, _ , path = greedy(ville_destination, depart, duree, temps_chgmt_pression, precision, wind_data)
        if found :
            return found, ville_depart, ville_arr ,path
    elif technique == "selection":
        duree = 120
        temps_chgmt_pression = 6*3600
        precision = 10000
        eloignement = 1.2

        found, _ , path = N_closest(ville_destination, depart, duree, temps_chgmt_pression, precision,eloignement, wind_data)
        if found :
            return found, ville_depart, ville_arr ,path
    elif technique == "exploration":
        duree = 120
        temps_chgmt_pression = 6*3600
        precision = 10000

        found, _ , path = wide_search(ville_destination, depart, duree, temps_chgmt_pression, precision, wind_data)
        if found :
            return found, ville_depart, ville_arr,path
    
    return found ,ville_depart, ville_destination, []


"""
        Action 0 : You do nothing and let the balloon follow the wind for temps_exploration seconds
        Action 1 : You push the balloon upwards (goes up in altitude) (instanneous action)
        Action 2 : You push the balloon downwards (goes down in altitude) (instanneous action)
"""

def create_data( path : list) :
    """
    Fonction qui crée un élément de la base de données à partir d'un chemin
    """
    data = []

    i = 0
    while (i+1 < len(path)):
        delta_altitude = path[i].p - path[i+1].p
        if (delta_altitude == 0):
            # Le ballon est à la même altitude, il a suivi les vents
            if (path[i].t == path[i+1].t):
                # Le ballon n'a pas bougé, on ne le prend pas en compte
                i += 1
                continue
            else:
                # Le ballon a bougé, on prend en compte le changement de temps
                data.append([[path[i].long, path[i].lat, path[i].t, path[i].p], 0] )
                i += 1
                continue
            
        elif (delta_altitude > 0) :
            #Le ballon est monté en altitude, NORMALEMENT EN TEMPS CONSIDÉRÉ COMME INSTANTANÉ

            d_alt = 0
            while(d_alt < delta_altitude):
                data.append([[path[i].long, path[i].lat, path[i].t, path[i].p - d_alt], 1])
                d_alt += 1
            i += 1
            continue
        
        elif (delta_altitude < 0) :
            #Le ballon est descendu en altitude, NORMALEMENT EN TEMPS CONSIDÉRÉ COMME INSTANTANÉ
            delta_altitude = -delta_altitude

            d_alt = 0
            while(d_alt < delta_altitude):
                data.append([[path[i].long, path[i].lat, path[i].t, path[i].p + d_alt], 2])
                d_alt += 1
            i += 1
            continue
    return data

def create_database_random(n : int, liste_villes : list) :
    """
    Fonction qui crée une base de données de n éléments et qui les ajoute dans un csv file
    """
    data = []
    i = 0
    while (i < n) :
        # Generate a random path
        found, ville_dep, ville_arr, path = random_path(liste_villes)
        if found:
            i += 1
            # Create data from the path
            data.extend([["Chemin : " + str(ville_dep) +" to " +str(ville_arr) ]])
            data.extend(create_data(path))
            with open("database_random_paths_monde.csv", "a") as f:
                writer = csv.writer(f)
                writer.writerows(data)
            data = []


# Create the database of 10 000 elements
create_database_random(1000, villes_monde)




###########
## TESTS ##
###########

def test_date() :
    temps = generate_random_date(dt.datetime(2020, 1, 1), dt.datetime(2020, 10, 30))
    print(temps)


#test_date()

def test_path() :
    found, path = random_path(villes_france)
    if found :
        print("Chemin trouvé.")
        print(create_data(path))
    else :
        print("Chemin non trouvé.")

#test_path()



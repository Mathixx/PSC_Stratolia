#########################
## MODULES NECESSAIRES ##
#########################

import datetime as dt
import sys
import random

sys.path.append('./Algo Naif')
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

picke_file_path = "/users/eleves-b/2022/mathias.perez/Documents/DATA_VENT/objet_wind_data_2021.pickle"
with open(picke_file_path, "rb") as f:
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

def random_path_greedy(ville_destination, liste_villes) :
    """
    Fonction qui génère un chemin aléatoire entre 2 villes prise au hasard de la liste
    """
    path = []
    ville_depart = choisir_ville_au_hasard(liste_villes)

    distance_max = 5000000 # 5000 km

    while(ville_destination.nom == ville_depart.nom or distance_destination((ville_destination.long, ville_destination.lat), ville_depart.long, ville_depart.lat) > distance_max):
        ville_depart = choisir_ville_au_hasard(liste_villes)
    
    temps = (generate_random_date(dt.datetime(2021, 1, 1), dt.datetime(2021, 12, 24))-dt.datetime(2021, 1, 1)).total_seconds()
    #Convert it in an integer
    temps = int(temps)
    depart = Node(ville_depart.long, ville_depart.lat, temps, 16, None) #long, lat, temps, pression, None


    #print("Ville de départ : ", ville_depart.nom)
    #print("Ville de destination : ", ville_destination.nom)
    ville_arr = ville_destination
    ville_destination = (ville_destination.long, ville_destination.lat)
    

    duree = 120
    temps_chgmt_pression = 6*3600
    precision = 10000

    found, _ , path = greedy(ville_destination, depart, duree, temps_chgmt_pression, precision, wind_data)
    if found :
        return found, ville_depart, ville_arr ,path
    return found ,ville_depart, ville_arr, []



def random_path_hard(ville_destination, liste_villes) :
    
    duree = 120
    temps_chgmt_pression = 6*3600  # Remplacez par la durée du changement de pression souhaitée
    precision = 10000

    ville_depart = choisir_ville_au_hasard(liste_villes)

    while(ville_destination.nom == ville_depart.nom):
        ville_depart = choisir_ville_au_hasard(liste_villes)
    
    temps = (generate_random_date(dt.datetime(2021, 1, 1), dt.datetime(2021, 12, 24))-dt.datetime(2021, 1, 1)).total_seconds()
    tempsB = temps
    #Convert it in an integer
    temps = int(temps)
    depart = Node(ville_depart.long, ville_depart.lat, temps, 16, None) #long, lat, temps, pression, None


    ville_arr = ville_destination
    ville_destination = (ville_destination.long, ville_destination.lat)

    found, _ , _ = greedy(ville_destination, depart, duree, temps_chgmt_pression, precision, wind_data)

    if not found:
        #print("Greedy failed")
        found, _ , path = N_closest(ville_destination, depart, duree, temps_chgmt_pression, precision, 1, wind_data)
        if not found:
            #print("Select failed")
            #Take a random value in 0 and 1
            p = random.random()
            if p < 0.3:
                #print("Wide search not done")
                return False, ville_depart, ville_arr, []
            found, _ , path = wide_search(ville_destination, depart, duree, temps_chgmt_pression, precision, wind_data)
        return found, ville_depart , ville_arr , path
    else:
        return False, ville_depart, ville_arr, []


def create_data(path : list, ville_arr) :
    """
    Fonction qui crée un élément de la base de données à partir d'un chemin
    """
    data = []
    #print("create data")

    i = 0
    while (i < len(path)):
        if (i+1 < len(path) and path[i].t == path[i+1].t and path[i].p == path[i+1].p):
            i += 1
            continue
        data.append([ville_arr.long, ville_arr.lat, path[i].long, path[i].lat, path[i].t, path[i].p])
        i += 1
    #print("data created")
    return data


def create_database_easy(n : int, liste_villes, ville_arr) :
    """
    Fonction qui crée une base de données de n éléments et qui les ajoute dans un csv file
    """
    data = []
    i = 0
    #ville_arr = choisir_ville_au_hasard(capitales_europe)

    while (i < n) :
        # Generate a random path
        #print("Path number : ", i+1)
        found, ville_dep, ville_arr, path = random_path_greedy(ville_arr, liste_villes)
        if found:
            i += 1
            # Create data from the path
            #data.extend([["Chemin : " + str(ville_dep) +" to " + str(ville_arr) ]])
            data.extend(create_data(path, ville_arr))
            with open("database_"+str(ville_arr)+"_france21.csv", "a") as f:
                writer = csv.writer(f)
                writer.writerows(data)
            data = []
        else :
            continue

def create_database_hard(n : int, liste_villes, ville_arr) :
    """
    Fonction qui crée une base de données de n éléments et qui les ajoute dans un csv file
    """
    data = []
    #ville_arr = choisir_ville_au_hasard(capitales_europe)
    i = 0
    while (i < n) :
        # Generate a random path
        #print("Path number : ", i+1)
        found, ville_dep, ville_arr, path = random_path_hard(ville_arr, liste_villes)
        if found:
            i += 1
            # Create data from the path
            #data.extend([["Chemin : " + str(ville_dep) +" to " + str(ville_arr) ]])
            data.extend(create_data(path, ville_arr))
            with open("database_"+str(ville_arr)+"_france21.csv", "a") as f:
                writer = csv.writer(f)
                writer.writerows(data)
            data = []
        else :
            continue
            

def database() :
    ville_arr = choisir_ville_au_hasard(capitales_europe)

    create_database_easy(100, villes_europe, ville_arr)
    print("easy-1 done")
    create_database_hard(80, villes_europe, ville_arr)
    print("hard-1 done")

    create_database_easy(1000, villes_europe, ville_arr)
    print("easy-2 done")
    create_database_hard(100, villes_europe, ville_arr)
    print("hard-2 done")

    create_database_easy(1000, villes_europe, ville_arr)
    print("easy-3 done")
    create_database_hard(1000, villes_europe, ville_arr)
    print("hard-3 done")

    create_database_easy(100, villes_europe, ville_arr)
    print("easy-4 done")
    create_database_hard(100, villes_europe, ville_arr)
    print("hard-4 done")

    create_database_easy(1000, villes_europe, ville_arr)
    print("easy-4 done")
    create_database_hard(100, villes_europe, ville_arr)
    print("hard-4 done")


    print("let me sleep")


database()

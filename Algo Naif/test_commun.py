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

"""
data.extend([["Chemin : " + str(ville_dep) +" to " +str(ville_arr) ]])
            data.extend(create_data(path))
            with open("database_random_paths_monde.csv", "a") as f:
                writer = csv.writer(f)
                writer.writerows(data)
            data = []

"""

def generate_random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + dt.timedelta(days=random_number_of_days)
    hr  = random.randrange(0, 24, 6)
    random_time = dt.time(hour=hr, minute=0, second=0, microsecond=0, tzinfo=None, fold=0)
    return dt.datetime.combine(random_date, random_time)

def test1(technique, liste_villes):
    ville_depart = choisir_ville_au_hasard(liste_villes)
    ville_destination = choisir_ville_au_hasard(liste_villes)

    #distance_max = 5000000 # 5000 km

    while(ville_destination.nom == ville_depart.nom):
        ville_destination = choisir_ville_au_hasard(liste_villes)
    
    temps = (generate_random_date(dt.datetime(2020, 1, 1), dt.datetime(2020, 10, 30))-dt.datetime(2020, 1, 1)).total_seconds()
    #Convert it in an integer
    temps = int(temps)
    depart = Node(ville_depart.long, ville_depart.lat, temps, 16, None) #long, lat, temps, pression, None


    print("Ville de départ : ", ville_depart.nom)
    print("Ville de destination : ", ville_destination.nom)
    ville_arr = ville_destination
    ville_destination = (ville_destination.long, ville_destination.lat)

    # duree = int(input("Veuillez entrer la durée d'exploration (nombre d'heures divisible par 6) : "))
    duree = 60
    
    # Paramètres de test
    temps_chgmt_pression = 6*3600  # Remplacez par la durée du changement de pression souhaitée
    precision = 10000 # Précision de la destination

    # Exécution de la fonction
    temps_debut_execution = time.time()

    if technique == "greedy":
        duree = 120
        temps_chgmt_pression = 6*3600
        precision = 10000

        found, distance_min , path = greedy(ville_destination, depart, duree, temps_chgmt_pression, precision, wind_data)

    elif technique == "selection":
        duree = 120
        temps_chgmt_pression = 6*3600
        precision = 10000
        eloignement = 1.2

        found, distance_min , path = N_closest(ville_destination, depart, duree, temps_chgmt_pression, precision,eloignement, wind_data)

    elif technique == "exploration":
        duree = 120
        temps_chgmt_pression = 6*3600
        precision = 10000

        found, distance_min , path = wide_search(ville_destination, depart, duree, temps_chgmt_pression, precision, wind_data)

    temps_fin_execution = time.time()

    duree_execution = temps_fin_execution - temps_debut_execution
    print(f"Le code a pris {duree_execution} secondes pour s'exécuter.")
        
    # Renvoie si on a atteint la destination et le temps d'exécution.
    return (found, distance_min, duree_execution)

####################################
## CREATION DE LA BASE DE DONNÉES ##
####################################

def test_commun(liste_villes):
    Technique = ["greedy", "selection", "exploration"]
    """
    with open("test_commun_villes_france.txt", "a") as file:
        file.write("Test commun sur les villes de France.\n\n")
        file.write("Les paramètres des test sont : \n")
        file.write("Durée d'exploration : 120 heures.\n")
        file.write("Temps de changement de pression : 6 heures.\n")
        file.write("Précision : 10000 m.\n")
    """
    for tech in Technique:
        if tech == "greedy" or tech == "selection":
            continue
        with open("test_commun_villes_france.txt", "a") as file:
            file.write("Résulats de l'algorithme : " + tech +"\n")
        if tech == "selection":
            with open("test_commun_villes_france.txt", "a") as file:
                file.write("Pour ce test on a pris N : 100 " + tech +"\n")
        nombre_tests = 10000
        if tech == "exploration":
            nombre_tests = 100
        moyenne_temps = 0
        moyenne_chemins_trouves = 0
        moyenne_distance = 0
        for i in range(nombre_tests):
            print(str(i)+"-ième test...")
            (a_atteint_destination, distance, duree_execution) = test1(tech, liste_villes)
            if a_atteint_destination:
                moyenne_chemins_trouves += 1
            moyenne_temps += duree_execution
            moyenne_distance += distance/1000
        moyenne_chemins_trouves /= nombre_tests
        moyenne_temps = moyenne_temps / nombre_tests
        moyenne_distance = moyenne_distance / nombre_tests
        with open("test_commun_villes_france.txt", "a") as file:
            file.write("La fréquence de chemins trouvés est de : " + str(moyenne_chemins_trouves*100) +" %.\n")
            file.write("La distance moyenne à la destination est de : "+str(moyenne_distance) + " km.\n")
            file.write("La moyenne temporelle est de : " + str(moyenne_temps) +" secondes.\n")
            file.write("\n")

test_commun(villes_france)
   
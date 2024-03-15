#########################           ##################
## MODULES NÉCESSAIRES ##           ## VERSION TEST ##
#########################           ##################

import random
import time

from selection_search import *
from villes import *
#from Affichage import animation


###########
## TESTS ##       
###########




def test1_N_closest():
    depart = choisir_ville_au_hasard(villes_france)
    print("Départ : "+ str(depart))
    dest = choisir_ville_au_hasard(villes_france)
    # On ne veut pas que la destination soit égale au départ
    while(dest.nom == depart.nom):
        dest = choisir_ville_au_hasard(villes_france)
    print("Destination : "+str(dest))
    temps_I = random.randint(0, 100)
    print("Temps de départ : "+ str(temps_I))
    pression =  random.randint(0,16)
    print("Pression de départ : "+str(pression))
    # duree = int(input("Veuillez entrer la durée d'exploration (nombre d'heures divisible par 6) : "))
    duree = 72
    
    # Paramètres de test
    destination = (dest.long, dest.lat)
    n = Node(depart.long, depart.lat, temps_I*21600, pression=pression, prev=None)
    temps_chgmt_pression = 3600  # Remplacez par la durée du changement de pression souhaitée
    precision = 5000 # Précision de la destination
    eloignement = 1.2 # Ajuster si besoin 

    # Exécution de la fonction
    temps_debut_execution = time.time()
    a_atteint_destination, distance_min, res = N_closest(destination, n, duree, temps_chgmt_pression, precision, eloignement, wind_data)
    temps_fin_execution = time.time()
    duree_execution = temps_fin_execution - temps_debut_execution
    print(f"Le code a pris {duree_execution} secondes pour s'exécuter.")

    #coords = []
    #for i in range(len(res)):
    #    n = res[i]
    #    coords.append((n.long, n.lat, convPression_altitude(n.p), n.t[0], n.t[1]))
    #print(coords)
    #animation(coords, destination, 1)
    
    
    # Renvoie si on a atteint la destination et le temps d'exécution.
    return (a_atteint_destination, distance_min, duree_execution)


# Exécution du test
#test1_N_closest()


def test2_N_closest():
    # On fait varier la limite d'éloignement et la durée dans test1
    nombre_tests = 100
    moyenne_temps = 0
    moyenne_chemins_trouves = 0
    moyenne_distance = 0
    for i in range(nombre_tests):
        print(str(i)+"-ième test...")
        (a_atteint_destination, distance_min, duree_execution) = test1_N_closest()
        if a_atteint_destination:
            moyenne_chemins_trouves += 1
        moyenne_temps += duree_execution
        moyenne_distance += distance_min/1000
    moyenne_chemins_trouves /= nombre_tests
    moyenne_temps = moyenne_temps / nombre_tests
    moyenne_distance = moyenne_distance / nombre_tests
    print ("La fréquence de chemins trouvés est de : " + str(moyenne_chemins_trouves*100) +" %.")
    print("La distance moyenne à la destination est de : "+str(moyenne_distance) + " km.")
    print ("La moyenne temporelle est de : " + str(moyenne_temps) +" secondes.")


# Exécution du test
test2_N_closest()

# Résultats N=10 et 1000 tests : 28.8% de chemins trouvés / Moyenne temporelle 0.477s





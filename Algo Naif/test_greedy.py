#########################           ##################
## MODULES NÉCESSAIRES ##           ## VERSION TEST ##
#########################           ##################

import random
import time

from greedy import *
from villes import *
#from Affichage import animation


###########
## TESTS ##       
###########


def test1_greedy():
    depart = choisir_ville_au_hasard(villes_france)
    print("Départ : "+ str(depart))
    dest = choisir_ville_au_hasard(villes_france)
    # On ne veut pas que la destination soit égale au départ
    while(dest.nom == depart.nom):
        dest = choisir_ville_au_hasard(villes_france)
    print("Destination : "+str(dest))
    temps_I = random.randint(0, 1000)
    print("Temps de départ : "+ str(temps_I))
    pression =  random.randint(0,16)
    print("Pression de départ : "+str(pression))
    # duree = int(input("Veuillez entrer la durée d'exploration (nombre d'heures divisible par 6) : "))
    duree = 150
    
    # Paramètres de test
    destination = (dest.long, dest.lat)
    n = Node(depart.long, depart.lat, temps_I*21600, pression=pression, prev=None)
    temps_chgmt_pression = 3600  # Remplacez par la durée du changement de pression souhaitée
    precision = 10000 # Précision de la destination

    # Exécution de la fonction
    temps_debut_execution = time.time()
    a_atteint_destination, distance, res = greedy(destination, n, duree, temps_chgmt_pression, precision, wind_data)
    temps_fin_execution = time.time()
    duree_execution = temps_fin_execution - temps_debut_execution
    print(f"Le code a pris {duree_execution} secondes pour s'exécuter.")

    #coords = []
    #for i in range(len(res)):
        #n = res[i]
        #coords.append((n.long, n.lat, convPression_altitude(n.p), n.t[0], n.t[1]))
    #print(coords)
    #animation(coords, destination, 1)
    
    
    # Renvoie si on a atteint la destination et le temps d'exécution.
    return (a_atteint_destination, distance, duree_execution)


# Exécution du test
#test1_greedy()


def test2_greedy():
    # On fait varier la limite d'éloignement et la durée dans test1
    nombre_tests = 1000
    moyenne_temps = 0
    moyenne_chemins_trouves = 0
    moyenne_distance = 0
    for i in range(nombre_tests):
        print(str(i)+"-ième test...")
        (a_atteint_destination, distance, duree_execution) = test1_greedy()
        if a_atteint_destination:
            moyenne_chemins_trouves += 1
        moyenne_temps += duree_execution
        moyenne_distance += distance/1000
    moyenne_chemins_trouves /= nombre_tests
    moyenne_temps = moyenne_temps / nombre_tests
    moyenne_distance = moyenne_distance / nombre_tests
    print ("La fréquence de chemins trouvés est de : " + str(moyenne_chemins_trouves*100) +" %.")
    print("La distance moyenne à la destination est de : "+str(moyenne_distance) + " km.")
    print ("La moyenne temporelle est de : " + str(moyenne_temps) +" secondes.")


# Exécution du test
test2_greedy()





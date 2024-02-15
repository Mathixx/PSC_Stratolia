#########################           ##################
## MODULES NÉCESSAIRES ##           ## VERSION TEST ##
#########################           ##################

import random
import time

from makeTree import *
from villes import *


###########
## TESTS ##       
###########




def test1_makeTree():
    depart = choisir_ville_au_hasard(villes_monde)
    print("Départ : "+ str(depart))
    dest = choisir_ville_au_hasard(villes_monde)
    # On ne veut pas que la destination soit égale au départ
    while(dest.nom == depart.nom):
        dest = choisir_ville_au_hasard(villes_monde)
    print("Destination : "+str(dest))
    temps_I = random.randint(0, 100)
    print("Temps de départ : "+ str(temps_I))
    temps_sec = 0     # À modifier si besoin
    pression = random.randint(0,16)
    print("Pression de départ : "+str(pression))
    # duree = int(input("Veuillez entrer la durée d'exploration (nombre d'heures divisible par 6) : "))
    duree = 60
    
    # Paramètres de test
    destination = (dest.long, dest.lat)
    n = Node(depart.long, depart.lat, temps=(temps_I, temps_sec), pression=pression, prev=None)
    temps_chgmt_pression = 6*3600  # Remplacez par la durée du changement de pression souhaitée
    precision = 10000  # Précision de la destination
    limite_eloignement = 1.2*distance_destination(destination, depart.long, depart.lat) # Ajuster si besoin 

    # Exécution de la fonction
    temps_debut_execution = time.time()
    a_atteint_destination, res = Tree_Largeur(destination, n, duree, temps_chgmt_pression, precision, limite_eloignement, wind_data)
    temps_fin_execution = time.time()
    duree_execution = temps_fin_execution - temps_debut_execution
    print(f"Le code a pris {duree_execution} secondes pour s'exécuter.")
    
    # Renvoie si on a atteint la destination et le temps d'exécution.
    return (a_atteint_destination, duree_execution)


# Exécution du test
#test1_makeTree()


def test2_makeTree():
    # On fait varier la limite d'éloignement et la durée dans test1
    nombre_tests = 50
    moyenne_temps = 0
    moyenne_chemins_trouves = 0
    for i in range(nombre_tests):
        print(str(i)+"-ième test...")
        (a_atteint_destination, duree_execution) = test1_makeTree()
        if a_atteint_destination:
            moyenne_chemins_trouves += 1
        moyenne_temps += duree_execution
    moyenne_chemins_trouves /= nombre_tests
    moyenne_temps = moyenne_temps / nombre_tests
    print ("La fréquence de chemins trouvés est de : " + str(moyenne_chemins_trouves*100) +" %.")
    print ("La moyenne temporelle est de : " + str(moyenne_temps) +" secondes.")


# Exécution du test
test2_makeTree()





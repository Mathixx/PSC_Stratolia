#########################           ##################
## MODULES NÉCESSAIRES ##           ## VERSION TEST ##
#########################           ##################

import random
import time

from greedy import *
from villes import *
from Affichage import animation
#from Affichage import animation
import matplotlib.pyplot as plt



###########
## TESTS ##       
###########


def test1_greedy():
    #depart = choisir_ville_au_hasard(villes_europe)
    depart = Ville("Marrakech",  -7.58984375, 31.630334854125977)
    print("Départ : "+ str(depart))
    #dest = choisir_ville_au_hasard(villes_europe)
    dest = Ville("Paris", 2.2118199376859393, 48.710240264856644)
    # On ne veut pas que la destination soit égale au départ
    while(dest.nom == depart.nom):
        dest = choisir_ville_au_hasard(villes_europe)
    print("Destination : "+str(dest))
    temps_I = random.randint(0, 1000)
    print("Temps de départ : "+ str(temps_I))
    pression =  random.randint(0,16)
    print("Pression de départ : "+str(pression))
    # duree = int(input("Veuillez entrer la durée d'exploration (nombre d'heures divisible par 6) : "))
    duree = 120
    
    # Paramètres de test
    destination = (dest.long, dest.lat)
    n = Node(depart.long, depart.lat, temps_I*21600, pression=pression, prev=None)
    temps_chgmt_pression = 3600  # Remplacez par la durée du changement de pression souhaitée
    precision = 500 # Précision de la destination

    # Exécution de la fonction
    temps_debut_execution = time.time()
    a_atteint_destination, distance, res = greedy(destination, n, duree, temps_chgmt_pression, precision, wind_data)
    temps_fin_execution = time.time()
    duree_execution = temps_fin_execution - temps_debut_execution
    print(f"Le code a pris {duree_execution} secondes pour s'exécuter.")

    if a_atteint_destination:
        print("trouvé :")
        coords = chemin_graphic(res)
        nom = "Chemin_"+depart.nom+"_"+dest.nom+".gif"
        animation(coords, destination, 1, nom)
    
    # Renvoie si on a atteint la destination et le temps d'exécution.
    return (a_atteint_destination, distance, duree_execution)


# Exécution du test
#test1_greedy()

def trouver_chemin():
    test = False
    while not(test):
        test, _, _ = test1_greedy()

trouver_chemin()

def obtention_gif():
    count  = 0
    while count < 10:
        if test1_greedy()[0]:
            count += 1
            print(count)

#obtention_gif()
        

def test2_greedy():
    # On fait varier la limite d'éloignement et la durée dans test1
    nombre_tests = 10
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
#test2_greedy()


def graph_precision():
    # On veut obtenir un graphe de la performance de l'algorithme en fonction de la précision
    # On fait varier la précision de 1000 à 100000
    nombre_tests = 1000
    temps_execution = []
    frequence_succes = []
    liste_precision = [1000, 5000, 10000, 20000]
    for precision in liste_precision:
        print("Précision : "+str(precision))
        moyenne_temps = 0
        moyenne_chemins_trouves = 0
        for i in range(nombre_tests):
            print(str(i)+"-ième test...")
            (a_atteint_destination, distance, duree_execution) = test1_greedy()
            if a_atteint_destination:
                moyenne_chemins_trouves += 1
            moyenne_temps += duree_execution
        moyenne_chemins_trouves /= nombre_tests
        moyenne_temps = moyenne_temps / nombre_tests
        print ("La fréquence de chemins trouvés est de : " + str(moyenne_chemins_trouves*100) +" %.")
        print ("La moyenne temporelle est de : " + str(moyenne_temps) +" secondes.")
        temps_execution.append(moyenne_temps)
        frequence_succes.append(moyenne_chemins_trouves*100)
    # On utilise matplotlib pour tracer le graphe
    plt.plot(liste_precision, temps_execution, label="Temps d'exécution")
    plt.plot(liste_precision, frequence_succes, label="Fréquence de succès")
    plt.xlabel("Précision")
    plt.ylabel("Temps d'exécution/Fréquence de succès")
    plt.legend("Performance de l'algortihme greedy en fonction de la précision")
    plt.show()

#graph_precision()
    



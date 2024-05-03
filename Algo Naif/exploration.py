#########################
## MODULES NÉCESSAIRES ##
#########################


import math
import sys

from parcours import parcours_a_Z
from parcours_interpolate import parcours_a_Z_interpolate
from Node import *

from data_vent import *
from villes import *
from Affichage import animation
from Affichage import visupoints
import time

#########################
## FONCTION PRINCIPALE ##
#########################


"""
Programme qui détermine si on peut aller d'un point à un autre et qui renvoie le chemin dans le cas échéant

Entrée :
- position de la destination : longitude, latitude
- position intiale : noeud
Attention : on commence toujours sur un temps rond (au sens des données de vent ie multiple de six heures)
- durée de l'exploration (en heures)
Attention : on impose que la durée d'exploration soit un multiple de 6 heures !
- fréquence temporelle des changements de niveau de pression (en secondes)
Attention : on impose que le temps des changements de niveau de pression divise 6 heures !
- précisison (distance à la destination voulue en m)
- limite d'éloignement (distance à la destination à partir de laquelle on abandonne ce chemin). 

Sortie :
- un booléen qui indique si un chemin a été trouvé
- une liste de noeuds qui décrit le chemin trouvé (ou vide sinon)
"""


def wide_search(destination : (float,float), depart : Node, duree : int, temps_chgmt_pression : int, precision : int, tab_vent : dict) -> (bool, int, list) :

    # On vérifie que le noeud de départ n'a pas de parent.
    if not(depart.prev == None):
        raise ValueError("Le point de départ ne doit pas avoir de parent.")
        
    # On vérifie qu'on commence sur un temps 'rond'.
    if not(depart.t%21600 == 0):
        raise ValueError("On doit commencer sur un temps 'rond', ie multiple de six heures.")
    
    temps_initial = case_tps(depart.t)

    # On vérifie que la durée d'exploration est un multiple de six heures.
    if not(duree%6 == 0):
        raise ValueError("La durée d'exploration doit être un multiple de six heures.")
    
    # On vérifie que le temps des changements de niveau de pression divise six heures.
    if not(21600%temps_chgmt_pression == 0):
        raise ValueError("Le temps des changements de niveau de pression doit diviser six heures.")
    
    nombre_d_iterations = (duree//6)*(21600//temps_chgmt_pression)

    # On intialise l'écart minimal entre deux chemins explorés (en m)
    ecart_min = 100000

    # On initialise la liste des points que nous explorons.
    listeP = [depart]

    # On initialise le point le plus proche trouvé
    closest = depart
    distance_closest = distance_destination(destination, depart.long, depart.lat)
    limite_eloignement = int(distance_closest)

    for count in range(nombre_d_iterations) : 

        # On veut afficher dans quelle boucle la recherche est en cours.
        #print("Recherche dans la boucle "+str(count)+" ...")

        # Si la liste des points à explorer est nulle on abandonne.
        if len(listeP) == 0:
            print("Aucun chemin n'a été concluant.")
            return (False, limite_eloignement, [pointF])
        
        # On initialise la liste des points qu'on va atteindre.
        listeF = []

        for point in listeP :
            
            distance = distance_destination(destination, point.long, point.lat)

            # On continue l'exploration. On appelle parcours à Z pour tous les niveaux de pression
            # correspondant à notre point.
            for i in range(0, 17) :

                (a_rencontre_destination, pointF) = parcours_a_Z_interpolate(destination, Node(point.long, point.lat, point.t, i, point), temps_chgmt_pression, precision, tab_vent)

                # Si on a rencontré la destination, on remonte l'arbre pour reconstituer le chemin complet.
                if a_rencontre_destination:
                    liste = chemin(pointF)
                    #affichage_liste(liste)
                    return (True, precision, liste)
                # Sinon on ajoute le nouveau point à la liste des futurs points. 
                listeF.append(pointF)
        # On garde que les N éléments les plus proches.
        listeP = selection_opti(destination, listeF, ecart_min)
        #print("Nombre de points en cours d'exploration : "+str(len(listeP)))
        #visupoints(listeP,1)

        # On met à jour le point le plus proche atteint.
        dist = distance_destination(destination, listeP[0].long, listeP[0].lat)
        if (dist < distance_closest):
            closest = listeP[0]
            distance_closest = dist
        

    # Dans ce cas on a dépassé la limite temporelle d'exploration.
    print("On a atteint la limite temporelle d'exploration.")
    #distance_minimale = min(distance_destination(destination, point.long, point.lat) for point in listeP)
    #print("Distance de la destination = "+str(distance_minimale//1000)+ " km.")
    #print("Meilleur point final : "+str(listeP[0]))
    #print("Meilleure distance atteinte = "+str(distance_closest//1000)+ " km.")
    #print("Point le plus proche : "+str(closest)) 
    liste = chemin(listeP[0])
    return (False, distance_closest,liste)





###########################
## FONCTIONS AUXILIAIRES ##
###########################

'''
À écrire
'''


def selection_opti(destination : (float,float), liste : list, ecart_min : int) -> list:
    liste.sort(key = lambda x : distance_destination(destination, x.long, x.lat))
    res = []
    for x in liste:
        if len(res) == 1000:
            break
        # On ajoute x dans la liste seulement si la distance entre x et tous les éléments de res est suffisament grande.
        if all(distance_destination((y.long,y.lat), x.long, x.lat) > distance_destination(destination, y.long, y.lat)/30 for y in res):
            res.append(x)
    return res

    

###########
## TESTS ##
###########


def test_wide():
    # Demander à l'utilisateur d'entrer les données d'entrée
    #longInit = float(input("Veuillez entrer la longitude du point de départ : "))
    #latInit = float(input("Veuillez entrer la latitude du point de départ : "))
    #destination_long = float(input("Veuillez entrer la longitude de la destination : "))
    #destination_lat = float(input("Veuillez entrer la latitude de la destination : "))
    #temps_I = int(input("Veuillez entrer le temps de départ du parcours : "))
    dep = Ville("Toulouse", 1.4442, 43.6047)
    dest = Ville("rennes", 358.3222, 48.1173)
    depart = Node(dep.long, dep.lat, 21600*561, 14, None)
    destination = (dest.long, dest.lat)
    duree = 120
    temps_chgmt_pression = 3600
    precision = 10000
    (boool,dist,liste) = wide_search(destination, depart, duree, temps_chgmt_pression, precision, wind_data)
    animation(chemin_graphic(liste),destination,1)


#test_wide()


def test1_wide():
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
    duree = 120
    
    # Paramètres de test
    destination = (dest.long, dest.lat)
    n = Node(depart.long, depart.lat, temps_I*21600, pression=pression, prev=None)
    temps_chgmt_pression = 3600  # Remplacez par la durée du changement de pression souhaitée
    precision = 10000 # Précision de la destination

    # Exécution de la fonction
    temps_debut_execution = time.time()
    a_atteint_destination, distance, res = wide_search(destination, n, duree, temps_chgmt_pression, precision, wind_data)
    temps_fin_execution = time.time()
    duree_execution = temps_fin_execution - temps_debut_execution
    print(f"Le code a pris {duree_execution} secondes pour s'exécuter.")
    # Renvoie si on a atteint la destination et le temps d'exécution.
    return (a_atteint_destination, distance, duree_execution)




def test2_wide():
    nombre_tests = 10
    moyenne_temps = 0
    moyenne_chemins_trouves = 0
    moyenne_distance = 0
    for i in range(nombre_tests):
        print(str(i)+"-ième test...")
        (a_atteint_destination, distance, duree_execution) = test1_wide()
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


#test2_wide()

def graph_precision():
    # On veut obtenir un graphe de la performance de l'algorithme en fonction de la précision
    # On fait varier la précision de 1000 à 100000
    nombre_tests = 1000
    temps_execution = []
    frequence_succes = []
    liste_precision = [1000, 2000, 3000, 4000, 5000, 7500, 10000, 15000, 20000, 30000, 40000, 50000, 75000, 100000]
    for precision in liste_precision:
        print("Précision : "+str(precision))
        moyenne_temps = 0
        moyenne_chemins_trouves = 0
        for i in range(nombre_tests):
            print(str(i)+"-ième test...")
            (a_atteint_destination, distance, duree_execution) = test1_wide()
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


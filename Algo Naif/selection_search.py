#########################
## MODULES NÉCESSAIRES ##
#########################


import math
import sys

from parcours import parcours_a_Z
from parcours_interpolate import parcours_a_Z_interpolate
from Node import *
from parcours import distance_destination

from data_vent import *



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


def N_closest(destination : (float,float), depart : Node, duree : int, temps_chgmt_pression : int, precision : int, eloignement : float, tab_vent : dict) -> (bool, int, list) :

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

    # On vérifie que la limite d'éloignement choisie est suffisamment grande pour que l'algorithme fonctionne correctement.
    if eloignement<1:
        raise ValueError("La limite d'éloignement est inférieure à la distance entre le point de départ et la destination.")

    limite_eloignement = distance_destination(destination, depart.long, depart.lat)*eloignement

    # On réduit la limite d'éloignement au fur et à mesure pour qu'elle vaille un quart de la distance à la fin.
    constante_de_retrecissement = (1/(10*eloignement))**(1/nombre_d_iterations)

    # Valeur de N (modifiable si besoin)
    N = 100

    # On initialise la liste des points que nous explorons.
    listeP = [depart]
  

    for count in range(nombre_d_iterations) : 

        # On veut afficher dans quelle boucle la recherche est en cours.
        print("Recherche dans la boucle "+str(count)+" ...")

        # Si la liste des points à explorer est nulle on abandonne.
        if len(listeP) == 0:
            print("Aucun chemin n'a été concluant.")
            return (False, limite_eloignement, [pointF])
        
        # On initialise la liste des points qu'on va atteindre.
        listeF = []

        for point in listeP :
            
            distance = distance_destination(destination, point.long, point.lat)

            # Premier cas : si on est trop loin de la destination on abandonne l'exploration à partir de ce point.
            if distance > limite_eloignement :
               continue

            # Deuxième cas : on continue l'exploration. On appelle parcours à Z pour tous les niveaux de pression
            # correspondant à notre point.
            for i in range(0, 17) :

                (a_rencontre_destination, pointF) = parcours_a_Z(destination, Node(point.long, point.lat, point.t, i, point), temps_chgmt_pression, precision, tab_vent)

                # Si on a rencontré la destination, on remonte l'arbre pour reconstituer le chemin complet.
                if a_rencontre_destination:
                    liste = chemin(pointF)
                    affichage_liste(liste)
                    return (True, precision, liste)
                # Sinon on ajoute le nouveau point à la liste des futurs points. 
                listeF.append(pointF)
        # On garde que les N éléments les plus proches.
        listeP = N_plus_proches(destination, listeF, N)
        
        
        limite_eloignement *= constante_de_retrecissement

    # Dans ce cas on a dépassé la limite temporelle d'exploration.
    print("On a atteint la limite temporelle d'exploration.")
    distance_minimale = distance_min(listeP, destination, limite_eloignement)
    return (False, distance_minimale,[listeP[0]])





###########################
## FONCTIONS AUXILIAIRES ##
###########################

'''
Fonction qui reconstitue le chemin parcouru
Entrée : noeud d'arrivée
Sortie : la liste des points parcourus depuis le départ jusqu'à l'arrivée
'''

def chemin(point_atteint : Node) -> list:
    liste = [point_atteint]
    p = point_atteint
    while p.prev != None :
        p = p.prev
        liste.append(p)
    liste.reverse()
    return liste

'''
Fonction qui reconstitue le chemin parcouru en un format de donnée utilisable par l'algorithme de Mohammed
Entrée : liste des poids (format Node) parcourus depuis le départ jusqu'a l'arrivée
Sortie : la liste de coordonnées en format [(long_i,lat_i,z_i,sec_i),]i
'''

def chemin_graphic(chemin_node : list) -> list:
    liste = []
    for i in range(len(chemin_node)):
        n = chemin_node[i]
        liste.append([n.long, n.lat, altitude_from_indice(n.p), n.t])
    return liste



'''
Fonction qui affiche proprement la trajectoire trouvée

Entrée : liste de Node
Pas de sortie
'''

def affichage_liste(liste : list):
    print()
    print("Liste des points formant la trajectoire : ")
    print()
    for x in liste:
        if isinstance(x, Node):
            print(x)
        else:
            print("Erreur : un des éléments de la liste n'est pas une instance de la classe Node.")
            return


'''
Fonction qui convertit la donnée de case de pression en une altitude (en m??)

Entrée : case de pression (int dans [0,17[)
Sortie : altitude (int)
'''

def convPression_altitude(pressionData : int) -> int :
    # Formules admises fournies par Louis Hart-Davis
    tabPhP = [10,20,30,50,70,100,150,200,250,300,400,500,600,700,850,925,1000]
    pressionHp = tabPhP[pressionData]
    return 0.3048*145366.45*(1-(pressionHp/1013.25)**0.190284)



'''
Fonction qui renvoie la liste des N points les plus proches de la destination parmi une liste de points.
Entrée : 
- destination
- liste de noeuds
- nombre de points à conserver
Sortie :
- liste des N noeuds les plus proches de la destination
'''


def N_plus_proches(destination : (float, float), liste : list, N : int) -> list:
    if N < 0:
        raise ValueError("N doit être positif.")
    l = len(liste)
    if l<=N:
        return liste
    low, high = 0, l - 1
    while low <= high:
        pivot_idx = partition(destination, liste, low, high)
        if pivot_idx == N:
            return liste[:N]
        elif pivot_idx < N:
            low = pivot_idx + 1
        else:
            high = pivot_idx - 1
    return None
    



'''
Fonction auxilaire nécessaire pour la fonction N_plus_proches
'''


def partition(destination : (float, float), liste : list, low : int, high : int) -> int:
    pivot = liste[high]
    distance_pivot = distance_destination(destination, pivot.long, pivot.lat)
    i = low - 1
    for j in range(low, high):
        if distance_destination(destination, liste[j].long, liste[j].lat) <= distance_pivot:
            i += 1
            liste[i], liste[j] = liste[j], liste[i]
    liste[i + 1], liste[high] = liste[high], liste[i + 1]
    return i + 1


    
'''
Fonction qui renvoie la distance du point le plus proche de la destination dans une liste de points.
Entrée : liste de points et la limite d'éloignement
Sortie : distance du point le plus proche / limite d'éloignement si la liste est vide
'''


def distance_min(liste : list, destination : (float,float), limite_eloignement : int) -> int:
    dmin = limite_eloignement
    for x in liste:
        d = distance_destination(destination, x.long, x.lat)
        dmin = min(d,dmin)
    return dmin



###########
## TESTS ##
###########


### OBJECTIF : Hippo doit rentrer chez lui ! MAIS il a mal au pied et n'a qu'un ballon stratosphérique à disposition
# Trouvons quand partir
"""
son adresse :
48.865013122558594 ; 2.2885401248931885

73 bvrd des marechaux :
48.71699905395508 ; 2.2039577960968018

"""


def test(): 
    t = 0
    while True :
        res = Tree_Largeur((2.1675682067871094,48.710262298583984),Node(2.2039577960968018,48.71699905395508,(t,0),0,None),24,3*3600,100,40000,wind_data)
        if res[0] == True :
            print("un chemin a été trouvé :")
            affichage_liste(res[1])
            break
        t +=1

#test()


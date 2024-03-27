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
from villes import *
from Affichage import animation
from Affichage import visupoints

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

            # On continue l'exploration. On appelle parcours à Z pour tous les niveaux de pression
            # correspondant à notre point.
            for i in range(0, 17) :

                (a_rencontre_destination, pointF) = parcours_a_Z_interpolate(destination, Node(point.long, point.lat, point.t, i, point), temps_chgmt_pression, precision, tab_vent)

                # Si on a rencontré la destination, on remonte l'arbre pour reconstituer le chemin complet.
                if a_rencontre_destination:
                    liste = chemin_animation(pointF)
                    affichage_liste(liste)
                    return (True, precision, liste)
                # Sinon on ajoute le nouveau point à la liste des futurs points. 
                listeF.append(pointF)
        # On garde que les N éléments les plus proches.
        listeP = selection_opti(destination, listeF, ecart_min)
        print("Nombre de points en cours d'exploration : "+str(len(listeP)))
        visupoints(listeP,1)

        # On met à jour le point le plus proche atteint.
        dist = distance_destination(destination, listeP[0].long, listeP[0].lat)
        if (dist < distance_closest):
            closest = listeP[0]
            distance_closest = dist
        

    # Dans ce cas on a dépassé la limite temporelle d'exploration.
    print("On a atteint la limite temporelle d'exploration.")
    distance_minimale = min(distance_destination(destination, point.long, point.lat) for point in listeP)
    print("Distance de la destination = "+str(distance_minimale//1000)+ " km.")
    print("Meilleur point final : "+str(listeP[0]))
    print("Meilleure distance atteinte = "+str(distance_closest//1000)+ " km.")
    print("Point le plus proche : "+str(closest)) 
    liste = chemin_animation(listeP[0])
    return (False, distance_minimale,liste)





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
Fonction qui reconstitue le chemin parcouru
Entrée : noeud d'arrivée
Sortie : la liste des points parcourus dans le format de la fonction animation [(long,lat,alt,sec)]
'''


def chemin_animation(point_atteint : Node) -> list:
    coords = []
    p = point_atteint
    while p.prev != None:
        coords.append((p.long,p.lat,convPression_altitude(p.p),p.t))
        p = p.prev
    coords.reverse()
    return coords


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
    dep = Ville("Paris", 2.3522, 48.8566)
    dest = Ville("Marseille", 5.3698, 43.2965)
    depart = Node(dep.long, dep.lat, 0, 0, None)
    destination = (dest.long, dest.lat)
    duree = 120
    temps_chgmt_pression = 6*3600
    precision = 10000
    (boool,dist,liste) = wide_search(destination, depart, duree, temps_chgmt_pression, precision, wind_data)
    animation(liste,destination,1)

test_wide()
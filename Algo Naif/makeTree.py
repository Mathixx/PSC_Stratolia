import math
import sys
from parcours import parcours_a_Z
import pickle
with open("objet_wind_data_2020.pickle", "rb") as f:
    wind_data = pickle.load(f)


class Node :
    def __init__(self, longitude, latitude, pression, temps, prev):
        self.long = longitude
        self.lat = latitude
        self.p = pression
        self.t = temps
        self.prev = prev
    
"""
A vrai dire, on a pas reelement besoin de construire de graphe.
Si on sait quelle destination on souhaite atteindre, on parcours le graphe de la maniere evoquée ci-après et on retourne un booleen qui nous dit si on peut atteindre ou non la solution en un temps Tmax fixé

Construire le graphe permet de garder en memoire le chemion a prendre (en remontant les pères)
"""


def Tree_Largeur(destination,longitude : (int, int), latitude : (int, int), pression : int, temps : int, duree : int) -> (bool, list(Node)) :
    #On fixe ici la precision de notre algo : a quel distance de l'objectif considere-t-on etre arrive ? (en m)
    precision = 1000

    racine = Node(longitude, latitude, pression, temps, None)

    listeP = [racine]

    while True :
        for n in listeP :
            if testPosition(destination, n.long, n.lat, precision) :
            #retourner la liste avec le parcours en arriere du graphe
                liste = [n]
                nb = n
                while nb.prev != None :
                    nb = nb.prev
                    liste.append(nb)
                return True, liste
            
            if n.t > temps + 100 :
                return False, []

            #Ici considère l'evolution en  altitude sur les 20 000 km, parcours total en 35 minutes -> negligeable
            for i in range(0, 17) :
                if i!= pression :
                    listeP.append(Node(longitude, latitude, i, temps, n))
            
            #Ensuite, pour chaque noeud de la colonne, on considère son évolution temporelle a altitude fixée
            listeF = []
            for noeudP in listeP :
                longB, latB = parcours_a_Z(longitude, latitude, noeudP.p, wind_data, temps, duree)
                listeF.append(Node(longB,latB,noeudP.p, temps+duree, noeudP))
        listeP = listeF





def testPosition(destination : ((int,int),(int,int)), longitude : (int,int), latitude : (int,int), precision : int) -> bool :
    if destination[0][0] == longitude[0] and destination[1][0] == latitude[0] :
        if (math.sqrt((destination[0][1]-longitude[1])**2 + (destination[1][1]-latitude[1])**2) < precision) :
            return True
    return False
#On peut egalement ajouter dans cette fonction des éléments qui arretent l'exploration si on va trop loin ou ce genre de choses


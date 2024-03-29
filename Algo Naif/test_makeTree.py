#########################           ##################
## MODULES NÉCESSAIRES ##           ## VERSION TEST ##
#########################           ##################

import random
import time

from makeTree import *


###########
## TESTS ##       
###########


class Ville:
    def __init__(self, nom, longitude, latitude):
        self.nom = nom
        self.long = longitude
        self.lat = latitude

    def __str__(self):
        return self.nom + " (Longitude : "+str(self.long)+" | Latitude : "+str(self.lat)+")"


# Liste de villes françaises.

villes_france = [
    Ville("Paris", 2.3522, 48.8566),
    Ville("Marseille", 5.3698, 43.2965),
    Ville("Lyon", 4.8357, 45.7640),
    Ville("Toulouse", 1.4442, 43.6047),
    Ville("Nice", 7.2620, 43.7102),
    Ville("Nantes", 358.4464, 47.2184),  
    Ville("Montpellier", 3.8767, 43.6110),
    Ville("Strasbourg", 7.7521, 48.5734),
    Ville("Bordeaux", 359.4208, 44.8378),  
    Ville("Lille", 3.0573, 50.6292),
    Ville("Rennes", 358.3222, 48.1173), 
    Ville("Reims", 4.0317, 49.2583),
    Ville("Le Havre", 0.1070, 49.4944),
    Ville("Saint-Étienne", 4.3872, 45.4397),
    Ville("Toulon", 5.9280, 43.1242),
    Ville("Grenoble", 5.7245, 45.1885),
    Ville("Dijon", 5.0415, 47.3220),
    Ville("Angers", 359.4368, 47.4784),  
    Ville("Nîmes", 4.3601, 43.8367),
    Ville("Aix-en-Provence", 5.4474, 43.5297)
]


def choisir_ville_au_hasard(liste_villes):
    return random.choice(liste_villes)


def test1_makeTree():
    depart = choisir_ville_au_hasard(villes_france)
    print("Départ : "+ str(depart))
    dest = choisir_ville_au_hasard(villes_france)
    # On ne veut pas que la destination soit égale au départ
    while(dest.nom == depart.nom):
        dest = choisir_ville_au_hasard(villes_france)
    print("Destination : "+str(dest))
    temps_I = random.randint(0, 100)
    print("Temps de départ : "+ str(temps_I))
    temps_sec = 0     # À modifier si besoin
    pression = random.randint(0,16)
    print("Pression de départ : "+str(pression))
    duree = int(input("Veuillez entrer la durée d'exploration (nombre d'heures divisible par 6) : "))
    
    # Paramètres de test
    destination = (dest.long, dest.lat)
    n = Node(depart.long, depart.lat, temps=(temps_I, temps_sec), pression=pression, prev=None)
    temps_chgmt_pression = 3*3600  # Remplacez par la durée du changement de pression souhaitée
    precision = 10000  # Précision de la destination
    limite_eloignement = distance_destination(destination, depart.long, depart.lat) # Ajuster si besoin 

    # Exécution de la fonction
    temps_debut_execution = time.time()
    a_atteint_destination, res = Tree_Largeur(destination, n, duree, temps_chgmt_pression, precision, limite_eloignement, wind_data)
    temps_fin_execution = time.time()
    duree_execution = temps_fin_execution - temps_debut_execution
    print(f"Le code a pris {duree_execution} secondes pour s'exécuter.")
    
    # Renvoie si on a atteint la destination et le temps d'exécution.
    return (a_atteint_destination, duree_execution)


# Exécution du test
test1_makeTree()


def test2_makeTree():
    # On fait varier la limite d'éloignement et la durée dans test1
    nombre_tests = 100
    moyenne_temps = 0
    moyenne_chemins_trouves = 0
    for i in range(nombre_tests):
        (a_atteint_destination, duree_execution) = test1_makeTree()
        if a_atteint_destination:
            moyenne_chemins_trouves += 1
        moyenne_temps += 1
    moyenne_chemins_trouves /= nombre_tests
    moyenne_temps /= nombre_tests
    print ("La fréquence de chemins trouvés est de : " + str(moyenne_chemins_trouves) +" %.")
    print ("La moyenne temporelle est de : " + str(moyenne_temps) +" secondes.")


# Exécution du test
#test2_makeTree()

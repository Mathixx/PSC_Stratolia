import random

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


villes_200 = random.choices(villes_france, k=200)
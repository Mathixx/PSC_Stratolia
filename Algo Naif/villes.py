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

# Liste de villes dans le monde.

villes_monde = [
    Ville("Tokyo", 139.6917, 35.6895),
    Ville("New Delhi", 77.1025, 28.7041),
    Ville("Beijing", 116.4074, 39.9042),
    Ville("Brasília", -47.9297, -15.7801),
    Ville("Moscow", 37.6173, 55.7558),
    Ville("Washington, D.C.", -77.0369, 38.8951),
    Ville("London", -0.1278, 51.5074),
    Ville("Paris", 2.3522, 48.8566),
    Ville("Berlin", 13.4050, 52.5200),
    Ville("Canberra", 149.1300, -35.2809),
    Ville("Rome", 12.4964, 41.9028),
    Ville("Ottawa", -75.6972, 45.4215),
    Ville("Madrid", -3.7038, 40.4168),
    Ville("Seoul", 126.9780, 37.5665),
    Ville("Buenos Aires", -58.3816, -34.6037),
    Ville("Cairo", 31.2357, 30.0444),
    Ville("Brussels", 4.3517, 50.8503),
    Ville("Mexico City", -99.1332, 19.4326),
    Ville("Tokyo", 139.6917, 35.6895),
    Ville("Buenos Aires", -58.3816, -34.6037),
    Ville("Bangkok", 100.5018, 13.7563),
    Ville("Canberra", 149.1300, -35.2809),
    Ville("London", -0.1278, 51.5074),
    Ville("Berlin", 13.4050, 52.5200),
    Ville("Beijing", 116.4074, 39.9042),
    Ville("Paris", 2.3522, 48.8566),
    Ville("Moscow", 37.6173, 55.7558),
    Ville("Washington, D.C.", -77.0369, 38.8951),
    Ville("Madrid", -3.7038, 40.4168),
    Ville("Ottawa", -75.6972, 45.4215),
    Ville("Rome", 12.4964, 41.9028),
    Ville("Seoul", 126.9780, 37.5665),
    Ville("Bangkok", 100.5018, 13.7563),
    Ville("Brussels", 4.3517, 50.8503),
    Ville("Brasília", -47.9297, -15.7801),
    Ville("Cairo", 31.2357, 30.0444),
    Ville("New Delhi", 77.1025, 28.7041),
    Ville("Mexico City", -99.1332, 19.4326),
    Ville("Tokyo", 139.6917, 35.6895),
    Ville("Beijing", 116.4074, 39.9042),
    Ville("Berlin", 13.4050, 52.5200),
    Ville("London", -0.1278, 51.5074),
    Ville("Paris", 2.3522, 48.8566),
    Ville("Moscow", 37.6173, 55.7558),
    Ville("Washington, D.C.", -77.0369, 38.8951),
    Ville("New Delhi", 77.1025, 28.7041),
    Ville("Bangkok", 100.5018, 13.7563),
    Ville("Brasília", -47.9297, -15.7801)
]



def choisir_ville_au_hasard(liste_villes):
    return random.choice(liste_villes)



import random
from data_vent import *
from math import radians, sin, cos, sqrt, atan2

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

# Liste de villes en Europe.

villes_europe = [
    Ville("Paris", 2.3522, 48.8566),
    Ville("Marseille", 5.3698, 43.2965),
    Ville("Lyon", 4.8357, 45.7640),
    Ville("Toulouse", 1.4442, 43.6047),
    Ville("Londres", -0.1278, 51.5074),
    Ville("Berlin", 13.4050, 52.5200),
    Ville("Madrid", -3.7038, 40.4168),
    Ville("Rome", 12.4964, 41.9028),
    Ville("Amsterdam", 4.897975, 52.374540),
    Ville("Bruxelles", 4.3517, 50.8503),
    Ville("Lisbonne", -9.1393, 38.7223),
    Ville("Vienne", 16.3738, 48.2082),
    Ville("Varsovie", 21.0122, 52.2297),
    Ville("Budapest", 19.0402, 47.4979),
    Ville("Prague", 14.4378, 50.0755),
    Ville("Athènes", 23.7275, 37.9838),
    Ville("Stockholm", 18.0686, 59.3293),
    Ville("Oslo", 10.7522, 59.9139),
    Ville("Copenhague", 12.5683, 55.6761),
    Ville("Helsinki", 24.9384, 60.1695),
    Ville("Dublin", -6.2603, 53.3498),
    Ville("Édimbourg", -3.1883, 55.9533),
    Ville("Reykjavik", -21.9426, 64.1466),
    Ville("Moscou", 37.6173, 55.7558),
    Ville("Kiev", 30.5238, 50.4501),
    Ville("Bucarest", 26.1025, 44.4268),
    Ville("Sofia", 23.3219, 42.6977),
    Ville("Ankara", 32.8597, 39.9334),
    Ville("Istanbul", 28.9784, 41.0082),
    Ville("Athènes", 23.7275, 37.9838),
    Ville("Bucarest", 26.1025, 44.4268),
    Ville("Leeds", -1.5491, 53.8008),
    Ville("Manchester", -2.2426, 53.4808),
    Ville("Liverpool", -2.9912, 53.4084),
    Ville("Barcelone", 2.1734, 41.3851),
    Ville("Valence", -0.3750, 39.4699),
    Ville("Florence", 11.2558, 43.7696),
    Ville("Milan", 9.1859, 45.4654)
]


    
    

# Liste de villes dans le monde.

villes_monde = [
    Ville("Kinshasa", 15.2663, -4.4419),
    Ville("Joahannesburg", 28.0473, -26.2041),
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
    #Rajout de villes 
    Ville("Lima", -77.0428, -12.0464),
    Ville("Santiago", -70.6483, -33.4372),
    Ville("Bogota", -74.0721, 4.7110),
    Ville("Quito", -78.4678, -0.1807),
    Ville("Caracas", -66.9036, 10.4806),
    Ville("La Paz", -68.1193, -16.5000),
    Ville("Sao Paulo", -46.6333, -23.5505),
    #Rajout de villes en Angleterre
    Ville("Manchester", -2.2426, 53.4808),
    Ville("Liverpool", -2.9912, 53.4084),
    Ville("Birmingham", -1.8936, 52.4862),
    Ville("Leeds", -1.5491, 53.8008),
    #Rajout de villes en Espagne
    Ville("Barcelona", 2.1734, 41.3851),
    Ville("Valencia", -0.3750, 39.4699),
    Ville("Seville", -5.9845, 37.3891),
    Ville("Zaragoza", -0.8773, 41.6488),
    Ville("Sidney", 151.2093, -33.8688)
]

capitales_europe = [ Ville("Paris", 2.3522, 48.8566), 
                    Ville("Berlin", 13.4050, 52.5200), 
                    Ville("Madrid", -3.7038, 40.4168), 
                    Ville("Rome", 12.4964, 41.9028), 
                    Ville("Amsterdam", 4.897975, 52.374540), 
                    Ville("Bruxelles", 4.3517, 50.8503), 
                    Ville("Lisbonne", -9.1393, 38.7223), 
                    Ville("Vienne", 16.3738, 48.2082), 
                    Ville("Varsovie", 21.0122, 52.2297), 
                    Ville("Budapest", 19.0402, 47.4979), 
                    Ville("Prague", 14.4378, 50.0755), 
                    Ville("Athènes", 23.7275, 37.9838), 
                    Ville("Stockholm", 18.0686, 59.3293), 
                    Ville("Oslo", 10.7522, 59.9139), 
                    Ville("Copenhague", 12.5683, 55.6761), 
                    Ville("Helsinki", 24.9384, 60.1695), 
                    Ville("Dublin", -6.2603, 53.3498), 
                    Ville("Édimbourg", -3.1883, 55.9533), 
                    Ville("Reykjavik", -21.9426, 64.1466), 
                    Ville("Londres", -0.1278, 51.5074), 
                    #Ville("Moscou", 37.6173, 55.7558), 
                    Ville("Kiev", 30.5238, 50.4501), 
                    Ville("Bucarest", 26.1025, 44.4268),
                      Ville("Sofia", 23.3219, 42.6977), 
                      Ville("Ankara", 32.8597, 39.9334), 
                      Ville("Istanbul", 28.9784, 41.0082), 
                      Ville("Leeds", -1.5491, 53.8008), 
                      Ville("Manchester", -2.2426, 53.4808), 
                      Ville("Liverpool", -2.9912, 53.4084), 
                      Ville("Barcelone", 2.1734, 41.3851), 
                      Ville("Valence", -0.3750, 39.4699), 
                      Ville("Florence", 11.2558, 43.7696), 
                      Ville("Milan", 9.1859, 45.4654) 
]


capitales_europe = [ Ville("Paris", 2.3522, 48.8566), 
                    Ville("Berlin", 13.4050, 52.5200), 
                    Ville("Madrid", -3.7038, 40.4168), 
                    Ville("Rome", 12.4964, 41.9028), 
                    Ville("Amsterdam", 4.897975, 52.374540), 
                    Ville("Bruxelles", 4.3517, 50.8503), 
                    Ville("Lisbonne", -9.1393, 38.7223), 
                    Ville("Vienne", 16.3738, 48.2082), 
                    Ville("Varsovie", 21.0122, 52.2297), 
                    Ville("Budapest", 19.0402, 47.4979), 
                    Ville("Prague", 14.4378, 50.0755), 
                    Ville("Athènes", 23.7275, 37.9838), 
                    Ville("Stockholm", 18.0686, 59.3293), 
                    Ville("Oslo", 10.7522, 59.9139), 
                    Ville("Copenhague", 12.5683, 55.6761), 
                    Ville("Helsinki", 24.9384, 60.1695), 
                    Ville("Dublin", -6.2603, 53.3498), 
                    Ville("Édimbourg", -3.1883, 55.9533), 
                    Ville("Reykjavik", -21.9426, 64.1466), 
                    Ville("Londres", -0.1278, 51.5074), 
                    #Ville("Moscou", 37.6173, 55.7558), 
                    Ville("Kiev", 30.5238, 50.4501), 
                    Ville("Bucarest", 26.1025, 44.4268),
                      Ville("Sofia", 23.3219, 42.6977), 
                      Ville("Ankara", 32.8597, 39.9334), 
                      Ville("Istanbul", 28.9784, 41.0082), 
                      Ville("Leeds", -1.5491, 53.8008), 
                      Ville("Manchester", -2.2426, 53.4808), 
                      Ville("Liverpool", -2.9912, 53.4084), 
                      Ville("Barcelone", 2.1734, 41.3851), 
                      Ville("Valence", -0.3750, 39.4699), 
                      Ville("Florence", 11.2558, 43.7696), 
                      Ville("Milan", 9.1859, 45.4654) 
]





def choisir_ville_au_hasard(liste_villes):
    return random.choice(liste_villes)


def distance_entre_villes(ville1, ville2):
    # Rayon moyen de la Terre en kilomètres
    rayon_terre = 6371.0

    # Conversion des coordonnées degrés en radians
    lon1 = radians(ville1.long)
    lat1 = radians(ville1.lat)
    lon2 = radians(ville2.long)
    lat2 = radians(ville2.lat)

    # Différence de longitude et de latitude
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Formule de la haversine
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Distance entre les deux villes
    distance = rayon_terre * c
    return distance


def est_loin_des_autres(ville, villes):
    for autre_ville in villes:
        if ville.nom != autre_ville.nom:
            distance = distance_entre_villes(ville, autre_ville)
            if distance < 5000:
                return False
    return True

#Je veux afficher, parmi les villes du monde, celle q

def test() :
    ville_loin = None

    for ville in villes_monde:
        if est_loin_des_autres(ville, villes_monde):
            ville_loin = ville
            break

    if ville_loin:
        print(f"{ville_loin.nom} est à plus de 5000 km de toutes les autres villes.")
    else:
        print("Aucune ville n'est à plus de 5000 km de toutes les autres villes.")

#test()

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def afficher_positions_villes(villes, filename, color, region):
    # Extract latitudes and longitudes
    lats = [ville.lat for ville in villes]
    lons = [ville.long for ville in villes]
    
    # Calculate the geographical bounds
    min_lat, max_lat = min(lats), max(lats)
    min_long, max_long = min(lons), max(lons)
    
    # Calculate the aspect ratio
    lat_range = max_lat - min_lat
    long_range = max_long - min_long
    aspect_ratio = long_range / lat_range

    # Set the figure size based on the aspect ratio and region
    if region == 'France':
        fig_width = 12
        fig_height = 10
        marker_size = 20
    elif region == 'Europe':
        fig_width = 10
        fig_height = fig_width / aspect_ratio
        marker_size = 7
    elif region == 'World':
        fig_width = 15
        fig_height = 7.5
        marker_size = 8

    fig = plt.figure(figsize=(fig_width, fig_height), dpi=300)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    for ville in villes:
        ax.plot(ville.long, ville.lat, 'o', color=color, transform=ccrs.PlateCarree(), markersize=marker_size)

    ax.coastlines(resolution='110m')
    
    if region == 'France':
        ax.set_extent([-5, 9, 41, 51], crs=ccrs.PlateCarree())
    elif region == 'Europe':
        ax.set_extent([-30, 40, 30, 70], crs=ccrs.PlateCarree())
    elif region == 'World':
        ax.set_global()
    else:
        ax.set_extent([min_long, max_long, min_lat, max_lat], crs=ccrs.PlateCarree())
    
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.LAKES)
    ax.add_feature(cfeature.RIVERS)

    plt.savefig(filename, format='png', dpi=300)  # Save the figure with higher DPI
    # plt.show()


# afficher_positions_villes(villes_france, 'villes_france.png', 'red', 'France')
# afficher_positions_villes(villes_europe, 'villes_europe.png', 'blue', 'Europe')
afficher_positions_villes(villes_monde, 'villes_monde.png', 'purple', 'World')


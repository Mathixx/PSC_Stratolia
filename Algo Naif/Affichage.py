import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from celluloid import Camera
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib import animation
import matplotlib.gridspec as gridspec
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.dates as mdates
from datetime import datetime, timedelta


def animation(coords,heure_depart,step):
    X, Y, Z = zip(*coords)
    longitude_min, longitude_max = min(X)-1, max(X)+1 # Min et Max Longitudes
    latitude_min, latitude_max = min(Y)-1, max(Y)+1  # Min et Max Latitudes

  
    # Configuration de GridSpec
    fig = plt.figure(figsize=(15, 12))
    gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])

    # Axe 3D
    ax1 = ax = fig.add_subplot(gs[0], projection='3d')  
    ax1.set_xlim([min(X), max(X)])
    ax1.set_ylim([min(Y), max(Y)])
    ax1.set_zlim([min(Z), max(Z)])

    # Ajout des noms des axes pour le graphique 3D
    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Latitude')
    ax1.set_zlabel('Altitude')

    # Axe 2D
    ax2 = fig.add_subplot(gs[1],projection=ccrs.PlateCarree())
    ax2.set_global()



    camera = Camera(fig)
    heure_actuelle = heure_depart

    # Création de chaque frame de l'animation
    for i in range(len(coords)):
        

        x, y, z = coords[i]

        # Graphique 3D 
        ax1.plot(X[:i+1], Y[:i+1], Z[:i+1], color='b')
        ax1.scatter([x], [y], [z], color='blue', s=30)
        ax1.scatter([x], [y], 0, color='red', s=30)
        ax1.plot(X[:i+1], Y[:i+1], 0, color='r', linestyle='dashed', alpha=0.5)
        ax1.plot([x, x], [y, y], [0, z], color='grey', linestyle='-')

        # Graphique 2D 
        ax2.set_extent([longitude_min, longitude_max, latitude_min, latitude_max], crs=ccrs.PlateCarree())
        ax2.add_feature(cfeature.COASTLINE)
        ax2.add_feature(cfeature.COASTLINE)
        ax2.add_feature(cfeature.BORDERS, linestyle=':')
        ax2.add_feature(cfeature.LAND)
        ax2.add_feature(cfeature.OCEAN)
        ax2.add_feature(cfeature.LAKES)
        ax2.add_feature(cfeature.RIVERS)
        ax2.plot(X[:i+1], Y[:i+1], color='r',linestyle='dashed')
        ax2.scatter([x], [y], color='r', s=30)

        ax2.text(0.5, 1.05, heure_actuelle.strftime('%Y-%m-%d %H:%M:%S'), 
                ha='center', va='center', transform=ax2.transAxes, fontsize = 14)
        
        camera.snap()

        #Changement d'heure
        heure_actuelle += step
        

    # Génération et sauvegarde de l'animation
    animation = camera.animate()
    animation.save('Animation_trajectoire.gif', writer='Pillow', fps=2)

##Example 
spirale = [
    (50.0, 0.0, 0.0),
    (38.43, 29.22, 3.45),
    (12.45, 44.85, 6.90),
    (-16.59, 41.64, 10.34),
    (-36.93, 22.22, 13.79),
    (-41.14, -4.47, 17.24),
    (-28.79, -27.27, 20.69),
    (-6.14, -37.43, 24.14),
    (16.96, -31.99, 27.59),
    (31.30, -14.48, 31.03),
    (31.99, 7.04, 34.48),
    (20.09, 23.65, 37.93),
    (1.59, 29.27, 41.38),
    (-15.48, 22.83, 44.83),
    (-24.51, 8.26, 48.28),
    (-22.87, -7.71, 51.72),
    (-12.58, -18.55, 55.17),
    (1.12, -20.66, 58.62),
    (12.28, -14.45, 62.07),
    (16.84, -3.71, 65.52),
    (14.08, 6.52, 68.97),
    (6.46, 12.19, 72.41),
    (-1.95, 11.91, 75.86),
    (-7.51, 7.11, 79.31),
    (-8.57, 0.93, 82.76),
    (-5.91, -3.56, 86.21),
    (-1.91, -4.81, 89.66),
    (0.92, -3.32, 93.10),
    (1.37, -1.04, 96.55),
    (0.0, 0.0, 100.0)
]
# Heure de départ et intervalle de temps (step) en minutes
heure_depart = datetime(2024, 1, 1, 8, 0, 0)  # Exemple : 8h00 du matin
step = timedelta(minutes=30)  # Exemple : 30 minutes

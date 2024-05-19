#########################
## MODULES NÉCESSAIRES ##
#########################

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
import pickle

###########################
## FONCTIONS PRINCIPALES ##
###########################

def visupoints(liste,echelle=1):
    ''' Visualise '''
    X,Y = [],[]
    
    for n in liste :
        X.append(n.long)
        Y.append(n.lat)
    X = [(x-360 if x>180 else x ) for x in X]
    longitude_min, longitude_max = min(X)-echelle, max(X)+echelle # Min et Max Longitudes
    latitude_min, latitude_max = min(Y)-echelle, max(Y)+echelle  # Min et Max Latitudes
     # Création de la figure
    fig = plt.figure(figsize=(15, 12))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    # Ajout des points sur la carte
    
    ax.set_extent([longitude_min, longitude_max, latitude_min, latitude_max], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.LAKES)
    ax.add_feature(cfeature.RIVERS)
    ax.scatter(X, Y, transform=ccrs.PlateCarree(), color='red', marker='o', s=30)


    
    # Enregistrement de l'image
    nom = "points "+str(liste[0].t)+".png"
    plt.savefig(nom)

    

def animation(coords,dest,echelle=1):
    '''  crée une animation de la trajectoire du ballon, prenant en entrée une liste de coordonnées coords pour la trajectoire.
    Entrée : Coords  de la forme [(long_i,lat_i,z_i,sec_i),]
             un tuple dest pour la destination (long,lat),
             (Optionel) une echelle pour la carte (en long/lat)'''
      
    X, Y, Z, S = zip(*coords)
    X = [(x-360 if x>180 else x ) for x in X] #Conversion des longitudes dans ]-180;180]

    longitude_min, longitude_max = min(X)-echelle, max(X)+echelle # Min et Max Longitudes+= echelle
    latitude_min, latitude_max = min(Y)-echelle, max(Y)+echelle  # Min et Max Latitudes+= echelle

    # Configuration de GridSpec
    fig = plt.figure(figsize=(15, 12))
    gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])

    # Axe 3D
    ax1 = ax = fig.add_subplot(gs[0], projection='3d')  
    m = max(max(X)-min(X),max(Y)-min(Y))
    
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
    #ax2.set_xlim([(min(X)+max(X)-m)/2, (min(X)+max(X)+m)/2])
    #ax2.set_ylim([(min(Y)+max(X)-m)/2, (min(X)+max(X)+m)/2])

    camera = Camera(fig)
    
    # Création de chaque frame de l'animation
    for i in range(len(coords)):
        x, y, z = X[i],Y[i],Z[i]

        # Depart et arrivée
        ax1.scatter([X[0]], [Y[0]], [Z[0]], color='green', s=300, edgecolor='black', label='Départ',marker='^')
        ax2.scatter([X[0]], [Y[0]], color='green', s=100, edgecolor='black', transform=ccrs.PlateCarree(), label='Départ',marker='^')

        ax1.scatter([dest[0]],[dest[1]],[0] , color='green', s=300, label='Destination',marker='x')
        ax2.scatter([dest[0]], [dest[1]], color='green', s=100, transform=ccrs.PlateCarree(), label='Destination',marker='x')  
        
        if i == 0:
            ax1.legend(loc='upper left', fontsize = 16)

        
        

        # Graphique 3D 
        ax1.plot(X[:i+1], Y[:i+1], Z[:i+1], color='b')
        ax1.scatter([x], [y], [z], color='blue', s=30)
        ax1.scatter([x], [y], 0, color='red', s=30)
        ax1.plot(X[:i+1], Y[:i+1], 0, color='r', linestyle='dashed', alpha=0.5)
        ax1.plot([x, x], [y, y], [0, z], color='grey', linestyle='-')

        # Graphique 2D - Carte
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

        
        #Calcul et affiche de l'heure
        heure_actuelle = datetime(2020, 1, 1, 0, 0, 0)+timedelta(seconds = S[i])
        ax2.text(0.5, 1.05, heure_actuelle.strftime('%Y-%m-%d %H:%M:%S'), 
                ha='center', va='center', transform=ax2.transAxes, fontsize = 14)
        
        camera.snap()


    # Génération et sauvegarde de l'animation
    animation = camera.animate()
    animation.save('Animation_trajectoire.gif', writer='Pillow', fps=2)


def animation_simult(coords1, coords2, dest,echelle=1):
    # Tronquer la liste la plus longue
     min_length = min(len(coords1), len(coords2))
     coords1 = coords1[:min_length]
     coords2 = coords2[:min_length]
    
    # Extraire les données
     X1, Y1, Z1, S1 = zip(*coords1)
     X2, Y2, Z2, S2 = zip(*coords2)
    
    # Convertir les longitudes
     X1 = [(x-360 if x>180 else x ) for x in X1]
     X2 = [(x-360 if x>180 else x ) for x in X2]
    
    # Déterminer les limites pour les axes
     all_X = X1 + X2
     all_Y = Y1 + Y2
     longitude_min, longitude_max = min(all_X) - echelle, max(all_X) + echelle
     latitude_min, latitude_max = min(all_Y) - echelle, max(all_Y) + echelle
    
    # Configurer la figure et les axes
     fig = plt.figure(figsize=(15, 12))
     gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])
     ax1 = fig.add_subplot(gs[0], projection='3d')
     ax2 = fig.add_subplot(gs[1], projection=ccrs.PlateCarree())

     ax1.set_xlim([longitude_min, longitude_max])
     ax1.set_ylim([latitude_min, latitude_max])
     ax1.set_zlim([0, max(max(Z1), max(Z2))])

     ax1.set_xlabel('Longitude')
     ax1.set_ylabel('Latitude')
     ax1.set_zlabel('Altitude')

     camera = Camera(fig)

    # Création de chaque frame de l'animation
     for i in range(min_length):
         # Depart et arrivée
        ax1.scatter([X1[0]], [Y1[0]], [Z1[0]], color='green', s=300, edgecolor='black', label='Départ',marker='^')
        ax2.scatter([X1[0]], [Y1[0]], color='green', s=100, edgecolor='black', transform=ccrs.PlateCarree(), label='Départ',marker='^')

        ax1.scatter([dest[0]],[dest[1]],[0] , color='green', s=300, label='Destination',marker='x')
        ax2.scatter([dest[0]], [dest[1]], color='green', s=100, transform=ccrs.PlateCarree(), label='Destination',marker='x')  

        # Graphique 2D - Carte
        ax2.set_extent([longitude_min, longitude_max, latitude_min, latitude_max], crs=ccrs.PlateCarree())
        ax2.add_feature(cfeature.COASTLINE)
        ax2.add_feature(cfeature.COASTLINE)
        ax2.add_feature(cfeature.BORDERS, linestyle=':')
        ax2.add_feature(cfeature.LAND)
        ax2.add_feature(cfeature.OCEAN)
        ax2.add_feature(cfeature.LAKES)
        ax2.add_feature(cfeature.RIVERS)

        # Trajectoire pour coords1
        ax1.plot(X1[:i+1], Y1[:i+1], Z1[:i+1], color='purple')
        ax1.scatter([X1[i]], [Y1[i]], [Z1[i]], color='purple', s=30)
        ax1.plot(X1[:i+1], Y1[:i+1], 0, color='blue', linestyle='dashed', alpha=0.5)
        ax1.plot([X1[i], X1[i]], [Y1[i], Y1[i]], [0, Z1[i]], color='grey', linestyle='-')
        ax2.plot(X1[:i+1], Y1[:i+1], color='blue', linestyle='dashed', transform=ccrs.PlateCarree())
        ax2.scatter([X1[i]], [Y1[i]], color='blue', s=30, transform=ccrs.PlateCarree())
        
        # Trajectoire pour coords2
        ax1.plot(X2[:i+1], Y2[:i+1], Z2[:i+1], color='orange')
        ax1.scatter([X2[i]], [Y2[i]], [Z2[i]], color='orange', s=30)
        ax1.plot(X2[:i+1], Y2[:i+1], 0, color='red', linestyle='dashed', alpha=0.5)
        ax1.plot([X2[i], X2[i]], [Y2[i], Y2[i]], [0, Z2[i]], color='grey', linestyle='-')
        ax2.plot(X2[:i+1], Y2[:i+1], color='red', linestyle='dashed', transform=ccrs.PlateCarree())
        ax2.scatter([X2[i]], [Y2[i]], color='red', s=30, transform=ccrs.PlateCarree())
        
        # Affichage de l'heure
        heure_actuelle1 = datetime(2020, 1, 1, 0, 0, 0) + timedelta(seconds=S1[i])
        ax2.text(0.5, 1.05, f'{heure_actuelle1.strftime("%Y-%m-%d %H:%M:%S")}', 
                 ha='center', va='center', transform=ax2.transAxes, fontsize=14)
        
        camera.snap()

    # Génération et sauvegarde de l'animation
     animation = camera.animate()
     animation.save('Animation_trajectoire.gif', writer='Pillow', fps=2)





with open("objet_wind_data_2020.pickle", "rb") as f:
    wind_data = pickle.load(f)


def convPression_altitude(p):
    '''hPA -> km'''
    # Formule admise fournie par Louis Hart-Davis
    return 0.3048*145366.45*(1-(p/1013.25)**0.190284)/1000

#Données 
pres = wind_data['metadata']['grid']['pressure']
longs = wind_data['metadata']['grid']['longitude']
lats = wind_data['metadata']['grid']['latitude']
alts = convPression_altitude(pres)


def quadrillage(latmin,latmax,longmin,longmax):
    
    # longs, lats, alts
    long_indices = np.where((longmin <= longs) & (longs <= longmax))[0]
    lat_indices = np.where((latmin <= lats) & (lats <= latmax))[0]

    # Utilisation de tous les points pour Z car nous voulons utiliser tous les points d'altitude
    X, Y, Z = longs[long_indices], lats[lat_indices], alts


    # Axe 3D
    fig3d = plt.figure(figsize=(8, 6))
    ax3d = fig3d.add_subplot(111, projection='3d')

    # Configuration des axes pour 3D
    ax3d.set_xlim([longmin, longmax])
    ax3d.set_ylim([latmin, latmax])
    ax3d.set_zlim([0, np.max(alts)])
    ax3d.set_xlabel('Longitude')
    ax3d.set_ylabel('Latitude')
    ax3d.set_zlabel('Altitude')
    ax3d.view_init(elev=20, azim=30)

    plt.savefig('3d_map_without_red_grid.png')


    for alt in np.unique(Z):
        # Trace des lignes horizontales à cette altitude pour chaque latitude unique
        for y in Y:
            ax3d.plot([longmin, longmax], [y, y], [alt, alt], 'r--',alpha=1)  # Ligne horizontale à travers l'axe x

        # Trace des lignes verticales à cette altitude pour chaque longitude unique
        for x in X:
            ax3d.plot([x, x], [latmin, latmax], [alt, alt], 'r--',alpha=1)  # Ligne verticale à travers l'axe y



    plt.savefig('3d_map_with_red_grid.png')

    # Axe 2D
    fig2d = plt.figure(figsize=(8, 6))
    ax2d = fig2d.add_subplot(111, projection=ccrs.PlateCarree())
    ax2d.set_extent([longmin-0.5, longmax+0.5, latmin-0.5, latmax+0.5], crs=ccrs.PlateCarree())
    ax2d.add_feature(cfeature.COASTLINE)
    ax2d.add_feature(cfeature.BORDERS, linestyle=':')
    ax2d.add_feature(cfeature.LAND)
    ax2d.add_feature(cfeature.OCEAN)
    ax2d.add_feature(cfeature.LAKES)
    ax2d.add_feature(cfeature.RIVERS)

    plt.savefig('2d_map_without_red_grid.png')

    # Ajout du quadrillage rouge en pointillé pour 2D
    gl = ax2d.gridlines(draw_labels=True, linestyle='--', color='red', xlocs=np.arange(longmin, longmax + 2.5, 2.5), ylocs=np.arange(latmin, latmax + 2.5, 2.5), label='Grid')
    gl.xlabels_top = False
    gl.ylabels_right = False
    plt.savefig('2d_map_with_red_grid.png')

    plt.savefig('2d_map_with_red_grid.png')

# Créer une figure et un axe
fig, ax = plt.subplots(figsize=(5, 10))


def affiche_altitude():
    # Définir les limites de l'axe des y
    ax.set_ylim(0, 26)

    # Masquer l'axe des x
    ax.xaxis.set_visible(False)


    # Ajouter des titres et labels

    plt.ylabel('Altitude (km)')

    plt.savefig('alt_without_red_grid.png')

    # Tracer une ligne horizontale pour chaque altitude
    for alt in alts:
        ax.axhline(y=alt, linestyle='--', color='red', linewidth=2)  # Changer la couleur et l'épaisseur selon les besoins

    # Afficher le graphique
    plt.savefig('alt_with_red_grid.png')



##############
##  Example ## 
##############
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
spirale_modifiee = [
    (x, y, z,  600*i) for i, (x, y, z) in enumerate(spirale)
]

#animation(spirale_modifiee, [0.0, 0.0, 100.0],1)
#animation_simult(spirale_modifiee, spirale_modifiee[::-1] ,[0.0, 0.0, 100.0],1)
#affiche_altitude()
#quadrillage(27.5,70,-12.5,45)
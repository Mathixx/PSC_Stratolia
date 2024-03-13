import sys, math, pickle, numpy as np, random as rd, matplotlib.pyplot as plt, matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.gridspec as gridspec


#Importation des données NOAA
with open("objet_wind_data_2020.pickle", "rb") as f:
    wind_data = pickle.load(f)

def convPression_altitude(p): return 0.3048*145366.45*(1-(p/1013.25)**0.190284)/1000 
    #hPA -> km Formule admise fournie par Louis Hart-Davis 

#Données 
pres = wind_data['metadata']['grid']['pressure']
longs = wind_data['metadata']['grid']['longitude']
lats = wind_data['metadata']['grid']['latitude']
alts = convPression_altitude(pres)


def affiche_vents3D(temps,longmin, longmax, latmin,latmax):
     
     #On selectionne les indices qui nous interessent
     long_indices = np.where((longmin <= longs) & (longs <= longmax))[0]
     lat_indices = np.where((latmin <= lats) & (lats <= latmax))[0]

     #Composantes u et v du vent
     u = wind_data['data'][temps, :, :, :][:, np.ix_(lat_indices, long_indices)[0], np.ix_(lat_indices, long_indices)[1], 0]
     v = wind_data['data'][temps, :, :, :][:, np.ix_(lat_indices, long_indices)[0], np.ix_(lat_indices, long_indices)[1], 1]

     # Meshgrid pour les coordonnées filtrées et tous les niveaux de pression
     Z,Y,X = np.meshgrid( alts, lats[lat_indices],longs[long_indices], indexing='ij')
     
     fig = plt.figure()
     ax = fig.add_subplot(111, projection='3d')
    
     ax.quiver(X, Y, Z, u, v, 0, length=0.1, arrow_length_ratio=0.4, normalize=False, pivot = "middle" ) 
     ax.set_zlim(min(alts), max(alts)) #On doit inverser l'axe des altitudes car il n'est pas dans le mm sens que pression

     ax.set_xlabel('Longitude')
     ax.set_ylabel('Latitude')
     ax.set_zlabel('Altitude (km)')
     plt.show()


def affiche_vents2D(temps, longmin, longmax, latmin,latmax, pression, indice = False, ret=False):
    '''Affiche les vents à instant et pression fixés.
    Indice indique si l'argument pression est l'inidice dans wind_data ou une pression en hPa
    ret indique si on veut afficher le graphique ou return X,Y,u,v'''

    # Indice de la pression la plus proche 
    closest_pressure_idx = pression if indice else np.abs(pres - pression).argmin()

    # Indices de longitude et latitude
    long_indices = np.where((longmin <= longs) & (longs <= longmax))[0]
    lat_indices = np.where((latmin <= lats) & (lats <= latmax))[0]

    # Composantes u,v du vent
    u = wind_data['data'][temps, closest_pressure_idx, :, :][np.ix_(lat_indices, long_indices)[0], np.ix_(lat_indices, long_indices)[1], 0]
    v = wind_data['data'][temps, closest_pressure_idx, :, :][ np.ix_(lat_indices, long_indices)[0], np.ix_(lat_indices, long_indices)[1], 1]

    X, Y = np.meshgrid(longs[long_indices], lats[lat_indices])

    if ret: return (X,Y,u,v)
    else :
        #Affichage des vents 2D
        plt.figure(figsize=(10, 8))
        plt.quiver(X, Y, u, v, color = 'r', pivot = 'middle')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title(f'Vecteurs vents à {pres[closest_pressure_idx]} hPa / Altitude {format(alts[closest_pressure_idx],'.2f')} km')
        plt.show()



def affiche_ventsGIF(temps, longmin, longmax, latmin,latmax,show = True, save = False):

    #On définit l'animation, ici on joue sur la pression
    def animv(num,qr,temps, longmin, longmax, latmin,latmax):
        nummod = (16-num)%17 #On part de la pression la plus élévée au début
        u,v = affiche_vents2D(temps,longmin,longmax,latmin,latmax,nummod,True,True)[2:4]
        qr.set_UVC(u,v) 
        ax.set_title(f'Pression : {pres[nummod]} hPA / Altitude {format(alts[nummod],'.2f')} km')
        
    fig,ax = plt.subplots()
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title(f'Pression : {pres[16]} hPA/ Altitude {format(alts[16],'.2f')} km')
    X,Y,U,V = affiche_vents2D(temps, longmin,longmax,latmin,latmax,0,True,True)
    qr = ax.quiver(X,Y,U,V,color = 'r',pivot = 'middle')

    anim = animation.FuncAnimation(fig, animv, fargs=(qr,temps, longmin, longmax, latmin,latmax),
                              interval=1000, frames=range(17), blit=False)
    if show :
        plt.show()
    if save : 
        anim.save('ventsanim.gif', writer='pillow', fps=1)


#### Tests ####
#affiche_vents3D(0,20,30,-5,5)
#affiche_vents2D(0,10,40,-5,5,200)
#affiche_ventsGIF(0,10,40,-5,5,show = True, save = False)
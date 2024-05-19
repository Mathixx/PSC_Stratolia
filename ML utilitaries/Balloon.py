import datetime as dt
import sys

sys.path.append('/Users/mathiasperez/Documents/GitHub/PSC_Stratolia/Algo Naif')
from data_vent import *

import math


"""
Est ce que l'on garde le champ prev alors qu'on en aura potentiellement pas beosin car on explore une seul option a chaque fois
le render peut se demerder ? 

Quid du fait d'appler up quand t'es deja en limte ?

"""

with open("objet_wind_data_2020.pickle", "rb") as f:
    wind_data = pickle.load(f)


class Balloon:
    def __init__(self, longitude : float, latitude :  float, temps : dt.datetime, pression, prev, precision : int):
        self.long = longitude
        self.lat = latitude
        # Vérification que temps est un couple d'entiers
        if not isinstance(temps, dt.datetime) :
            raise ValueError("Le temps doit être sous format dt.datetime")
        self.t = temps
        # Vérification que pression est un entier
        if not isinstance(pression, int):
            raise ValueError("La pression doit être un entier.")
        self.p = pression
        self.precision = precision
        self.prev = prev

    def __str__(self):
        long_decimal_length = len(str('{:.6f}'.format(self.long).split('.')[1]))
        lat_decimal_length = len(str('{:.6f}'.format(self.lat).split('.')[1]))
        time_decimal_length = len(str(self.t.strftime('%Y%m%d%H%M%S')))

        # Largeur fixe pour le champ "Pression"
        pression_width = 3

        return "Longitude: {:{long_width}.{long_width}f} | Latitude: {:{lat_width}.{lat_width}f} | Pression: {:{pression_width}d} | Date: {:>{time_width}}".format(
            self.long, self.lat, self.p, self.t.strftime('%Y-%m-%d-%H-%M-%S'),
            long_width=long_decimal_length + 6, lat_width=lat_decimal_length + 6,
            pression_width=pression_width, time_width=time_decimal_length
        )
    
    ##################
    ## DEPLACEMENTS ##
    ##################
   
    def up(self, temps_exploration : int, goal_long, goal_lat, tab_vent : dict):
        if self.p == 0 :
            self.follow_wind(temps_exploration, goal_long, goal_lat, tab_vent)
            return
        self.p -= 1
        self.t += 0 # A MODIFIER Apres apprentissage

    def down(self, temps_exploration : int, goal_long, goal_lat, tab_vent : dict):
        if self.p == 16 :
            self.follow_wind(temps_exploration, goal_long, goal_lat, tab_vent)
            return
        self.p += 1
        self.temps += 0 # A MODIFIER Apres apprentissage

    def follow_wind(self, temps_exploration : int, goal_long, goal_lat, tab_vent : dict) -> bool:
        # utiliser la fonction d'interpolation de hippo et 
        # laisser le ballon évoluer selon le vent choisi pendant temps_exploration
        """
        on actualise les données du ballon et on renvoie un booleen si on est entre dans une zone limite autour
        d'une position objectif
        """
        long = self.long 
        lat = self.lat
        pression = self.p
        temps_init = (self.t - dt.datetime(2020, 1, 1, 0, 0)).total_seconds()
        temps_case = temps_init%21600
        temps_restant = temps_exploration
        precision = self.precision

        # On utilise la précision pour déterminer la fréquence à laquelle on vérifie si on a atteint la destination (temps en secondes). 
        # On estime arbitrairement la vitesse des vents.
        vitesse_moyenne_vents = 7
        temps_test_arrivee = math.ceil(precision/vitesse_moyenne_vents)

        # Constante utile : (rayon de la Terre en m et conversion degrés en radians)
        k = 1000 * 6371 * math.pi / 180

        while(temps_restant>0):

            # On s'assure que les valeurs de longitude et latitude soient dans le bon intervalle.
            (long, lat) = mod(long, lat)
            self.lat = lat
            self.long = long

            # On vérifie si on a atteint la destination. Si oui on renvoie notre position.
            if distance_destination((goal_long, goal_lat),long,lat) <= precision:
                return True
        
            # On récupère les données de vent (en m.s-1). Grâce aux hypothèses sur les temps on sait qu'on reste dans la même case temporelle.
            ventU, ventV = self.exact_winds(tab_vent)

            # On met à jour les valeurs de longitude et latitude.
            temps_evolution = min(temps_restant, temps_test_arrivee)
            lat += (temps_evolution*ventV)/k
            long += (temps_evolution*ventU)/k
            temps_restant -= temps_evolution

            #on met à jour ces valeurs pour le ballon également
            self.t += dt.timedelta(seconds = temps_evolution)
            self.lat = lat
            self.long = long

        # On s'assure que les valeurs de longitude et latitude soient dans le bon intervalle.
        (long, lat) = mod(long, lat)
        self.lat, self.long = lat, long
        
        return (False)


    """
    INPUT : Une instance de notre objet ballon
    OUTPUT : a sub-array of wind_data centered around the coordinates of the balloon
    """
    def get_winds(self, tab_vent : dict):
        long, lat, p = self.long, self.lat,self.p
        temps = (self.t - dt.datetime(2020, 1, 1, 0, 0)).total_seconds()
        tabVent = []
        #On met le vent en position actuelle
        tabVent.append(ventU_ventV_interpolate(long, lat, temps, p, tab_vent))
        coords = coord_list(long, lat, temps, p)
        for i in range(len(coords)):
            if coords[i][0] :
                tabVent.append(ventU_ventV_interpolate(coords[i][1][0], coords[i][1][1], coords[i][1][2], coords[i][1][3], tab_vent))
            else :
                tabVent.append((0,0))
        return  tabVent

    def exact_winds(self, tab_vent: dict):
        temps = (self.t - dt.datetime(2020, 1, 1, 0, 0)).total_seconds()
        return ventU_ventV_interpolate(self.long, self.lat, temps, self.p, tab_vent)


###########################
## FONCTIONS AUXILIAIRES ##
###########################

def cubic_mask(delta, r_x, r_y, r_z, n_t):
    d = delta
    mask = []
    for i in range(-r_x,r_x):
        s = []
        for j in range(-r_y,r_y):
            u = []
            for k in range(0,17):
                v = []
                for l in range(r_t):
                    v.append((d*i,d*j,k,l))
                u.append(v)
            s.append(u)
        mask.append(s)

    return mask

def get_winds_around_point(longitude, latitude, temps,  tab_vent):
    mask = cubic_mask(1, 1, 1, 1, 1)  # Example mask parameters, adjust as needed
    coords = coord_list(longitude, latitude, 0, 0, mask)
    winds = []
    for coord in coords:
        if coord[0]:
            winds.append(ventU_ventV_interpolate(coord[1][0], coord[1][1], coord[1][2], coord[1][3], tab_vent))
        else:
            winds.append((0, 0))
    return winds




#MONCEF decided : pas  = 50


def coord_list(long, lat, temps, p, mask) : #ICI ON rajoute le masque fournit par MONCEF et on rajoute les coordonnées modifiées
    # Constante utile : (rayon de la Terre en m et conversion degrés en radians)
    k = 1000 * 6371 * math.pi / 180
    res = []
    #On considere un cube de cote 2*temps_expl*vitessM centre sur le point inital et on considere les points au centre de chacune de ses faces
    cote = 10000
    for i in range(2):
        if ((p + 2*i-1) >= 0 and (p + 2*i-1) <= 16) :
            res.append([True, [long, lat, temps+131, p + 2*i-1]])
        else :
            res.append([False, []])
    for i in range(2):
        if ((p + 2*(2*i-1)) >= 0 and (p + 2*(2*i-1)) <= 16) :
            res.append([True, [long, lat, temps+2*131, p + 2*(2*i-1)]])
        else :
            res.append([False, []])
    
    #Ajout des logitudes modifiées
    r_ajus = 1000 * 6371 * math.cos(lat*math.pi/180)
    delta_long = 360 * cote/(2*math.pi*r_ajus)
    for i in range(2):
        long_ajus = long +(2*i-1)*delta_long
        res.append([True,[mod_long(long_ajus), lat, temps+131, p]])
    for i in range(2):
        long_ajus = long +(2*i-1)*2*delta_long
        res.append([True,[mod_long(long_ajus), lat, temps+2*131, p]])
    
    #Ajout des latitudes modifiées
    r_ajus = 1000 * 6371
    delta_lat = 360 * cote/(2*math.pi*r_ajus)
    for i in range(2):
        lat_ajus = lat +(2*i-1)*delta_lat
        res.append([True,[long, mod_lat(lat_ajus), temps+131, p]])
    for i in range(2):
        lat_ajus = lat +(2*i-1)*2*delta_lat
        res.append([True,[long, mod_lat(lat_ajus), temps+2*131, p]])
    return res


def test() :
    long, lat, temps, p = 2.2118199376859393,48.710240264856644, 0, 4
    coords = coord_list(long, lat, temps, p)    
    for i in range(len(coords)):
        if coords[i][0] :
            print(coords[i][1])

        

def testClass() :
    ballon : Balloon
    #print(type(ballon))
    long, lat, temps, p = 2.2118199376859393,48.710240264856644, 1000, 1
    date = dt.datetime(2020, 1, 1) + dt.timedelta(seconds=temps)

    ballon = Balloon(long, lat, date, p, None, 1000)
    print(ballon.__str__())

    """
    ballon.follow_wind(131, 2, 4, wind_data)
    print(ballon.__str__())
    """
    print(ballon.exact_winds(wind_data))
    print("voici le tableau des vents")
    print(len(ballon.get_winds(wind_data)))



#testClass()
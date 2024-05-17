#########################           ##################
## MODULES NÉCESSAIRES ##           ## VERSION TEST ##
#########################           ##################

import random
import time

from villes import *
from Affichage import *
#from Affichage import animation
import matplotlib.pyplot as plt
from parcours_interpolate import *
import datetime as dt

import pickle

picke_file_path = "/users/eleves-b/2022/mathias.perez/Documents/DATA_VENT/objet_wind_data_2021.pickle"
with open(picke_file_path, "rb") as f:
   wind_data = pickle.load(f)
   
def generate_random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + dt.timedelta(days=random_number_of_days)
    hr  = random.randrange(0, 24, 6)
    random_time = dt.time(hour=hr, minute=0, second=0, microsecond=0, tzinfo=None, fold=0)
    return dt.datetime.combine(random_date, random_time)   


###########


blue_colors = ['blue', 'dodgerblue', 'deepskyblue', 'skyblue', 'lightblue', 'powderblue', 'lightsteelblue', 'steelblue', 'royalblue', 'blue', 'mediumblue', 'darkblue', 'navy', 'midnightblue']

def test_colors() :
    # print a simple image with all the colors
    fig, ax = plt.subplots()
    for i in range(13):
        ax.scatter([i], [i], color=blue_colors[i], label=blue_colors[i])
    ax.legend()
    plt.savefig("test_colors.png")
    
# test_colors()


def affich_exp() :
    ville_depart = Ville("Paris", 2.3522, 48.8566)
    duree = 120
    temps = int((generate_random_date(dt.datetime(2021, 1, 1), dt.datetime(2021, 12, 24))-dt.datetime(2021, 1, 1)).total_seconds())
    depart = Node(ville_depart.long, ville_depart.lat, temps, 16, None) 
    liste_point = [depart]
    visupoints(liste_point, color = 'red')
    liste_next = []
    for j in range(duree//6) :
        liste_next = []
        print(j)
        print(len(liste_point))
        for point in liste_point :
            for i in range(17):
                point.p = i
                liste_next.append(parcours_a_Z_interpolate((0, -90), point, 6*3600,10000, wind_data)[1])

        liste_point = liste_next
        visupoints(liste_point, color = 'red')
        

affich_exp()
        


    

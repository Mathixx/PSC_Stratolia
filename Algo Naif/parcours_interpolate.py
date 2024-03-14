#########################
## MODULES NÉCESSAIRES ##
#########################


import math
from data_vent import *
import sys
from Node import *


#########################
## FONCTION PRINCIPALE ##
#########################


"""
Ce programme détermine l'évolution du ballon supposé à altitude fixée pendant une fenêtre de temps données. Si pendant cette évolution
le ballon rencontre la destination, on s'arrête et on le signale.

Entrée : 
- destination : longitude, latitude
- position initiale : longitude, latitude, temps, pression
- durée de l'évolution (en secondes)
- précisison (distance à la destination voulue en m)
- données de vent

Sortie :
- booléen indiquant si on a rencontré la destination
- position finale : longitude, latitude, temps, pression
"""


def parcours_a_Z(destination : (float,float), n : Node, temps_chgmt_pression : int, precision : int, tab_vent : dict) -> (bool,Node)  :
    long = n.long
    lat = n.lat
    temps = n.t
    pression = n.p
    temps_init = temps[0]
    temps_restant = temps_chgmt_pression
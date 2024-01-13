import math
import sys
from parcours import parcours_a_Z
from makeTree import Tree_Largeur

import pickle
with open("objet_wind_data_2020.pickle", "rb") as f:
    wind_data = pickle.load(f)

"""
Coordonnées du 73 boulevard des maréchaux : 
longitude ->  2.211653
latitude -> 48.709859

cela donne dans le tableau : 
longitude : (0, 247705.136)
latitude : (55, 135504.20799999937)


https://www.coordonnees-gps.fr
"""

def convPrg_Coord(longitude : (int,int), latitude : (int,int)) -> (int, int):
    return (longitude[0]*2.5+2.5*longitude[1]/280000, latitude[0]*2.5-90+latitude[1]/280000*2.5)

def convCoord_Prg(longitude, latitude) :
    x0 = math.floor(longitude/2.5)
    x1 = (longitude - 2.5*x0)*280000/2.5
    y0 = math.floor((latitude+90)/2.5)
    y1 = (latitude+90-2.5*y0)*280000/2.5
    return ((x0,x1),(y0,y1))


"""
for pression in range (17) :
    #je fais evoluer pendant 10j
    print("pression : "+ str(pression))
    (long, lat) = parcours_a_Z((0, 247705.136), (55, 135504.20799999937), pression, wind_data, 0, 90)
    print (convPrg_Coord(long,lat))
"""

destination  = convCoord_Prg((2.2101489978376114, 48.700457632812494))

result = Tree_Largeur(destination,(0, 247705.136),(55, 135504.20799999937),3, 0, 90)
if result[0] :
    print('ok')
    coords = []
    for n in result[1] :
        x,y = convPrg_Coord(n.long, n.lat)
        z = 20000-n.p*1176
        coords.append((x,y,z))




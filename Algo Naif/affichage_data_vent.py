#########################
## MODULES NÉCESSAIRES ##
#########################


from matplotlib import pyplot as plt
import numpy as np
from data_vent import wind_data


#################################
## ANALYSE DES DONNÉES DE VENT ##
#################################

def affichage_all_vent(wind_data):
    all_ventU = []
    all_ventV = []
    mean_ventU = 0
    mean_ventV = 0
    for temps in range(100):
        # On ne va que jusqu'à 100 sinon il y a trop de données. 
        for pression in range(len(wind_data["data"][temps])):
            for case_longitude in range(len(wind_data["data"][temps][pression])):
                for case_latitude in range(len(wind_data["data"][temps][pression][case_longitude])):
                    all_ventU.append(wind_data["data"][temps][pression][case_longitude][case_latitude][0])
                    all_ventV.append(wind_data["data"][temps][pression][case_longitude][case_latitude][1])

    # On affiche les valeurs de ventU
    plt.hist(all_ventU, bins = 1000, range=(-100,100))
    plt.title("Valeurs de ventU sur l'ensemble de l'année")
    plt.xlabel("Vent U")
    plt.show()
    # plt.savefig('ventU.pdf', bbox_inches='tight')
    plt.close()


    # On affiche les valeurs de ventV
    plt.hist(all_ventV, bins = 1000, range=(-50,50))
    plt.title("Valeurs de ventV sur l'ensemble de l'année")
    plt.xlabel("Vent V")
    plt.show()
    #plt.savefig('ventV.png', bbox_inches='tight')
    plt.close()

#affichage_all_vent(wind_data)

def affichage_vent_p_h_fixes():
    all_ventU = []
    all_ventV = []
    pression = 16
    case_longitude = 0
    case_latitude = 55
    for temps in range(0,1000):
        all_ventU.append(wind_data["data"][temps][pression][case_longitude][case_latitude][0])
        all_ventV.append(wind_data["data"][temps][pression][case_longitude][case_latitude][1])

    # On affiche les valeurs de ventU
    plt.hist(all_ventU)
    plt.title("Valeurs de ventU pour une pression de 16 hPa")
    plt.xlabel("Temps")
    plt.ylabel("Vent U")
    plt.show()
    # plt.savefig('ventU.pdf', bbox_inches='tight')
    plt.close()
    
    # On affiche les valeurs de ventV
    plt.hist(all_ventV)
    plt.title("Valeurs de ventV pour une pression de 16 hPa")
    plt.xlabel("Temps")
    plt.ylabel("Vent V")
    plt.show()
    #plt.savefig('ventV.png', bbox_inches='tight')
    plt.close()

affichage_vent_p_h_fixes()




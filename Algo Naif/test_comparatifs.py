from greedy import *
from selection_search import *
from villes import *

def test():
    # On va tester les deux algorithmes sur les mêmes données.
    # On va choisir deux villes et juste faire changer le temps de départ.
    depart = Ville("Paris", 2.3522, 48.8566)
    dest = Ville("Marseille", 5.3698, 43.2965)
    duree = 180
    temps_chgmt_pression = 3600
    precision = 10000
    tab_reussi_greedy = 50*[0]
    tab_reussi_selection = 50*[0]
    for i in range(0,25):
        tab_reussi_greedy[i] = greedy((dest.long, dest.lat), Node(depart.long, depart.lat, i*10*21600, pression=0, prev=None), duree, temps_chgmt_pression, precision, wind_data)[0]
        tab_reussi_selection[i] = N_closest((dest.long, dest.lat), Node(depart.long, depart.lat, i*10*21600, pression=0, prev=None), duree, temps_chgmt_pression, precision, 1.2, wind_data)[0]
    # On compte le nombre de paires true, true; true, false; false, true; false, false
    nb_true_true = 0
    nb_true_false = 0
    nb_false_true = 0
    nb_false_false = 0
    for i in range(0,25):
        if tab_reussi_greedy[i] and tab_reussi_selection[i]:
            nb_true_true += 1
        elif tab_reussi_greedy[i] and not tab_reussi_selection[i]:
            nb_true_false += 1
        elif not tab_reussi_greedy[i] and tab_reussi_selection[i]:
            nb_false_true += 1
        else:
            nb_false_false += 1
    for i in range(0,25):
        print("Temps départ = "+str(i*10)+ " : "+str(tab_reussi_greedy[i])+ " | "+str(tab_reussi_selection[i]))
    print("Nombre de paires true, true : "+str(nb_true_true))
    print("Nombre de paires true, false : "+str(nb_true_false))
    print("Nombre de paires false, true : "+str(nb_false_true))
    print("Nombre de paires false, false : "+str(nb_false_false))
    

test()
    
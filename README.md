# PSC_Stratolia
Partie Naïve :


Le tableau wind_data est un tableau 4D :
    1 donnée de temps : résolution d'un point toutes les 6 heures.
    1 donnée de pression 
    2 données de longitude et de latitude : résolution  2,5 °.
    2 données de vent U, V ( U dans la direction Sud->Nord; V dans la direction Ouest -> Est)
    

Les vents sont des vecteurs 2D. La composante z est toujours considérée comme nulle. 
La composante u est la composante ouest -> est et la composante v est la composante sud -> nord.
Voici un mémo sur la représentation des vents : http://colaweb.gmu.edu/dev/clim301/lectures/wind/wind-uv

Notes sur les coordonnées : 
    Les cases divisent la surface du globe en termes de latitude et de longitude avec une résolution de 2,5°. On peut en déduire la largeur et la longueur des cases lorsqu'on décide de projeter sur le plan de la surface terrestre. Les cases ont toutes la même longueur (au sens de la distance Nord-Sud) qui vaut environ 278km. Par contre la largeur d'une case (au sens de la distance Est-Ouest) dépend de la latitude suivant la formule : L = 278 * cos(lat).

    On note les positions sont la forme de deux flottants long-lat. On a donc les conversions suivantes pour obtenir les angles qui correspondent aux entiers.
    Latitude d'une case : -90° + 2,5° * int <= lat <= -90° + 2,5° * (int+1)                   Total : 72 subdivisions.
    Longitude d'une case : 0° + 2,5° * int <= long <= 0° + 2,5° * (int+1)                     Total : 144 subdivisions.
    
Note sur le coordonnées de temps : 
    On décrit le temps avec un couple (int, int). La première coordonnée décrit notre position dans le tableau wind_data et la deuxième le nombre de secondes écoulées au sein de cette case (qui dure six heures pour rappel).



Historique modifications : 

2.0 Hippo : 
- modifications de la classe Node pour garantir le type entier de la pression et du temps tout au long des fonctions
- modifications de la fonction print(node) pour que les barres verticales soient toujours alignées 
- modifications mineures sur les tests d'argument au début de makeTree (ValueError)

2.1 Hippo :
- erreur corrigée dans ventUventV sur l'appel à wind_data
- création du fichier test_parcours et ecriture d'un test
- nettoyage des commentaires

2.2 Hippo : 
2.2.0
- correction de la fonction distance : résolution d'erreur quand on est de part et d'autre du méridien 0
- écriture de test_makeTree
2.2.1
- changement de la condition d'arrêt sur liste P
2.2.2
- introduction constante de rétrecissement


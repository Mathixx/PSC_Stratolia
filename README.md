# PSC_Stratolia
Partie Naïve :


Le tableau wind_data est un tableau 4D :
    1 donnée de temps : résolution d'un point toutes les 6 heures.
    2 données de longitude et de latitude : résolution  2,5 °.
    1 donnée de pression 
    2 données de vent U, V ( U dans la direction Sud->Nord; V dans la direction Ouest -> Est)
    

Les vents sont des vecteurs 2D. La composante z est toujours considérée comme nulle. 
La composante u est la composante ouest -> est et la composante v est la composante sud -> nord.
Voici un mémo sur la représentation des vents : http://colaweb.gmu.edu/dev/clim301/lectures/wind/wind-uv

Notes sur les coordonnées : 
    Les cases divisent la surface du globe en termes de latitude et de longitude avec une résolution de 2,5°. On peut en déduire la largeur et la longueur des cases lorsqu'on décide de projeter sur le plan de la surface terrestre. Les cases ont toutes la même longueur (au sens de la distance Nord-Sud) qui vaut environ 278km. Par contre la largeur d'une case (au sens de la distance Est-Ouest) dépend de la latitude suivant la formule : L = 278 * cos(lat).

    On note les positions sont la forme de deux couples latitude(int,float) et longitude(int,float). L'entier correspond à la numérotation des latitudes et longitudes dans le tableau wind_data. On a donc les conversions suivantes pour obtenir les angles qui correspondent aux entiers.
    Latitude d'une case : -90° + 2,5° * int <= lat <= -90° + 2,5° * (int+1)                   Total : 72 subdivisions.
    Longitude d'une case : 0° + 2,5° * int <= long <= 0° + 2,5° * (int+1)                     Total : 144 subdivisions.
    Ensuite le flottant décrit la latitude et la longitude détaillée du point. On a donc les relations suivantes :
    latitude[0] = (2*(latitude[1]+90))//5 et longitude[0] = (2*(longitude[1]+90))//5

Note sur le coordonnées de temps : 
    On décrit le temps avec un couple (int, int). La première coordonnée décrit notre position dans le tableau wind_data et la deuxième le nombre de secondes écoulées au sein de cette case (qui dure six heures pour rappel).

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

    On note les positions sont la forme de deux flottants long-lat. On a donc les conversions suivantes pour obtenir les angles qui correspondent aux entiers.
    Latitude d'une case : -90° + 2,5° * int <= lat <= -90° + 2,5° * (int+1)                   Total : 72 subdivisions.
    Longitude d'une case : 0° + 2,5° * int <= long <= 0° + 2,5° * (int+1)                     Total : 144 subdivisions.
    
Note sur le coordonnées de temps : 
    On décrit le temps avec un couple (int, int). La première coordonnée décrit notre position dans le tableau wind_data et la deuxième le nombre de secondes écoulées au sein de cette case (qui dure six heures pour rappel).



TO DO : 
- EASY : améliorer l'affichage : calibrer les distances pour que les barres verticales soient toujours alignées
- MOYEN : mettre en lien les algos avec l'interface graphique
- MOYEN :corriger le problème du calcul de ventU ventV qaund on change de case (on avait vu que parfois on utilise le vent de la mauvaise case)
- HARD : améliorer le calcul de la limite d'éloignement - réflechir à la meilleur manière de faire
- 
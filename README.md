# PSC_Stratolia
Codes pour le PSC

Partie Naïve :


Le tableau wind_data ets un tableau 4D :
    1 données de temps : résolution d'un point toutes les 6 heures.
    2 données de longitude et de latitude : résolution  2,5 ° , soit un point tous les 278 km environ
    1 données de pression 
    Et en fin 2 données de vent U, V ( U dans la direction Sud->Nord; V dans la direction Ouest -> Est)
    

Les vents sont des vecteurs 2D. La composante z est considérée comme toujours nulle. 
La composante u est la composante ouest -> est et la composante v est la composante sud -> nord.
Voici un mémo sur la représentation des vents : http://colaweb.gmu.edu/dev/clim301/lectures/wind/wind-uv

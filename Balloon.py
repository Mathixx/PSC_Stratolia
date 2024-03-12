import datetime as dt
"""
Est ce que l'on garde le champ prev alors qu'on en aura potentiellement pas beosin car on explore une seul option a chaque fois
le render peut se demerder ? 

Quid du fait d'appler up quand t'es deja en limte ?

"""
class Balloon:
    def __init__(self, longitude : float, latitude :  float, temps : dt.datetime, pression, prev):
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
        self.prev = prev

    def __str__(self):
        long_decimal_length = len(str('{:.6f}'.format(self.long).split('.')[1]))
        lat_decimal_length = len(str('{:.6f}'.format(self.lat).split('.')[1]))
        #time_decimal_length = max(len(str(self.t)))

        # Largeur fixe pour le champ "Pression"
        pression_width = 3

        return "Longitude: {:{long_width}.{long_width}f} | Latitude: {:{lat_width}.{lat_width}f} | Pression: {:{pression_width}d} | Date: {:d}".format(
            self.long, self.lat, self.p, self.t,
            long_width=long_decimal_length + 6, lat_width=lat_decimal_length + 6,
            pression_width=pression_width
        )

    def up(self, temps_exploration : int):
        if self.p == 0 :
            self.follow_wind(temps_exploration)
            return
        self.p -= 1
        self.temps += dt.timedelta(seconds=131)

    def down(self, temps_exploration : int):
        if self.p == 16 :
            self.follow_wind(temps_exploration)
            return
        self.p += 1
        self.temps += dt.timedelta(seconds=131)

    def follow_wind(self, temps_exploration : int) -> bool:
        # utiliser la fonction d'interpolation de hippo et 
        # laisser le ballon évoluer selon le vent choisi pendant temps_exploration
        """
        on actualise les données du ballon et on renvoie un booleen si on est entre dans une zone limite autour
        d'une position objectif
        """
        pass


        """
        INPUT : Une instance de notre objet ballon
        OUTPUT : a sub-array of wind_data centered around the coordinates of the balloon
        """
    def get_winds(self):
        # Il reste a definir l'echantillonage souhaité pour le tableau de vents en sortie
        pass

    def exact_winds(self):
        #utiliser l'interpolation de hippo
        pass
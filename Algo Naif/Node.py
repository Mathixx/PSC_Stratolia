class Node:
    def __init__(self, longitude, latitude, temps, pression, prev):
        self.long = longitude
        self.lat = latitude
        # Vérification que temps est un couple d'entiers
        if not isinstance(temps, tuple) or len(temps) != 2 or not all(isinstance(t, int) for t in temps):
            raise ValueError("Le temps doit être un couple d'entiers.")
        self.t = temps
        # Vérification que pression est un entier
        if not isinstance(pression, int):
            raise ValueError("La pression doit être un entier.")
        self.p = pression
        self.prev = prev

    def __str__(self):
        long_decimal_length = len(str('{:.6f}'.format(self.long).split('.')[1]))
        lat_decimal_length = len(str('{:.6f}'.format(self.lat).split('.')[1]))
        time_decimal_length = max(len(str(self.t[0])), len(str(self.t[1])))

        # Largeur fixe pour le champ "Pression"
        pression_width = 3

        return "Longitude: {:{long_width}.{long_width}f} | Latitude: {:{lat_width}.{lat_width}f} | Pression: {:{pression_width}d} | Case temporelle: {:d} | Secondes: {:{secondes_width}d}".format(
            self.long, self.lat, self.p, self.t[0], self.t[1],
            long_width=long_decimal_length + 6, lat_width=lat_decimal_length + 6,
            pression_width=pression_width, secondes_width=time_decimal_length 
        )


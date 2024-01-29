
class Node :
    def __init__(self, longitude, latitude, temps, pression, prev):
        self.long = longitude
        self.lat = latitude
        self.t = temps
        self.p = pression
        self.prev = prev

def toString(self):
    return ("Longitude : "+str(self.long)+" | Latitude : " + str(self.lat)+ " | Pression  : "+str(self.p)+" | Temps : "+str(self.t))
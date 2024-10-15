class City:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = float(lat)
        self.lon = float(lon)
        self.adjacent = []

class Graph:
    def __init__(self):
        self.cities = {}

    def add_city(self, name, lat, lon):
        self.cities[name] = City(name, lat, lon)

    def add_edge(self, city1, city2):
        self.cities[city1].adjacent.append(city2)
        self.cities[city2].adjacent.append(city1)
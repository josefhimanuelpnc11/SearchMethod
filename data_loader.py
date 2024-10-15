import csv
from models import Graph

def load_cities(filename):
    graph = Graph()
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 3:
                name, lat, lon = row
                graph.add_city(name, float(lat), float(lon))
            else:
                print(f"Warning: Ignoring invalid line in cities file: {','.join(row)}")
    return graph

def load_adjacencies(filename, graph):
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                city1, city2 = parts
                if city1 in graph.cities and city2 in graph.cities:
                    graph.add_edge(city1, city2)
                else:
                    print(f"Warning: One or both cities not found in graph: {city1}, {city2}")
            else:
                print(f"Warning: Ignoring invalid line in adjacencies file: {line.strip()}")
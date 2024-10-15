import matplotlib.pyplot as plt

def create_map(graph, solution_path=None):
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot all cities
    for city in graph.cities.values():
        ax.plot(city.lon, city.lat, 'bo')  # Blue dots for cities
        ax.annotate(city.name, (city.lon, city.lat), fontsize=8, ha='right', va='bottom')
    
    # Plot existing paths
    for city in graph.cities.values():
        for adjacent in city.adjacent:
            adjacent_city = graph.cities[adjacent]
            ax.plot([city.lon, adjacent_city.lon], [city.lat, adjacent_city.lat], 'g-', linewidth=0.5, alpha=0.5)
    
    # Plot the solution path if provided
    if solution_path:
        path_lons = [graph.cities[city].lon for city in solution_path]
        path_lats = [graph.cities[city].lat for city in solution_path]
        ax.plot(path_lons, path_lats, 'r-', linewidth=2)  # Red line for the solution path
    
    ax.set_title("City Map with Route")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(True)

    # Add legend
    ax.plot([], [], 'bo', label='Cities')
    ax.plot([], [], 'g-', label='Existing Paths', linewidth=0.5, alpha=0.5)
    if solution_path:
        ax.plot([], [], 'r-', label='Solution Path', linewidth=2)
    ax.legend()

    return fig
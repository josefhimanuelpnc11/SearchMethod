import math

def haversine_distance(city1, city2):
    R = 6371  # Earth's radius in kilometers
    lat1, lon1 = math.radians(city1.lat), math.radians(city1.lon)
    lat2, lon2 = math.radians(city2.lat), math.radians(city2.lon)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def bfs(graph, start, goal):
    queue = [[start]]
    visited = set()
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node not in visited:
            visited.add(node)
            if node == goal:
                return path
            for adjacent in graph.cities[node].adjacent:
                new_path = list(path)
                new_path.append(adjacent)
                queue.append(new_path)
    return None

def dfs(graph, start, goal, path=None, visited=None):
    if path is None:
        path = [start]
    if visited is None:
        visited = set()
    visited.add(start)
    if start == goal:
        return path
    for adjacent in graph.cities[start].adjacent:
        if adjacent not in visited:
            new_path = dfs(graph, adjacent, goal, path + [adjacent], visited)
            if new_path:
                return new_path
    return None

def id_dfs(graph, start, goal, max_depth):
    for depth in range(max_depth):
        result = depth_limited_search(graph, start, goal, depth)
        if result is not None:
            return result
    return None

def depth_limited_search(graph, node, goal, depth, path=None):
    if path is None:
        path = [node]
    if depth == 0 and node == goal:
        return path
    elif depth > 0:
        for adjacent in graph.cities[node].adjacent:
            if adjacent not in path:
                new_path = depth_limited_search(graph, adjacent, goal, depth - 1, path + [adjacent])
                if new_path:
                    return new_path
    return None

def best_first_search(graph, start, goal):
    queue = [(0, [start])]
    visited = set()
    while queue:
        (cost, path) = queue.pop(0)
        node = path[-1]
        if node not in visited:
            visited.add(node)
            if node == goal:
                return path
            for adjacent in graph.cities[node].adjacent:
                if adjacent not in visited:
                    new_path = path + [adjacent]
                    priority = haversine_distance(graph.cities[adjacent], graph.cities[goal])
                    queue.append((priority, new_path))
                    queue.sort(key=lambda x: x[0])
    return None

def a_star(graph, start, goal):
    queue = [(0, 0, [start])]
    visited = set()
    while queue:
        (f, g, path) = queue.pop(0)
        node = path[-1]
        if node not in visited:
            visited.add(node)
            if node == goal:
                return path
            for adjacent in graph.cities[node].adjacent:
                if adjacent not in visited:
                    new_path = path + [adjacent]
                    new_g = g + haversine_distance(graph.cities[node], graph.cities[adjacent])
                    h = haversine_distance(graph.cities[adjacent], graph.cities[goal])
                    f = new_g + h
                    queue.append((f, new_g, new_path))
                    queue.sort(key=lambda x: x[0])
    return None
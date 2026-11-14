"""Graph search algorithms for a UAB Artificial Intelligence coursework project.

Based on the course's provided assignment scaffold; implemented as an academic project.
Student identifier removed from this portfolio copy.
"""

from SubwayMap import *
from utils import *
import os
import math
import copy


def expand(path, map):
    """
     It expands a SINGLE station and returns the list of class Path.
     Format of the parameter is:
        Args:
            path (object of Path class): Specific path to be expanded
            map (object of Map class):: All the information needed to expand the node
        Returns:
            path_list (list): List of paths that are connected to the given path.
    """
    path_list = []
    estacio_actual = path.route[-1]

    if estacio_actual in map.connections:
        for proxima_estacio in map.connections[estacio_actual]:
            nova_ruta = path.route + [proxima_estacio]
            nou_path = Path(nova_ruta)
            path_list.append(nou_path)

    return path_list


def remove_cycles(path_list):
    """
     It removes from path_list the set of paths that include some cycles in their path.
     Format of the parameter is:
        Args:
            path_list (LIST of Path Class): Expanded paths
        Returns:
            path_list (list): Expanded paths without cycles.
    """
    valid_paths = []

    for path in path_list:
        estacio_actual = path.route[-1]
        estacions_previes = path.route[:-1]
        if estacio_actual not in estacions_previes:
            valid_paths.append(path)

    return valid_paths


def insert_depth_first_search(expand_paths, list_of_path):
    """
     expand_paths is inserted to the list_of_path according to DEPTH FIRST SEARCH algorithm
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            list_of_path (LIST of Path Class): The paths to be visited
        Returns:
            list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    return expand_paths + list_of_path


def depth_first_search(origin_id, destination_id, map):
    """
     Depth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): the route that goes from origin_id to destination_id
    """
    list_of_path = [Path([origin_id])]

    while list_of_path != [] and list_of_path[0].route[-1] != destination_id:
        c = list_of_path.pop(0)
        e = expand(c, map)
        e = remove_cycles(e)
        list_of_path = insert_depth_first_search(e, list_of_path)

    if list_of_path != []:
        return list_of_path[0]

    return None

def insert_breadth_first_search(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to BREADTH FIRST SEARCH algorithm
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    return list_of_path + expand_paths


def breadth_first_search(origin_id, destination_id, map):
    """
     Breadth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    list_of_path = [Path([origin_id])]

    while list_of_path != [] and list_of_path[0].route[-1] != destination_id:
        c = list_of_path.pop(0)
        e = expand(c, map)
        e = remove_cycles(e)
        list_of_path = insert_breadth_first_search(e, list_of_path)

    if list_of_path != []:
        return list_of_path[0]

    return None


def calculate_cost(expand_paths, map, type_preference=0):
    """
         Calculate the cost according to type preference
         Format of the parameter is:
            Args:
                expand_paths (LIST of Paths Class): Expanded paths
                map (object of Map class): All the map information
                type_preference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
            Returns:
                expand_paths (LIST of Paths): Expanded path with updated cost
    """
    for path in expand_paths:
        penultim = path.penultimate
        ultim = path.last
        if type_preference == 0:
            g = 1
            path.update_g(g)
        elif type_preference == 1:
            g = map.connections[penultim][ultim]
            path.update_g(g)
        elif type_preference == 2:
            linia = map.stations[penultim]['line']
            final = map.stations[ultim]['line']
            if linia == final:
                vel = map.stations[penultim]['velocity']
                g = map.connections[penultim][ultim]*vel
                path.update_g(g)
            else:
                g = 0
                path.update_g(g)
        elif type_preference == 3:
            linia = map.stations[penultim]['line']
            final = map.stations[ultim]['line']
            if linia != map.stations[ultim]['line']:
                g = 1
                path.update_g(g)
            else:
                g = 0
        else:
            return None

    return expand_paths


def insert_cost(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to COST VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to cost
    """
    for nou_cami in expand_paths:
        inserit = False

        for i in range(len(list_of_path)):
            if nou_cami.g < list_of_path[i].g:
                list_of_path.insert(i, nou_cami)
                inserit = True
                break

        if not inserit:
            list_of_path.append(nou_cami)

    return list_of_path


def uniform_cost_search(origin_id, destination_id, map, type_preference=0):
    """
     Uniform Cost Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    list_of_path = [Path([origin_id])]
    while list_of_path:
        final = list_of_path.pop(0)
        if destination_id == final.last:
            return final
        else:
            expanded_paths = expand(final, map)
            for p in expanded_paths:
                p.g = final.g
            path_cost = calculate_cost(expanded_paths, map, type_preference)
            path_sense_cicles = remove_cycles(path_cost)
            list_of_path = insert_cost(path_sense_cicles, list_of_path)
    return None


def calculate_heuristics(expand_paths, map, destination_id, type_preference=0):
    """
     Calculate and UPDATE the heuristics of a path according to type preference
     WARNING: In calculate_cost, we didn't update the cost of the path inside the function
              for the reasons which will be clear when you code Astar (HINT: check remove_redundant_paths() function).
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            map (object of Map class): All the map information
            destination_id (int): Final station id
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            expand_paths (LIST of Path Class): Expanded paths with updated heuristics
    """
    x_d = map.stations[destination_id]['x']
    y_d = map.stations[destination_id]['y']

    for path in expand_paths:

        if type_preference == 0:
            if path.last != destination_id:
                heuristic = 1
                path.update_h(heuristic)
            else:
                heuristic = 0
                path.update_h(heuristic)

        elif type_preference == 1:
            x = map.stations[path.last]['x']
            y = map.stations[path.last]['y']
            dist = euclidean_dist((x, y), (x_d, y_d))
            max_vel = 0
            for k in map.velocity.keys():
                v = map.velocity[k]
                if v > max_vel:
                    max_vel = v
            heuristic = dist/max_vel
            path.update_h(heuristic)

        elif type_preference == 2:
            x = map.stations[path.last]['x']
            y = map.stations[path.last]['y']
            h = euclidean_dist((x, y), (x_d, y_d))
            path.update_h(h)

        elif type_preference == 3:
            linia_actual = map.stations[path.last]['line']
            linia_desti = map.stations[destination_id]['line']
            if linia_actual == linia_desti:
                h = 0
            else:
                h = 1
            path.update_h(h)

        else:
            return None

    return expand_paths


def update_f(expand_paths):
    """
      Update the f of a path
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
         Returns:
             expand_paths (LIST of Path Class): Expanded paths with updated costs
    """
    for path in expand_paths:
        path.update_f()
    return expand_paths


def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost):
    """
      It removes the Redundant Paths. They are not optimal solution!
      If a station is visited and have a lower g-cost at this moment, we should remove this path.
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
             list_of_path (LIST of Path Class): All the paths to be expanded
             visited_stations_cost (dict): All visited stations cost
         Returns:
             new_paths (LIST of Path Class): Expanded paths without redundant paths
             list_of_path (LIST of Path Class): list_of_path without redundant paths
             visited_stations_cost (dict): Updated visited stations cost
    """
    new_paths = []

    for path in expand_paths:
        id_ultima_estacio = path.last
        nou_cost = path.g

        if id_ultima_estacio not in visited_stations_cost:
            visited_stations_cost[id_ultima_estacio] = nou_cost
            new_paths.append(path)
        else:
            cost_anterior = visited_stations_cost[id_ultima_estacio]

            if nou_cost >= cost_anterior:
                continue

            visited_stations_cost[id_ultima_estacio] = nou_cost
            new_paths.append(path)

            llista_filtrada = []
            for pendent in list_of_path:
                if id_ultima_estacio not in pendent.route:
                    llista_filtrada.append(pendent)
            list_of_path = llista_filtrada

    return new_paths, list_of_path, visited_stations_cost


def insert_cost_f(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to f VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to f
    """
    for expanded_path in expand_paths:
        inserted = False
        new_list_of_path = []

        for existing_path in list_of_path:
            if (not inserted) and (expanded_path.f < existing_path.f):
                new_list_of_path.append(expanded_path)
                inserted = True
            new_list_of_path.append(existing_path)

        if not inserted:
            new_list_of_path.append(expanded_path)

        list_of_path = new_list_of_path

    return list_of_path


def distance_to_stations(coord, map):
    """
        From coordinates, it computes the distance to all stations in map.
        Format of the parameter is:
        Args:
            coord (list): Two REAL values, which refer to the coordinates of a point in the city.
            map (object of Map class): All the map information
        Returns:
            (dict): Dictionary containing as keys, all the Indexes of all the stations in the map, and as values, the
            distance between each station and the coord point
    """
    diccionari = {}
    llista = []

    for station_id in map.stations:
        x = map.stations[station_id]["x"]
        y = map.stations[station_id]["y"]

        dx = coord[0] - x
        dy = coord[1] - y

        distancia = math.sqrt(dx*dx + dy*dy)
        llista.append((distancia, station_id))

    llista.sort()

    for distancia, station_id in llista:
        diccionari[station_id] = distancia

    return diccionari


def Astar(origin_id, destination_id, map, type_preference=0):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    list_of_path = [Path([origin_id])]
    visited_stations_cost = {origin_id: 0}

    while list_of_path != [] and list_of_path[0].last != destination_id:

        current_path = list_of_path.pop(0)

        expand_paths = expand(current_path, map)

        for expanded_path in expand_paths:
            expanded_path.g = current_path.g

        expand_paths = remove_cycles(expand_paths)
        expand_paths = calculate_cost(expand_paths, map, type_preference)
        expand_paths = calculate_heuristics(expand_paths, map, destination_id, type_preference)
        expand_paths = update_f(expand_paths)

        resultat = remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost)

        expand_paths = resultat[0]
        list_of_path = resultat[1]
        visited_stations_cost = resultat[2]

        list_of_path = insert_cost_f(expand_paths, list_of_path)

    # No route was found: avoid indexing an empty frontier.
    return list_of_path[0] if list_of_path else None


def Astar_improved(origin_coord, destination_coord, map):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_coord (list): Two REAL values, which refer to the coordinates of the starting position
            destination_coord (list): Two REAL values, which refer to the coordinates of the final position
            map (object of Map class): All the map information

        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_coord to destination_coord
"""
    WALK_SPEED = 5.0
    map_aux = copy.deepcopy(map)
    map_aux.velocity["walk"] = WALK_SPEED

    map_aux.stations[0] = {
        'name': 'Origin',
        'line': 0,
        'x': origin_coord[0],
        'y': origin_coord[1],
        'velocity': WALK_SPEED
    }

    map_aux.stations[-1] = {
        'name': 'Destination',
        'line': 0,
        'x': destination_coord[0],
        'y': destination_coord[1],
        'velocity': WALK_SPEED
    }

    map_aux.connections[0] = {}
    if -1 not in map_aux.connections:
        map_aux.connections[-1] = {}

    map_aux.connections[0][-1] = euclidean_dist(origin_coord, destination_coord) / WALK_SPEED

    dist_from_origin = distance_to_stations(origin_coord, map)

    dist_to_destination = distance_to_stations(destination_coord, map)

    for station_id in map.stations.keys():
        map_aux.connections[0][station_id] = dist_from_origin[station_id] / WALK_SPEED

        if station_id not in map_aux.connections:
            map_aux.connections[station_id] = {}

        map_aux.connections[station_id][-1] = dist_to_destination[station_id] / WALK_SPEED

    return Astar(0, -1, map_aux, 1)

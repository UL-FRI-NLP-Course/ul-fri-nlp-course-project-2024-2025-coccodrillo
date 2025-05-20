import networkx as nx
import pandas as pd
import numpy as np
from places import get_geo
import random


walking_speed_kmh = 5
cost_matrix = None


# Funzione per calcolare il costo totale basato su pesi e importanza
def get_total_cost(beauty, time_to_visit, costo_A_B, importanzaB, importanzaT, importanzaE):
    # Moltiplica ogni peso per l'importanza, maggiore importanza => maggiore influenza
    return (importanzaB * beauty) + (importanzaT *  time_to_visit) + (importanzaE *  costo_A_B)   



# Funzione per calcolare il costo totale di un arco considerando importanza
def calculate_edge_cost(G, i, j, importance_beauty, importance_time_visit, importance_edge):
    beauty = G.nodes[j]['beauty']
    time_to_visit = G.nodes[j]['time_to_visit']
    costo_A_B = cost_matrix[i][j]
    
    # Calcola il costo totale per l'arco (i, j) ponderato dagli importi
    return get_total_cost(beauty, time_to_visit, costo_A_B, importance_beauty, importance_time_visit, importance_edge)

# Function to calculate total time spent based on sum of time to visit (peso2) and edge cost (costo_A_B)
def calculate_total_time(G, path):
    total_time = 0
    for i in range(len(path) - 1):
        current_node = path[i]
        next_node = path[i + 1]
        
        # Add the time to visit (peso2) and the edge cost (costo_A_B)
        peso2_A = G.nodes[current_node]['time_to_visit']
        edge_cost = G[current_node][next_node]['weight']
        
        # Sum of time to visit and the time (cost) for the edge
        total_time += peso2_A + edge_cost

    return total_time



# Function to normalize the input list to [0, 1]
def normalize(values):
    min_val = min(values)
    max_val = max(values)
    return [(v - min_val) / (max_val - min_val) for v in values]


def get_best_k_places(path, G, n_days, hours_per_day=8):
    # Total time available is the product of n_days and hours per day
    available_time = n_days * hours_per_day
    total_time_spent = 0
    places_to_visit = []  # List to store the places we will visit
    k = 0  # Variable to keep track of the number of places
    
    # Iterate over the path to accumulate time and decide which places to visit
    for i in range(len(path) - 1):
        current_node = path[i]
        next_node = path[i + 1]
        
        # Add the time to visit (peso2) and the cost to move between nodes (edge cost)
        peso2_A = G.nodes[current_node]['time_to_visit']
        edge_cost = G[current_node][next_node]['weight']
        
        # Calculate the time spent for this place (time to visit + edge cost)
        time_for_this_place = peso2_A + edge_cost
        
        # Check if we can add this place without exceeding the available time
        if total_time_spent + time_for_this_place <= available_time:
            places_to_visit.append(current_node)
            total_time_spent += time_for_this_place
            k += 1
        else:
            break  # If we exceed the available time, stop
        
    # Optionally, include the last place in the path if it's within the time limit
    if total_time_spent + G.nodes[path[-1]]['time_to_visit'] <= available_time:
        places_to_visit.append(path[-1])
    
    return places_to_visit, total_time_spent




# Function to compute the minimum path for TSP using a greedy approach
def path_min_tsp(G, start_node):
    visited = set()  
    current_node = start_node
    visited.add(current_node)
    path = [current_node] 
    total_cost = 0  

    while len(visited) < len(G.nodes):  
        min_cost = float('inf')
        next_node = None
        for neighbor in G.neighbors(current_node):
            if neighbor not in visited:
                edge_weight = G[current_node][neighbor]['weight']
                if edge_weight < min_cost:
                    min_cost = edge_weight
                    next_node = neighbor
        
        if next_node is not None:
            visited.add(next_node)
            path.append(next_node)
            total_cost += min_cost
            current_node = next_node

    return path, total_cost


        
        
def run(city,importance_time_visit,importance_beauty,importance_edge,start_node=0,n_days=0):
    if n_days == 0:
        n_days = random.randint(3,6)
    try:
        df = pd.read_csv("dataset/city/"+city.lower()+".csv")
        beauty = df['ranking'].tolist()  # For simplicity, we assume "ranking" is beauty
        duration = df['duration(h)'].tolist()  # Duration of visit in hours
        beauty_normalized = normalize(beauty)
        latitudes = df['lat'].tolist()
        longitudes = df['long'].tolist()
        n = len(df)
        global cost_matrix
        cost_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i != j:  # Skip distance to itself
                    cost_matrix[i][j] = get_geo.get_distance(latitudes[i],longitudes[i], latitudes[j], longitudes[j])
                else:
                    cost_matrix[i][j] = 0

        cost_matrix = np.array(cost_matrix) / walking_speed_kmh
        G = nx.DiGraph()
        for i in range(n):
            G.add_node(i, beauty=beauty_normalized[i], time_to_visit=duration[i])
        for i in range(n):
            for j in range(n):
                if i != j:
                    # Calcola il costo per l'arco (i, j)
                    costo = calculate_edge_cost(G, i, j, importance_beauty, importance_time_visit, importance_edge)
                    #print(i,j,costo)
                    costo_A_B = cost_matrix[i][j]
                    G.add_edge(i, j, weight=costo, costo=costo_A_B)


        path, total_cost = path_min_tsp(G, start_node)
        total_time = calculate_total_time(G, path)
        places_to_visit, total_time_spent = get_best_k_places(path, G, n_days)
        place_names = df['place'].tolist() 
        #rint(f"Path min from -> {start_node}: {path}")
        #print(f"Total time to visit (sum of time to visit + edge cost): {total_time} hours")
        return places_to_visit,place_names,total_time_spent
        #print(f"Best places to visit (names): {[place_names[i] for i in places_to_visit]}")
        #print(f"Total time spent: {total_time_spent} hours")
    except:
        return [],[],0
    


'''
This script creates a graph representation of places to visit, where each node corresponds to a place,
and edges represent the distance (in kilometers) between those places. The nodes are associated with 
two attributes: "beauty" (a measure of the place's aesthetic value) and "time to visit" (the amount 
of time required to explore the place). The goal is to calculate the most efficient route for visiting 
these places based on a weighted combination of these attributes and travel distances.

The edge weights are calculated considering both the distance between places and the relative importance 
of the "beauty" and "time to visit" of each place. This script allows you to compute:
1. The shortest path for visiting the places, considering both the beauty of each place and travel costs.
2. The total time required for the visit, considering both time spent at each place and travel times between them.
3. The best subset of places to visit within a given number of days (with each day having a fixed number of hours available for visiting).

In particular, the edge cost represents the time (in hours) it takes to walk between two places based 
on the distance in kilometers, assuming a walking speed of 5 km/h. The script then calculates the total 
time spent visiting the places, and ensures that the total visit time stays within the available hours for the specified days.

Key steps in the script:
- Normalize the "beauty" attribute to a range [0, 1].
- Calculate a weighted cost for each edge considering the beauty, time to visit, and distance.
- Use a greedy approach to find the minimum cost path for visiting the places (Traveling Salesman Problem - TSP).
- Calculate the total time spent (sum of time to visit and travel times) and determine which places can be visited 
  within the available time for a given number of days.

The script is designed for use cases where you want to plan an optimal route for visiting multiple places, 
minimizing travel time and considering the time each place requires to explore.
'''

import networkx as nx
import numpy as np


# Function to normalize a list or array to the range [0, 1]
def normalize(values):
    min_val = min(values)
    max_val = max(values)
    return [(x - min_val) / (max_val - min_val) for x in values]

# Function to calculate the total cost considering the importance factors
def get_total_cost(peso1_A, peso2_A, costo_A_B, importanza1, importanza2, importanza3):
    # 1 - peso1_A because higher beauty (peso1) is better, while higher time and edge cost are worse
    return (importanza1 * (1 - peso1_A)) + (importanza2 * peso2_A) + (importanza3 * costo_A_B)

# Function to calculate total time spent based on sum of time to visit (peso2) and edge cost (costo_A_B)
def calculate_total_time(G, path):
    total_time = 0
    for i in range(len(path) - 1):
        current_node = path[i]
        next_node = path[i + 1]
        
        # Add the time to visit (peso2) and the edge cost (costo_A_B)
        peso2_A = G.nodes[current_node]['peso2']
        edge_cost = G[current_node][next_node]['weight']
        
        # Sum of time to visit and the time (cost) for the edge
        total_time += peso2_A + edge_cost

    return total_time



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
        peso2_A = G.nodes[current_node]['peso2']
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
    if total_time_spent + G.nodes[path[-1]]['peso2'] <= available_time:
        places_to_visit.append(path[-1])
    
    return places_to_visit, total_time_spent



# Walking speed in km/h (you can adjust this value if necessary)
walking_speed_kmh = 5

# Normalizing w1 (beauty) to [0, 1]
w1 = [5, 3, 7, 2, 9, 4, 8, 6, 1, 10]
w1 = normalize(w1)

w2 = [4, 8, 1, 6, 3, 7, 5, 9, 2, 10]
# Normalizing the cost matrix
cost_matrix = [
    [0, 3, 5, 2, 6, 4, 7, 8, 9, 2],
    [3, 0, 4, 1, 5, 2, 6, 7, 8, 3],
    [5, 4, 0, 3, 2, 5, 6, 4, 5, 7],
    [2, 1, 3, 0, 4, 3, 5, 6, 7, 2],
    [6, 5, 2, 4, 0, 3, 7, 5, 6, 4],
    [4, 2, 5, 3, 3, 0, 6, 8, 5, 7],
    [7, 6, 6, 5, 7, 6, 0, 4, 5, 6],
    [8, 7, 4, 6, 5, 8, 4, 0, 3, 5],
    [9, 8, 5, 7, 6, 5, 5, 3, 0, 6],
    [2, 3, 7, 2, 4, 7, 6, 5, 6, 0]
]


# Convert the cost matrix from km to time in hours
cost_matrix = np.array(cost_matrix) / walking_speed_kmh




# Create a directed graph
n = 10  
G = nx.DiGraph()  

# Importance
importance_time_visit = 0.2  
importance_beauty     = 0.5  
importance_edge       = 0.3 

# Add nodes to the graph with their respective normalized weights
for i in range(n):
    peso1_nodo = w1[i]  
    peso2_nodo = w2[i]  
    G.add_node(i, peso1=peso1_nodo, peso2=peso2_nodo)

# Add edges to the graph with the total calculated costs
for i in range(n):
    for j in range(n):
        if i != j: 
            peso1_A = G.nodes[i]['peso1']
            peso2_A = G.nodes[i]['peso2']
            costo_A_B = cost_matrix[i][j]
            costo = get_total_cost(peso1_A, peso2_A, costo_A_B, importance_time_visit, importance_beauty, importance_edge)
            G.add_edge(i, j, weight=costo, costo=costo_A_B)

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




# Set the start node and calculate the minimum path and total cost
start_node = 0
path, total_cost = path_min_tsp(G, start_node)
# Calculate the total time spent based on time to visit (peso2) and edge cost
total_time = calculate_total_time(G, path)
n_days = 2  # Assume 2 days available for visiting
places_to_visit, total_time_spent = get_best_k_places(path, G, n_days)


# Print the result
print(f"Path min from -> {start_node}: {path}")
print(f"Total time to visit (sum of time to visit + edge cost): {total_time} hours")
print(f"Best places to visit: {places_to_visit}")
print(f"Total time spent: {total_time_spent} hours")
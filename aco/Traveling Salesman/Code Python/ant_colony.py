import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


#-----------------------------------------
def compute_cost(colony_size, distance_matrix, tour, el):
    reference = np.zeros(colony_size)
    for i in range(colony_size):  # For each ant
        dist = 0
        for j in range(52):
            dist += distance_matrix[tour[i, j], tour[i, j+1]]
        reference[i] = dist
    cost = reference.copy()
    reference -= el * np.min(reference)  # eliminates repeating distances
    return cost, reference
#---------------------------------------
def update_tau(colony_size, tau, tour, reference, evap_coeff, Q):
    """
    SUMMARY: The idea here is that we update the pheromones. We take into
    consideration the evaporation coefficient.
    Here, we're using Ant-Quantity AS variation. In this case, only local information, d_{ij}, is used to update pheromone 
    concentrations. Lower cost links are made more desirable. If d_{ij} represents the distance between links, then ant-quantity AS 
    prefers selection of the shortest links.
    """
    for i in range(colony_size):  # For each ant...
        for j in range(52):  # ... we update certain values of tau depending on the tour table
            delta_tau = Q / reference[i]  # This is an Ant-Quantity AS
            tau[tour[i, j], tour[i, j+1]] = (1 - evap_coeff) * tau[tour[i, j], tour[i, j+1]] + delta_tau
    return tau
#-------------------------------------------
def ant_tour_construction(start_places, colony_size, a_priori, tau, alpha, beta):
    """
    SUMMARY: This function completes the ant tour matrix for one iteration.
    For each ant in the colony, we make them traverse the whole map (tour). 
    They first start at a randomly generated starting area (start_places), 
    and jump to each node. The jumps are controlled by the attractiveness 
    of the node raised to beta, and the pheromone effect raised to alpha.
    """
    for i in range(colony_size):  # For each ant...
        a_priori_temp = np.copy(a_priori)  # ... we track its sight// sight is what it saw, or what cities it saw.
        for j in range(51):  # We then have it move around the 51 cities (not 52 because 1 is already starting point).
            c = start_places[i, j]  # We track its place and put it into c.
            a_priori_temp[:, c] = 0
            temp = (tau[c, :] ** alpha) * (a_priori_temp[c, :] ** beta)
            s = np.sum(temp)
            p = (1 / s) * temp
            r = np.random.rand()  # rand just generates from 0 to 1.
            s = 0
            for k in range(52):
                s += p[k]
                if r <= s:
                    start_places[i, j + 1] = k
                    break
    new_places = start_places
    return new_places
#-----------------------------


# =================== Part 0: Setup parameters =====================================
iterations = 500           # Number of iterations
colony_size = 60           # Number of ants
evap_coeff = 0.1           # Evaporation coefficient

alpha = 15                 # Greediness factor
beta = 20                  # Importance of trail

tau = 0.0001 * np.ones((52, 52))  # Initial pheromone levels

el = 0.97                  # Cost elimination parameter
Q = 0.2                    # Pheromone update constant

# =================== Part 0.1: Load berlin52 dataset from csv file ===================
os.chdir('D:\\Work\\N4\\TUH\\Report2\\TH2')
berlin52 = pd.read_csv('berlin52.csv')
x = berlin52.iloc[:, 0]
y = berlin52.iloc[:, 1]

# =================== Part 0.2: Plot berlin52 dataset ==================================
plt.figure()
plt.subplot(2, 2, 1)
mycolor = [0.93, 0.273, 0.191]
plt.scatter(x, y, c=[mycolor], edgecolors='k', s=5)
plt.title('Plot of Berlin52 Dataset')
plt.xlabel('x  (km)')
plt.ylabel('y  (km)')
plt.axis('square')

# =================== Part 1: Initialize parameters ====================================
distance_matrix = np.zeros((52, 52))
for i in range(52):
    for j in range(52):
        distance_matrix[i, j] = np.sqrt((x[i] - x[j])**2 + (y[i] - y[j])**2)

a_priori = np.zeros((52, 52))
for i in range(52):
    for j in range(52):
        if distance_matrix[i, j] == 0:
            a_priori[i, j] = 0
        else:
            a_priori[i, j] = 1 / distance_matrix[i, j]

# =================== Part 2: Ant System Algorithm ====================================
min_cost = np.zeros(iterations)
besttour = np.zeros((iterations, 53))
iteration = np.zeros(iterations)
mean_cost = np.zeros(iterations)
a = np.zeros(iterations)

for i in range(iterations):
    start_places = np.random.randint(0, 52, size=(colony_size, 1))
    tour, cost, reference, tau = ant_tour_construction(start_places, colony_size, a_priori, tau, alpha, beta, distance_matrix, el, Q)
    average_cost = np.mean(cost)
    min_cost[i], best_index = np.min(cost), np.argmin(cost)
    besttour[i, :] = np.hstack((tour[best_index], tour[best_index][0]))
    iteration[i] = i
    mean_cost[i] = np.mean(cost)
    a[i] = np.min(min_cost)

    # =================== Part 3: Plot results ============================================
    plt.subplot(2, 2, 3)
    plt.plot(iteration, a)
    plt.title('Tour vs Iterations')
    plt.xlabel('Iterations')
    plt.ylabel('Tour')
    plt.axis('square')

    plt.subplot(2, 2, 4)
    plt.plot(iteration, mean_cost)
    plt.title('Ant Behaviour')
    plt.xlabel('Iterations')
    plt.ylabel('Tour')
    plt.axis('square')

    k, l = np.min(min_cost), np.argmin(min_cost)
    X = x[besttour[l].astype(int)]
    Y = y[besttour[l].astype(int)]
    plt.subplot(2, 2, 2)
    plt.plot(X, Y, '--ko', markeredgecolor='k', markerfacecolor=[1, 1, 0], markersize=5)
    plt.grid(True)
    plt.xlabel('x (km)')
    plt.ylabel('y (km)')
    plt.title(f'Cost = {k}')
    plt.axis('square')

    plt.pause(0.1)
    plt.draw()



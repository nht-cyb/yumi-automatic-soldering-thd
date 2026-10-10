import util
import aco
import graphs
import pandas as pd

####################
# Loading Coordinates # Berlin 52 (Minimum Distance = 7544.3659)
coordinates = pd.read_csv('D:/Work/N4/TUH/ACOpy/data/berlin.txt', sep = '\t')
coordinates = coordinates.values

# Obtaining the Distance Matrix
distance_matrix = util.build_distance_matrix(coordinates)

# ACO - Parameters
parameters = {
              'ants': 60,
              'iterations': 500,
              'alpha':15,
              'beta':20,
              'decay':0.1,
              'local_search': True,
              'verbose': True
             }

# ACO - Algorithm
route, distance = aco.ant_colony_optimization(distance_matrix, **parameters)

# Plot Locations and Tour
graphs.plot_tour(coordinates, city_tour = route, view = 'notebook', size = 10)
print('Total Distance: ', round(distance, 6))

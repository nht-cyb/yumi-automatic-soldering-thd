import numpy as np
import matplotlib.pyplot as plt
import os

# Function to read coordinates from a text file
def read_coordinates(file_path):
    x_coords = []
    y_coords = []
    z_coords = []

    with open(file_path, 'r') as file:
        for line in file:
            # Split the line into components
            parts = line.strip().split(', ')
            x = float(parts[0].split(': ')[1])
            y = float(parts[1].split(': ')[1])
            z = float(parts[2].split(': ')[1])

            # Append the coordinates to the lists
            x_coords.append(x)
            y_coords.append(y)
            z_coords.append(z)

    return np.array(x_coords), np.array(y_coords), np.array(z_coords)

# Path to your coordinates text file
folder = 'visualize data'
#filename = '1110_data_no_station.txt'
#filename = 'extracted_1710_g.txt'
#filename = 'extracted_1710_y.txt'
#filename = '2210_data_BQ.txt'
#filename = '2310_data_begin_end_points.txt'
#filename = '2310_new_station.txt'
filename = 'visualize data/2310_outer_grid.txt'
file_path = os.path.join(folder, filename)

# Read coordinates from the file
x, y, z = read_coordinates(file_path)

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Scatter plot
ax.scatter(x, y, z, c='b', marker='o')

# Label axes
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

# Set title
ax.set_title('3D Scatter Plot of Coordinates of ')

# Show the plot
plt.show()
import re
import os

# Step 1: Read the .txt file
input_folder = 'input'
output_folder = 'visualize data'
filename = '2310_outer_grid.txt'

output_file_path = os.path.join(output_folder, filename)
input_file_path = os.path.join(input_folder, filename)

# Step 2: Initialize an empty list to hold the x, y, z coordinates
coordinates = []

# Step 3: Open and read the file line by line
with open(input_file_path, 'r') as file:
    for line in file:
        # Step 4: Use regex to match and extract the x, y, z values within the first set of brackets
        match = re.search(r'\[\s*([-.\d]+),\s*([-.\d]+),\s*([-.\d]+)\s*\]', line)
        if match:
            # Step 5: Convert the matched groups to floats and append them to the list
            x, y, z = map(float, match.groups())
            coordinates.append([x, y, z])

# Step 6: Save the coordinates to a new .txt file
with open(output_file_path, 'w') as output_file:
    for coord in coordinates:
        # Writing each set of coordinates in a readable format: "X: value, Y: value, Z: value"
        output_file.write(f'X: {coord[0]}, Y: {coord[1]}, Z: {coord[2]}\n')

print(f"Coordinates extracted and saved to {output_file_path}")

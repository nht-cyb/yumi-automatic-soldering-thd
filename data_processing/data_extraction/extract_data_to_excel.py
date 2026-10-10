import re
import os
import pandas as pd

# Step 1: Read the .txt file
input_folder = 'input'
output_folder = 'output'
filename = '1110_data_no_station.txt'

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

# Step 6: Convert the coordinates to a DataFrame and save to Excel
df = pd.DataFrame(coordinates, columns=['X', 'Y', 'Z'])

# Save to Excel file
df.to_excel(output_file_path, index=False)

print(f"Coordinates extracted and saved to {output_file_path}")
import re
import os
import pandas as pd

# Function to extract x, y, z coordinates from a file
def extract_coordinates(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r'\[\s*([-.\d]+),\s*([-.\d]+),\s*([-.\d]+)\s*\]', line)
            if match:
                x, y, z = map(float, match.groups())
                coordinates.append([x, y, z])
    return coordinates

# List of files to extract data from
#files =['1110_data_no_station.txt', '1710_data_g.txt', '1710_data_y.txt']  # Replace with your actual file paths
input_folder = 'input'
output_excel_file = 'output\extracted_coordinates.xlsx'

# Step 1: Use ExcelWriter to create an Excel file with multiple sheets
with pd.ExcelWriter(output_excel_file, engine='xlsxwriter') as writer:
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(input_folder, filename)
        # Extract the coordinates from each file
            coordinates = extract_coordinates(file_path)
        
        # Convert the coordinates to a DataFrame
            df = pd.DataFrame(coordinates, columns=['X', 'Y', 'Z'])
        
        # Get the name of the file (without the extension) for the sheet name
            sheet_name = filename.split('.')[0]
        
        # Write the DataFrame to a new sheet in the Excel file
            df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Data extracted and saved to {output_excel_file}")
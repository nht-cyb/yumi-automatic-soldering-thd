# oke this is passable, take points in the input to put it in row and column
import math
import os

# Example file paths
# Define your input and output file paths
input_file_path = "clickdata/clicked_positions.txt"       # change input here
output_dir = "converted_output/"

def calculate_row_col(x, y, ref_x, ref_y, spacing, tolerance):
    """
    Maps a point (x, y) to the nearest row and column on the grid.
    - ref_x, ref_y: Reference point for Column 1, Row 1.
    - spacing: Distance between rows and columns.
    - tolerance: Allowed deviation in pixels.
    """
    # Calculate theoretical row and column (may be floating-point)
    theoretical_col = (x - ref_x) / spacing + 1
    theoretical_row = (y - ref_y) / spacing + 1

    # Round to nearest integer row and column
    col = round(theoretical_col)
    row = round(theoretical_row)

    # Calculate the theoretical position of the mapped point
    mapped_x = ref_x + (col - 1) * spacing
    mapped_y = ref_y + (row - 1) * spacing

    # Validate within tolerance
    if abs(mapped_x - x) > tolerance or abs(mapped_y - y) > tolerance:
        return None  # Point does not match any valid grid position
    return row, col

def process_points(input_file, output_file, ref_x, ref_y, spacing, tolerance):
    """
    Reads points from an input file, maps them to grid rows and columns,
    removes duplicates, and writes the results to an output file.
    """
    with open(input_file, 'r') as f:
        points = f.readlines()

    mapped_positions = set()  # Use a set to avoid duplicates
    for line in points:
        try:
            x, y = map(float, line.strip().split())
            mapped_position = calculate_row_col(x, y, ref_x, ref_y, spacing, tolerance)
            if mapped_position:
                mapped_positions.add(mapped_position)  # Add only unique positions
        except ValueError:
            pass  # Skip invalid lines

    # Write unique results to the output file in the format "row column"
    with open(output_file, 'w') as f:
        for row, col in sorted(mapped_positions):  # Sort for consistent order
            f.write(f"{row} {col}\n")

    return mapped_positions

# Parameters
reference_x = 44  # X of Column 1, Row 1 5x7
reference_y = 24  # Y of Column 1, Row 1 6x8
grid_spacing = 20.4  # Spacing between rows and columns
tolerance = 5  # Tolerance in pixels for matching

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

input_filename = os.path.basename(input_file_path)

# Create a new output filename by joining input filename with the output directory
output_file_path = os.path.join(output_dir, f"{os.path.splitext(input_filename)[0]}_converted.txt")

# Check if the file already exists, if so, modify the name to avoid overwriting
counter = 1
while os.path.exists(output_file_path):
    output_file_path = os.path.join(output_dir, f"{os.path.splitext(input_filename)[0]}_output_{counter}.txt")
    counter += 1

# Process the points
processed_results = process_points(input_file_path, output_file_path, reference_x, reference_y, grid_spacing, tolerance)

# Show first few results as confirmation
print(list(processed_results)[:5])

import os

PROC_NAME = "MoveUpDown"  # RAPID routine called at each joint

def point_name(row, col):
    # Row 1..18 -> letter A..R, column 1..24 -> number, e.g. (1, 2) -> A2
    if not 1 <= row <= 26 or col < 1:
        raise ValueError
    return f"{chr(ord('A') + row - 1)}{col}"

def generate_commands(file_path):
    commands = []
    try:
        # Open the file and process line by line
        with open(file_path, 'r') as file:
            for line in file:
                # Split the line into row and column values
                values = line.strip().split()
                if len(values) != 2:
                    print(f"Skipping invalid line: {line.strip()}")
                    continue

                try:
                    row = int(values[0])
                    col = int(values[1])

                    # Create the command string
                    command = f"{PROC_NAME} {point_name(row, col)};"
                    commands.append(command)
                except ValueError:
                    print(f"Skipping invalid data: {line.strip()}")

        return commands

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

def save_commands(commands, output_folder):
    try:
        # Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, 'commands.txt')

        # Write commands to the file
        with open(output_file, 'w') as file:
            for command in commands:
                file.write(command + '\n')

        print(f"Commands saved to '{output_file}'")
    except Exception as e:
        print(f"Error saving commands: {e}")

# Example usage
if __name__ == "__main__":
    input_file = "converted_output/clicked_positions_converted.txt"  # Replace with your file path
    output_folder = "command"  # Folder to save the commands
    result = generate_commands(input_file)
    if result:
        save_commands(result, output_folder)

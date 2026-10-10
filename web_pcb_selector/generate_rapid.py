import os
import re

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
                    continue

                try:
                    row = int(values[0])
                    col = int(values[1])

                    # Create the command string
                    command = f"{PROC_NAME} {point_name(row, col)};"
                    commands.append(command)
                except ValueError:
                    continue

        return commands

    except FileNotFoundError:
        return []

def save_commands(commands, output_folder, input_file):
    try:
        # Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_folder, f"{base_name}_commands.txt")

        # Write commands to the file
        with open(output_file, 'w') as file:
            for command in commands:
                file.write(command + '\n')

    except Exception as e:
        pass

def declared_name(line):
    # Name of the robtarget/jointtarget declared on this line, or None
    match = re.search(r'\b(?:robtarget|jointtarget)\s+(\w+)\s*:=', line)
    return match.group(1) if match else None

def insert_robtargets(dataset_file, module_file, output_file):
    try:
        # Read robtarget definitions from dataset.txt
        with open(dataset_file, 'r') as dataset:
            robtargets = dataset.readlines()

        # Read the module file
        with open(module_file, 'r') as module:
            lines = module.readlines()

        # Keep only the definitions the module does not already declare
        existing = {declared_name(line) for line in lines}
        robtargets = [r for r in robtargets if declared_name(r) and declared_name(r) not in existing]

        # Create a new file for the updated module
        with open(output_file, 'w') as module:
            inserted = False
            for line in lines:
                # Data declarations must sit inside the module, before the first routine
                if not inserted and line.strip().startswith("PROC "):
                    for robtarget in robtargets:
                        module.write(robtarget)
                    if robtargets:
                        module.write('\n')  # Add a blank line after robtargets
                    inserted = True
                module.write(line)

    except FileNotFoundError:
        pass
    except Exception as e:
        pass

def replace_main_commands(module_file, commands, output_file):
    try:
        with open(module_file, 'r') as file:
            lines = file.readlines()

        with open(output_file, 'w') as file:
            inside_main = False
            for line in lines:
                if line.strip().startswith("PROC main()"):
                    inside_main = True
                    file.write(line)
                elif inside_main and line.strip() == "ENDPROC":
                    for command in commands:
                        file.write(f"        {command}\n")
                    inside_main = False
                    file.write(line)
                elif not inside_main or not line.strip().startswith(PROC_NAME):
                    # Calls already in main() are replaced by the selected joints
                    file.write(line)

    except FileNotFoundError:
        pass
    except Exception as e:
        pass

# Example usage
if __name__ == "__main__":
    input_file = "converted_output/clicked_positions_converted.txt"  # Replace with your file path
    dataset_file = "program/inputgp/2310_outer_grid.txt"  # File containing robtarget definitions
    module_file = "program/inputgp/calibrateXYZ_for_shifted_station.txt"  # Module file to update
    output_folder = "program"  # Folder to save the commands and outputs

    result = generate_commands(input_file)
    if result:
        save_commands(result, output_folder, input_file)

        base_name = os.path.splitext(os.path.basename(input_file))[0]
        updated_module_file = os.path.join(output_folder, f"{base_name}_module.txt")

        insert_robtargets(dataset_file, module_file, updated_module_file)
        replace_main_commands(updated_module_file, result, updated_module_file)

        # Report selected joints that have no robtarget in the generated module
        with open(updated_module_file, 'r') as module:
            declared = {declared_name(line) for line in module}
        missing = [c.split()[1].rstrip(';') for c in result if c.split()[1].rstrip(';') not in declared]
        if missing:
            print(f"Warning: no robtarget declared for {', '.join(missing)}. Add them to '{dataset_file}'.")

import os

def generate_commands(file_path):
    commands = []
    try:
        # Open the file and process line by line
        with open(file_path, 'r') as file:
            for line in file:
                # Split the line into x and y values
                values = line.strip().split()
                if len(values) != 2:
                    continue

                try:
                    x = int(values[0])
                    y = int(values[1])

                    # Format x and y with leading zeros if necessary
                    x_formatted = f"{x:02d}"
                    y_formatted = f"{y:02d}"

                    # Create the command string
                    command = f"FuncName P{x_formatted}{y_formatted};"
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

def insert_robtargets(dataset_file, module_file, output_file):
    try:
        # Read robtarget definitions from dataset.txt
        with open(dataset_file, 'r') as dataset:
            robtargets = dataset.readlines()

        # Read the module file
        with open(module_file, 'r') as module:
            lines = module.readlines()

        # Create a new file for the updated module
        with open(output_file, 'w') as module:
            for robtarget in robtargets:
                module.write(robtarget)
            module.write('\n')  # Add a blank line after robtargets
            for line in lines:
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
                        file.write(f"    {command}\n")
                    inside_main = False
                    file.write(line)
                elif not inside_main or not line.strip().startswith("FuncName"):
                    file.write(line)

    except FileNotFoundError:
        pass
    except Exception as e:
        pass

# Example usage
if __name__ == "__main__":
    input_file = "converted_output/clicked_positions_converted.txt.txt"  # Replace with your file path
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

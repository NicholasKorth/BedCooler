import os
import re

# --- Configuration ---
# 1. The filename of your KiCad PCB file.
PCB_FILENAME = "BedCooler.kicad_pcb" 

# 2. The name of the folder inside your project where you've stored all the 3D models.
#    (This should match the folder you created in Step 1).
SHAPES_FOLDER_NAME = "3dshapes"
# --- End of Configuration ---


def fix_kicad_pcb_paths(input_filename, shapes_folder):
    """
    Reads a KiCad PCB file, fixes the 3D model paths to be relative,
    and writes the output to a new file.
    """
    if not os.path.exists(input_filename):
        print(f"--- ERROR ---")
        print(f"The file '{input_filename}' was not found in this directory.")
        print("Please check the 'PCB_FILENAME' variable in this script and run it again.")
        return

    # Create a name for the new, corrected output file
    base, ext = os.path.splitext(input_filename)
    output_filename = f"{base}_fixed{ext}"

    print(f"Reading from: {input_filename}")
    print(f"Writing to:   {output_filename}")

    # This regular expression robustly finds the path inside a (model ...) block
    path_regex = re.compile(r'\(path "([^"]+)"\)')
    lines_changed = 0

    with open(input_filename, 'r', encoding='utf-8') as infile, \
         open(output_filename, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            # Check if the line contains a model path
            match = path_regex.search(line)
            if match:
                old_path = match.group(1)
                
                # Extract just the filename from the old path, handling both / and \
                filename = os.path.basename(old_path.replace('\\', '/'))

                # Construct the new, correct relative path using the KIPRJMOD variable
                new_path = f"${{KIPRJMOD}}/{shapes_folder}/{filename}"

                # Replace the old path string with the new one
                new_line = line.replace(old_path, new_path)
                outfile.write(new_line)
                
                if new_line != line:
                    lines_changed += 1
            else:
                # If the line doesn't contain a path, write it out unchanged
                outfile.write(line)

    print(f"\n✅ Success! Processed the file and fixed {lines_changed} model paths.")
    print(f"Open '{output_filename}' in KiCad to verify the 3D models are now correct.")


if __name__ == "__main__":
    fix_kicad_pcb_paths(PCB_FILENAME, SHAPES_FOLDER_NAME)
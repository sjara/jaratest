import sys, os
# Get the directory of the current script
current_script_directory = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory to the sys.path
parent_directory = os.path.abspath(os.path.join(current_script_directory, os.pardir))
sys.path.append(parent_directory)
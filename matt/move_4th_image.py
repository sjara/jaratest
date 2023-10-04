import re
import pathlib as pl
import subprocess

file_pattern = "low_freq_*.tif"

source_path = input("path to images: ")
dest_path = input("path to move images to: ")

# TODO: Could add in an input for the modulo number if we want divisors
#  other than 4

source_folder = pl.Path(source_path)
dest_folder = pl.Path(dest_path)

for file in source_folder.glob(file_pattern):
    num_string = file.name.split("_")[-1][0:5]
    num = int(num_string)
    if num % 4 == 0:
        dest = str(dest_folder) + "/" + file.name
        # Test print statement to verify var names are assigned correctly
        print(f"moving {file.name} to {dest}")

        # dry run of the rsync command, RUN FIRST TO VERIFY
        # subprocess.call(["rsync", "-avP", "--dry-run", f"{file}",
        #                  f"{dest}"])

        # Actual rsync that will copy files. RUN ABOVE TEST FIRST
        # subprocess.call(["rsync", "-avP", f"{file}", f"{dest}"])

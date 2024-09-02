import shutil
import os

# Define the source directory (the current output directory)
source_dir = os.path.join(os.getcwd(), "_site")
print(source_dir)

# Define the destination directory (one level up in the GitHub folder)
destination_dir = os.path.abspath(os.path.join(os.getcwd(), "../../Blog"))
print(destination_dir)

# # Remove the destination directory if it exists and copy the contents
if os.path.exists(destination_dir):
    shutil.rmtree(destination_dir)

shutil.copytree(source_dir, destination_dir)

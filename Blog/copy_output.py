import shutil
import os

# Define the source directory (the current output directory)
source_dir = os.path.join(os.getcwd(), "_site")
print(source_dir)

# Define the destination directory (level up in the GitHub folder)
destination_dir = os.path.abspath(os.path.join(os.getcwd(), "../../Blog"))
print(destination_dir)

# Ensure the destination directory exists
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Copy the contents of the source directory to the destination directory
for item in os.listdir(source_dir):
    source_item = os.path.join(source_dir, item)
    destination_item = os.path.join(destination_dir, item)
    
    if os.path.isdir(source_item):
        # If the item is a directory, copy it recursively
        shutil.copytree(source_item, destination_item, dirs_exist_ok=True)
    else:
        # If the item is a file, copy it
        shutil.copy2(source_item, destination_item)

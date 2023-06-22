import shutil
from pathlib import Path

# Define the path to the folder containing subfolders
folder_path = Path(r'D:\Downloads\Music')

# Loop through all subfolders
for subfolder in folder_path.iterdir():
    if subfolder.is_dir():
        # Delete empty folders
        if not any(subfolder.iterdir()):
            subfolder.rmdir()
        else:
            # Loop through all files in the current subfolder
            for file in subfolder.iterdir():
                # Define the paths for the current file
                src_path = file
                dst_path = folder_path / file.name
                # Move the file to the parent folder
                if src_path.is_file():
                    shutil.move(str(src_path), str(dst_path))
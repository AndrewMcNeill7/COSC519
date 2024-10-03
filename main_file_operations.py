import os
import shutil

def create_folder(directory):
    folder_name = "NewFolder"
    folder_path = os.path.join(directory, folder_name)
    os.makedirs(folder_path, exist_ok=True)  # Creates the folder if it doesn't exist
    return folder_path

def create_file(directory):
    file_name = "example.txt"
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'w') as f:
        f.write("This is an example file created inside the new folder.")
    return file_path

def copy_file(src, dst):
    shutil.copy(src, dst)

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def rename_file(old_name, new_name):
    os.rename(old_name, new_name)

def move_file(src, dst):
    import shutil
    shutil.move(src, dst)

def make_folder(folder_path):
    os.makedirs(folder_path, exist_ok=True)

def remove_folder(folder_path):
    import shutil
    shutil.rmtree(folder_path)

def list_files(directory):
    return os.listdir(directory)

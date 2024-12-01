# as of 11.12.23 all functions are implemented.
# to do:
import os
import shutil
import time
import fnmatch

# Function to create a folder


def create_folder(directory, folder_name="NewFolder"):
    folder_path = os.path.join(directory, folder_name)
    # Creates the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

# Function to create a file with a dynamic name


def create_file(directory, file_name="example.txt"):
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'w') as f:
        f.write("This is an example file created inside the new folder.")
    return file_path

# Function to copy a file


def copy_file(src, dst):
    try:
        shutil.copy(src, dst)
        print(f"File copied from {src} to {dst}")
    except Exception as e:
        print(f"Error copying file: {e}")
        raise

# Function to delete a file


def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File {file_path} deleted")
        else:
            print(f"File {file_path} does not exist")
    except Exception as e:
        print(f"Error deleting file: {e}")
        raise

# Function to rename a file


def rename_file(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        print(f"File renamed from {old_name} to {new_name}")
    except Exception as e:
        print(f"Error renaming file: {e}")
        raise

# Function to move a file


def move_file(src, dst):
    try:
        shutil.move(src, dst)
        print(f"File moved from {src} to {dst}")
    except Exception as e:
        print(f"Error moving file: {e}")
        raise

# Function to remove a folder


def remove_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        print(f"Folder {folder_path} removed")
    except Exception as e:
        print(f"Error removing folder: {e}")
        raise

# Function to list files in a directory


def list_files(directory):
    try:
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except Exception as e:
        print(f"Error listing files: {e}")
        raise

# Advanced file operations


class FileManager:
    def __init__(self, directory):
        self.directory = directory
        self.file_tags = {}

    # Method to search files by attributes
    def search_by_attributes(self, file_type=None, min_size=None, max_size=None, created_after=None, modified_after=None):
        results = []
        for dirpath, _, filenames in os.walk(self.directory):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                file_info = os.stat(file_path)
                file_size = file_info.st_size
                creation_time = time.ctime(file_info.st_ctime)
                modification_time = time.ctime(file_info.st_mtime)

                # Check file type
                if file_type and not fnmatch.fnmatch(filename, f'*.{file_type}'):
                    continue
                # Check file size
                if (min_size and file_size < min_size) or (max_size and file_size > max_size):
                    continue
                # Check creation date
                if created_after and time.mktime(time.strptime(creation_time)) < created_after:
                    continue
                # Check modification date
                if modified_after and time.mktime(time.strptime(modification_time)) < modified_after:
                    continue

                results.append({
                    'path': file_path,
                    'size': file_size,
                    'created': creation_time,
                    'modified': modification_time
                })
        return results

    # Method to search for specific text within files
    def search_within_files(self, search_text):
        results = []
        for dirpath, _, filenames in os.walk(self.directory):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                if filename.endswith(('.txt', '.csv')):
                    try:
                        with open(file_path, 'r', errors='ignore') as file:
                            contents = file.read()
                            if search_text in contents:
                                results.append(file_path)
                    except Exception as e:
                        print(f"Error reading file {file_path}: {e}")
        return results

    # Method to tag files with keywords
    def tag_file(self, file_path, tags):
        if file_path in self.file_tags:
            self.file_tags[file_path].update(tags)
        else:
            self.file_tags[file_path] = set(tags)

    # Method to search for files by tags
    def search_by_tags(self, tags):
        results = []
        for file_path, file_tags in self.file_tags.items():
            if file_tags.intersection(tags):
                results.append(file_path)
        return results

    def populate_tree(self, path):
        # Populate the tree with directories
        self.tree.delete(*self.tree.get_children())
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                self.tree.insert('', 'end', text=item, values=(full_path,))
                node = self.tree.insert(
                    '', 'end', text=item, values=(full_path,))
                self.populate_subtree(node, full_path)

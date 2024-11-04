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

# Advanced file operations:
class FileManager:
    def __init__(self, directory):
        self.directory = directory
        self.file_tags = {}

    def search_by_attributes(self, file_type=None, min_size=None, max_size=None,
                             created_after=None, modified_after=None):
        results = []
        for dirpath, dirnames, filenames in os.walk(self.directory):
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

    def search_within_files(self, search_text):
        results = []
        for dirpath, dirnames, filenames in os.walk(self.directory):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                if filename.endswith(('.txt', '.csv')):
                    with open(file_path, 'r', errors='ignore') as file:
                        contents = file.read()
                        if search_text in contents:
                            results.append(file_path)
        return results

    def tag_file(self, file_path, tags):
        if file_path in self.file_tags:
            self.file_tags[file_path].update(tags)
        else:
            self.file_tags[file_path] = set(tags)

    def search_by_tags(self, tags):
        results = []
        for file_path, file_tags in self.file_tags.items():
            if file_tags.intersection(tags):
                results.append(file_path)
        return results

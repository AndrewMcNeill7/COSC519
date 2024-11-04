from tkinter import *
from tkinter import filedialog, messagebox, simpledialog
import os
import main_file_operations  
import time

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


# Initialize FileManager
directory = os.path.join(os.path.expanduser("~"), "Documents", "my_file_manager")
file_manager = FileManager(directory)

def select_directory():
    return filedialog.askdirectory(title="Select Directory")

def create_folder_gui():
    folder_path = main_file_operations.create_folder(file_manager.directory)
    messagebox.showinfo("Folder Created", f"Folder created at {folder_path}")

def create_file_gui():
    file_path = main_file_operations.create_file(file_manager.directory)
    messagebox.showinfo("File Created", f"File created at {file_path}")

def copy_file_gui():
    src = filedialog.askopenfilename(title="Select File to Copy")
    dst = filedialog.askdirectory(title="Select Destination Folder")
    if src and dst:
        main_file_operations.copy_file(src, os.path.join(dst, os.path.basename(src)))
        messagebox.showinfo("File Copied", "The file has been copied successfully.")

def delete_file_gui():
    file_path = filedialog.askopenfilename(title="Select File to Delete")
    if file_path:
        main_file_operations.delete_file(file_path)
        messagebox.showinfo("File Deleted", "The file has been deleted successfully.")

def rename_file_gui():
    old_name = filedialog.askopenfilename(title="Select File to Rename")
    if old_name:
        new_name = simpledialog.askstring("New File Name", "Enter new file name:")
        if new_name:
            main_file_operations.rename_file(old_name, os.path.join(os.path.dirname(old_name), new_name))
            messagebox.showinfo("File Renamed", "The file has been renamed successfully.")

def move_file_gui():
    src = filedialog.askopenfilename(title="Select File to Move")
    dst = filedialog.askdirectory(title="Select Destination Folder")
    if src and dst:
        main_file_operations.move_file(src, dst)
        messagebox.showinfo("File Moved", "The file has been moved successfully.")

def list_files_gui():
    files = main_file_operations.list_files(file_manager.directory)
    messagebox.showinfo("Files in Directory", "\n".join(files))

def search_by_attributes_gui():
    file_type = simpledialog.askstring("File Type", "Enter file type (e.g., txt, csv):")
    min_size = simpledialog.askinteger("Minimum Size", "Enter minimum file size in bytes:")
    max_size = simpledialog.askinteger("Maximum Size", "Enter maximum file size in bytes:")
    created_after = simpledialog.askstring("Created After", "Enter creation date (YYYY-MM-DD):")
    modified_after = simpledialog.askstring("Modified After", "Enter modification date (YYYY-MM-DD):")

    # Convert dates to timestamps
    if created_after:
        created_after = time.mktime(time.strptime(created_after, "%Y-%m-%d"))
    if modified_after:
        modified_after = time.mktime(time.strptime(modified_after, "%Y-%m-%d"))

    results = file_manager.search_by_attributes(file_type, min_size, max_size, created_after, modified_after)
    messagebox.showinfo("Search Results", "\n".join([file['path'] for file in results]))

def search_within_files_gui():
    search_text = simpledialog.askstring("Search Text", "Enter text to search within files:")
    results = file_manager.search_within_files(search_text)
    messagebox.showinfo("Search Results", "\n".join(results))

def tag_file_gui():
    file_path = filedialog.askopenfilename(title="Select File to Tag")
    if file_path:
        tags = simpledialog.askstring("Tags", "Enter tags separated by commas:")
        if tags:
            tag_list = {tag.strip() for tag in tags.split(',')}
            file_manager.tag_file(file_path, tag_list)
            messagebox.showinfo("Success", "Tags added successfully.")

def search_by_tags_gui():
    tags = simpledialog.askstring("Tags", "Enter tags to search for (separated by commas):")
    if tags:
        tag_list = {tag.strip() for tag in tags.split(',')}
        results = file_manager.search_by_tags(tag_list)
        messagebox.showinfo("Search Results", "\n".join(results))


# Create the main window
root = Tk()
root.title("File Manager")
root.geometry("400x600")

# Create buttons for each file operation
Button(root, text="Create Folder", command=create_folder_gui).pack(pady=10)
Button(root, text="Create File", command=create_file_gui).pack(pady=10)
Button(root, text="Copy File", command=copy_file_gui).pack(pady=10)
Button(root, text="Delete File", command=delete_file_gui).pack(pady=10)
Button(root, text="Rename File", command=rename_file_gui).pack(pady=10)
Button(root, text="Move File", command=move_file_gui).pack(pady=10)
Button(root, text="List Files", command=list_files_gui).pack(pady=10)

# Add buttons for advanced search features
Button(root, text="Search by Attributes", command=search_by_attributes_gui).pack(pady=10)
Button(root, text="Search Within Files", command=search_within_files_gui).pack(pady=10)
Button(root, text="Tag File", command=tag_file_gui).pack(pady=10)
Button(root, text="Search by Tags", command=search_by_tags_gui).pack(pady=10)

# Run the main event loop
root.mainloop()

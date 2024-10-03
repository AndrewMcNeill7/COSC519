from tkinter import *
from tkinter import filedialog, messagebox
import file_operations  # Import the file operations module

def select_directory():
    return filedialog.askdirectory(title="Select Directory")

def create_folder_gui():
    directory = select_directory()
    if directory:
        folder_path = file_operations.create_folder(directory)
        messagebox.showinfo("Success", f"Folder created at: {folder_path}")

def create_file_gui():
    directory = select_directory()
    if directory:
        file_path = file_operations.create_file(directory)
        messagebox.showinfo("Success", f"File created at: {file_path}")

def copy_file_gui():
    src = filedialog.askopenfilename(title="Select File to Copy")
    if src:
        dst = filedialog.askdirectory(title="Select Destination Directory")
        if dst:
            file_operations.copy_file(src, os.path.join(dst, os.path.basename(src)))
            messagebox.showinfo("Success", "File copied successfully.")

def delete_file_gui():
    file_path = filedialog.askopenfilename(title="Select File to Delete")
    if file_path:
        file_operations.delete_file(file_path)
        messagebox.showinfo("Success", "File deleted successfully.")

def rename_file_gui():
    old_name = filedialog.askopenfilename(title="Select File to Rename")
    if old_name:
        new_name = simpledialog.askstring("Rename File", "Enter new name:")
        if new_name:
            file_operations.rename_file(old_name, os.path.join(os.path.dirname(old_name), new_name))
            messagebox.showinfo("Success", "File renamed successfully.")

def move_file_gui():
    src = filedialog.askopenfilename(title="Select File to Move")
    if src:
        dst = filedialog.askdirectory(title="Select Destination Directory")
        if dst:
            file_operations.move_file(src, os.path.join(dst, os.path.basename(src)))
            messagebox.showinfo("Success", "File moved successfully.")

def list_files_gui():
    directory = select_directory()
    if directory:
        files = file_operations.list_files(directory)
        messagebox.showinfo("Files in Directory", "\n".join(files))

# Create the main window
root = Tk()
root.title("File Manager")
root.geometry("400x400")

# Create buttons for each file operation
Button(root, text="Create Folder", command=create_folder_gui).pack(pady=10)
Button(root, text="Create File", command=create_file_gui).pack(pady=10)
Button(root, text="Copy File", command=copy_file_gui).pack(pady=10)
Button(root, text="Delete File", command=delete_file_gui).pack(pady=10)
Button(root, text="Rename File", command=rename_file_gui).pack(pady=10)
Button(root, text="Move File", command=move_file_gui).pack(pady=10)
Button(root, text="List Files", command=list_files_gui).pack(pady=10)

# Run the main event loop
root.mainloop()

import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import subprocess

class FileExplorer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("File Explorer")
        self.geometry("800x600")

        # Keep track of the current directory
        self.current_directory = os.path.expanduser("~")
        self.previous_directories = []

        # Create a paned window
        self.paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Create the directory tree
        self.tree_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.tree_frame)

        # Set the initial width of the tree_frame
        self.tree_frame.pack_propagate(False)
        self.tree_frame.config(width=250)

        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Add a scrollbar for the tree view
        tree_scroll = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Create the file list
        self.file_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.file_frame, weight=1)

        self.file_list = ttk.Treeview(self.file_frame, columns=("Name", "Size"), show="headings")
        self.file_list.heading("Name", text="File Name", anchor=tk.W)
        self.file_list.heading("Size", text="Size (KB)", anchor=tk.W)
        self.file_list.pack(fill=tk.BOTH, expand=True)

        # Add a scrollbar for the file list
        file_scroll = ttk.Scrollbar(self.file_frame, orient="vertical", command=self.file_list.yview)
        self.file_list.configure(yscrollcommand=file_scroll.set)
        file_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a toolbar with buttons
        self.toolbar = ttk.Frame(self)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.refresh_button = ttk.Button(self.toolbar, text="Refresh", command=self.refresh_file_list)
        self.refresh_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.new_folder_button = ttk.Button(self.toolbar, text="New Folder", command=self.create_new_folder)
        self.new_folder_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.new_file_button = ttk.Button(self.toolbar, text="New Text File", command=self.create_text_file)
        self.new_file_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.move_file_button = ttk.Button(self.toolbar, text="Move File", command=self.move_file)
        self.move_file_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Populate the tree with the root directory
        self.populate_tree(self.current_directory)

        # Bind selection events
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Double-1>", self.on_tree_expand)
        self.file_list.bind("<Double-1>", self.on_file_double_click)

    def populate_tree(self, path, parent=""):
        """Populate the tree with directories and files in the given path."""
        try:
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    # Insert directories
                    self.tree.insert(parent, 'end', text=item, values=(full_path,))
                elif os.path.isfile(full_path):
                    # Insert files directly
                    self.tree.insert(parent, 'end', text=item, values=(full_path,))
        except PermissionError:
            messagebox.showwarning("Access Denied", f"Cannot access directory: {path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_tree_expand(self, event):
        """Load directories when a node is expanded."""
        selected_item = self.tree.focus()
        path = self.tree.item(selected_item, "values")[0]

        # Check if the item already has children before populating
        if not self.tree.get_children(selected_item):
            self.populate_tree(path, selected_item)

    def on_tree_select(self, event):
        """Update the file list when a directory is selected."""
        selected_item = self.tree.focus()
        selected_path = self.tree.item(selected_item, "values")[0]
        self.previous_directories.append(self.current_directory)  # Save current directory
        self.current_directory = selected_path
        self.update_file_list(selected_path)

    def on_file_double_click(self, event):
        """Open the selected file on double click."""
        selected_item = self.file_list.focus()
        file_name = self.file_list.item(selected_item, "values")[0]
        file_path = os.path.join(self.current_directory, file_name)

        if os.path.isfile(file_path):
            if file_name.lower().endswith('.txt'):
                subprocess.run(['notepad', file_path])  # Open text files with Notepad
            else:
                os.startfile(file_path)  # Open with default application

    def update_file_list(self, directory):
        """Update the file list based on the selected directory."""
        self.file_list.delete(*self.file_list.get_children())
        try:
            for file_name in os.listdir(directory):
                file_path = os.path.join(directory, file_name)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path) // 1024  # Size in KB
                    self.file_list.insert("", "end", values=(file_name, size))
        except PermissionError:
            messagebox.showwarning("Access Denied", f"Cannot access directory: {directory}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_file_list(self):
        """Refresh the file list in the current directory."""
        self.update_file_list(self.current_directory)

    def create_new_folder(self):
        """Create a new folder in the current directory."""
        folder_name = simpledialog.askstring("New Folder", "Enter folder name:")
        if folder_name:
            new_folder_path = os.path.join(self.current_directory, folder_name)
            try:
                os.makedirs(new_folder_path)
                self.refresh_file_list()  # Refresh to show the new folder
            except FileExistsError:
                messagebox.showwarning("Warning", "Folder already exists.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def create_text_file(self):
        """Create a new text file in the current directory."""
        file_name = simpledialog.askstring("New Text File", "Enter file name (without .txt):")
        if file_name:
            file_name = f"{file_name}.txt"
            new_file_path = os.path.join(self.current_directory, file_name)
            try:
                with open(new_file_path, 'w') as new_file:
                    new_file.write("")  # Create an empty text file
                self.refresh_file_list()  # Refresh to show the new file
            except FileExistsError:
                messagebox.showwarning("Warning", "File already exists.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def move_file(self):
        """Move the selected file to a new directory."""
        selected_item = self.file_list.focus()
        if not selected_item:
            messagebox.showwarning("Select File", "Please select a file to move.")
            return

        file_name = self.file_list.item(selected_item, "values")[0]
        file_path = os.path.join(self.current_directory, file_name)

        # Prompt user for target directory
        target_directory = filedialog.askdirectory(title="Select Target Directory")
        if not target_directory:
            return  # User canceled the dialog

        target_file_path = os.path.join(target_directory, file_name)

        try:
            os.rename(file_path, target_file_path)  # Move the file
            self.refresh_file_list()  # Refresh the file list
            messagebox.showinfo("Success", f"File moved to {target_directory}")
        except FileNotFoundError:
            messagebox.showwarning("Error", "File not found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = FileExplorer()
    app.mainloop()
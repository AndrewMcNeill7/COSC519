#as of 11.12.23 all functions are implemented. 
#to do: 

import os
from tkinter import *
from tkinter import simpledialog, messagebox
from tkinter import ttk
import shutil  # For moving files
import file_operations  # Assuming file operations are handled as you described

class FileExplorer(Tk):
    def __init__(self):
        super().__init__()

        self.title("File Manager")
        self.geometry("1000x700")  # Larger window size for a cleaner look
        self.configure(bg='#F5F5F5')  # Lighter background color for a polished look

        # Set the icon for the window (optional)
        # self.iconbitmap('your_icon.ico')  # Optional: Use your own app icon

        # Main paned window with two panes
        self.paned_window = PanedWindow(self, orient=HORIZONTAL)
        self.paned_window.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Directory Tree (left pane)
        self.tree_frame = Frame(self.paned_window, bg='#F5F5F5')
        self.tree = ttk.Treeview(self.tree_frame, selectmode="browse", style="Custom.Treeview")
        self.tree.pack(fill=BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Scrollbar for tree view
        tree_scroll = Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        tree_scroll.pack(side=RIGHT, fill=Y)

        self.paned_window.add(self.tree_frame, width=250)

        # File List (right pane)
        self.file_frame = Frame(self.paned_window, bg='#F5F5F5')
        self.file_list = ttk.Treeview(self.file_frame, columns=("Name", "Size"), show="headings", selectmode="extended", style="Custom.Treeview")
        self.file_list.heading("Name", text="Name", anchor=W)
        self.file_list.heading("Size", text="Size (KB)", anchor=W)
        self.file_list.pack(fill=BOTH, expand=True)
        self.file_list.bind("<Double-1>", self.on_file_select)  # Bind double-click event

        # Scrollbar for file list
        file_scroll = Scrollbar(self.file_frame, orient="vertical", command=self.file_list.yview)
        self.file_list.configure(yscrollcommand=file_scroll.set)
        file_scroll.pack(side=RIGHT, fill=Y)

        self.paned_window.add(self.file_frame, width=650)

        # Add a frame for the search bar and button
        self.search_frame = Frame(self, bg='#F5F5F5')
        self.search_frame.pack(fill=X, pady=10)

        self.search_label = Label(self.search_frame, text="Search Files:")
        self.search_label.pack(side=LEFT, padx=5)

        self.search_entry = Entry(self.search_frame, width=40)
        self.search_entry.pack(side=LEFT, padx=5)

        self.search_button = Button(self.search_frame, text="Search", command=self.search_files)
        self.search_button.pack(side=LEFT, padx=5)

        # Populate the directory tree with initial nodes, starting from the home directory
        self.populate_tree(path=os.path.expanduser("~"))

        # Button frame at the bottom
        self.button_frame = Frame(self, bg='#F5F5F5')
        self.button_frame.pack(fill=X, pady=10)

        self.create_buttons()

        # Styling for Treeview and Button Widgets
        self.style = ttk.Style()
        self.style.configure("Custom.Treeview",
                             background="#EAEAEA",
                             foreground="black",
                             rowheight=25,
                             fieldbackground="#F5F5F5",
                             font=("Helvetica", 10))
        self.style.configure("Custom.Treeview.Heading", font=("Helvetica", 12, 'bold'))

        self.style.configure("TButton",
                             font=("Helvetica", 10),
                             padding=6,
                             relief="flat",
                             background="#f0f0f0",
                             foreground="#333333")
        self.style.map("TButton", background=[('active', '#45a049')])

    def create_buttons(self):
        # Use ttk.Button for styling
        ttk.Button(self.button_frame, text="Create Folder", command=self.create_folder_gui).pack(side=LEFT, padx=10)
        ttk.Button(self.button_frame, text="Create File", command=self.create_file_gui).pack(side=LEFT, padx=10)
        ttk.Button(self.button_frame, text="Move Files", command=self.batch_move_files_gui).pack(side=LEFT, padx=10)
        ttk.Button(self.button_frame, text="Delete Files", command=self.batch_delete_files_gui).pack(side=LEFT, padx=10)
        ttk.Button(self.button_frame, text="List Files", command=self.list_files_gui).pack(side=LEFT, padx=10)
        ttk.Button(self.button_frame, text="Rename File", command=self.rename_file_gui).pack(side=LEFT, padx=10)
        ttk.Button(self.button_frame, text="Remove Folder", command=self.remove_folder_gui).pack(side=LEFT, padx=10)
        ttk.Button(self.button_frame, text="Search by Attributes", command=self.search_by_attributes_gui).pack(side=LEFT, padx=10)
        ttk.Button(self.button_frame, text="Search within Files", command=self.search_within_files_gui).pack(side=LEFT, padx=10)
        ttk.Button(self.button_frame, text="Tag File", command=self.tag_file_gui).pack(side=LEFT, padx=10)
        ttk.Button(self.button_frame, text="Search by Tags", command=self.search_by_tags_gui).pack(side=LEFT, padx=10)

    def populate_tree(self, parent="", path=os.path.expanduser("~")):
        """Populate the directory tree with folders, starting from the user's home directory."""
        try:
            for folder in os.listdir(path):
                full_path = os.path.join(path, folder)
                if os.path.isdir(full_path):
                    node = self.tree.insert(parent, "end", text=folder, open=False)
                    self.populate_tree(node, full_path)
        except PermissionError:
            pass

    def on_tree_select(self, event):
        """Handler for directory selection in the tree view."""
        selected_item = self.tree.focus()
        selected_path = self.get_full_path(selected_item)

        if os.path.exists(selected_path) and os.path.isdir(selected_path):
            self.update_file_list(selected_path)

    def get_full_path(self, item):
        """Get the full path of the selected item in the tree view."""
        path = []
        while item:
            path.insert(0, self.tree.item(item, "text"))
            item = self.tree.parent(item)
        return os.path.join(os.path.expanduser("~"), *path)
    
    def rename_file_gui(self):
        selected_item = self.file_list.selection()
        if not selected_item:
            messagebox.showwarning("No file selected", "Please select a file to rename.")
            return

        old_file_name = self.file_list.item(selected_item, "values")[0]
        current_directory = self.get_full_path(self.tree.focus())
        old_file_path = os.path.join(current_directory, old_file_name)

        new_file_name = simpledialog.askstring("Rename File", "Enter the new file name:")
        if new_file_name:
            try:
                new_file_path = os.path.join(current_directory, new_file_name)
                file_operations.rename_file(old_file_path, new_file_path)
                messagebox.showinfo("Success", f"File renamed to {new_file_name}")
                self.update_file_list(current_directory)
            except Exception as e:
                messagebox.showerror("Error", f"Could not rename file: {e}")

    def remove_folder_gui(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("No folder selected", "Please select a folder to remove.")
            return

        folder_path = self.get_full_path(selected_item)
        confirm = messagebox.askyesno("Confirm Remove", f"Are you sure you want to remove the folder: {folder_path}?")
        if confirm:
            try:
                file_operations.remove_folder(folder_path)
                messagebox.showinfo("Success", f"Folder {folder_path} removed")
                self.populate_tree()  # Refresh the tree
            except Exception as e:
                messagebox.showerror("Error", f"Could not remove folder: {e}")

    def search_by_attributes_gui(self):
        directory = self.get_full_path(self.tree.focus())
        file_type = simpledialog.askstring("File Type", "Enter the file type (e.g., txt, csv):")
        min_size = simpledialog.askinteger("Min Size (bytes)", "Enter the minimum file size (in bytes):")
        max_size = simpledialog.askinteger("Max Size (bytes)", "Enter the maximum file size (in bytes):")

        results = file_operations.FileManager(directory).search_by_attributes(
        file_type=file_type, min_size=min_size, max_size=max_size
    )
        if results:
            result_text = "\n".join([f"Path: {r['path']} | Size: {r['size']} bytes" for r in results])
            messagebox.showinfo("Search Results", f"Found files:\n{result_text}")
        else:
            messagebox.showinfo("No Results", "No files matching your criteria were found.")

    def search_within_files_gui(self):
        directory = self.get_full_path(self.tree.focus())
        search_text = simpledialog.askstring("Search Text", "Enter the text to search within files:")

        if search_text:
            results = file_operations.FileManager(directory).search_within_files(search_text)
            if results:
                result_text = "\n".join(results)
                messagebox.showinfo("Search Results", f"Found in:\n{result_text}")
        else:
                messagebox.showinfo("No Results", "No files containing the specified text were found.")

    def tag_file_gui(self):
        selected_item = self.file_list.selection()
        if not selected_item:
            messagebox.showwarning("No file selected", "Please select a file to tag.")
            return

        file_name = self.file_list.item(selected_item, "values")[0]
        current_directory = self.get_full_path(self.tree.focus())
        file_path = os.path.join(current_directory, file_name)

        tags = simpledialog.askstring("Tags", "Enter tags separated by commas:")
        if tags:
            tags_list = [tag.strip() for tag in tags.split(',')]
            file_operations.FileManager(current_directory).tag_file(file_path, tags_list)
            messagebox.showinfo("Success", f"Tags added to {file_name}")

    def search_by_tags_gui(self):
        directory = self.get_full_path(self.tree.focus())
        tags = simpledialog.askstring("Tags", "Enter tags separated by commas:")

        if tags:
            tags_list = set(tag.strip() for tag in tags.split(','))
            results = file_operations.FileManager(directory).search_by_tags(tags_list)
            if results:
                result_text = "\n".join(results)
                messagebox.showinfo("Search Results", f"Files with tags:\n{result_text}")
            else:
                messagebox.showinfo("No Results", "No files with matching tags were found.")




    def update_file_list(self, directory):
        """Update the file list based on the selected directory."""
        for item in self.file_list.get_children():
            self.file_list.delete(item)

        try:
            for file_name in os.listdir(directory):
                file_path = os.path.join(directory, file_name)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path) // 1024  # Size in KB
                    self.file_list.insert("", "end", values=(file_name, size))
        except PermissionError:
            messagebox.showwarning("Access Denied", f"Cannot access directory: {directory}")

    def on_file_select(self, event):
        """Handler for file selection in the file list (double-click event)."""
        selected_item = self.file_list.focus()
        file_name = self.file_list.item(selected_item, "values")[0]
        current_directory = self.get_full_path(self.tree.focus())
        file_path = os.path.join(current_directory, file_name)

        if os.path.isfile(file_path):
            messagebox.showinfo("File Selected", f"You selected the file: {file_name}")
            # Add additional actions for opening or editing the file here

    def create_folder_gui(self):
        directory = self.get_full_path(self.tree.focus())  # Get the selected directory path
        folder_name = simpledialog.askstring("Folder Name", "Enter the folder name:")
        if folder_name:
            folder_path = file_operations.create_folder(directory, folder_name)
            messagebox.showinfo("Success", f"Folder created at: {folder_path}")
            self.update_file_list(directory)  # Update the file list to show the new folder

    def create_file_gui(self):
        directory = self.get_full_path(self.tree.focus())  # Get the selected directory path
        file_name = simpledialog.askstring("File Name", "Enter the file name (without extension):")
        if file_name:
            file_extension = simpledialog.askstring("File Extension", "Enter the file extension (e.g., .txt):")
            if file_extension:
                file_path = file_operations.create_file(directory, file_name, file_extension)
                messagebox.showinfo("Success", f"File created at: {file_path}")
                self.update_file_list(directory)  # Update the file list to show the new file

    def batch_move_files_gui(self):
        """Handle batch file moving."""
        # Get selected files in the file list
        selected_items = self.file_list.selection()
        if not selected_items:
            messagebox.showwarning("No files selected", "Please select files to move.")
            return
        
        # Get destination folder from user
        destination = simpledialog.askstring("Destination", "Enter the destination directory:")
        if destination:
            for item in selected_items:
                file_name = self.file_list.item(item, "values")[0]
                current_directory = self.get_full_path(self.tree.focus())
                src_path = os.path.join(current_directory, file_name)
                try:
                    file_operations.move_file(src_path, destination)
                except Exception as e:
                    messagebox.showerror("Error", f"Could not move file: {e}")
            
            messagebox.showinfo("Success", f"Files moved to {destination}")
            self.update_file_list(current_directory)  # Update the file list

    def batch_delete_files_gui(self):
        """Handle batch file deletion."""
        selected_items = self.file_list.selection()
        if not selected_items:
            messagebox.showwarning("No files selected", "Please select files to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected files?")
        if confirm:
            for item in selected_items:
                file_name = self.file_list.item(item, "values")[0]
                current_directory = self.get_full_path(self.tree.focus())
                file_path = os.path.join(current_directory, file_name)
                try:
                    file_operations.delete_file(file_path)
                except Exception as e:
                    messagebox.showerror("Error", f"Could not delete file: {e}")
            
            messagebox.showinfo("Success", "Selected files have been deleted.")
            self.update_file_list(current_directory)  # Update the file list

    def list_files_gui(self):
        """List all files in the current directory."""
        selected_item = self.tree.focus()
        current_directory = self.get_full_path(selected_item)
        self.update_file_list(current_directory)

    def search_files(self):
        """Search files based on the search entry."""
        search_query = self.search_entry.get().lower()
        if not search_query:
            messagebox.showwarning("No Query", "Please enter a search query.")
            return

        found_files = []
        selected_item = self.tree.focus()
        current_directory = self.get_full_path(selected_item)

        for file_name in os.listdir(current_directory):
            if search_query in file_name.lower():
                found_files.append(file_name)

        if found_files:
            messagebox.showinfo("Search Results", f"Found files: {', '.join(found_files)}")
        else:
            messagebox.showinfo("No Results", "No files matching your query were found.")

if __name__ == "__main__":
    app = FileExplorer()
    app.mainloop()

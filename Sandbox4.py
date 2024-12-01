import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import subprocess
import zipfile
import datetime 

class FileExplorer(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure styles
        self.style = ttk.Style()
        self.style.configure("Custom.Treeview",
                             background="#EAEAEA",
                             foreground="black",
                             rowheight=25,
                             fieldbackground="#F5F5F5",
                             font=("Helvetica", 10))
        self.style.configure("Custom.Treeview.Heading",
                             font=("Helvetica", 12, 'bold'))

        self.style.configure("TButton",
                             font=("Helvetica", 10),
                             padding=6,
                             relief="flat",
                             background="#f0f0f0",
                             foreground="#333333")
        self.style.map("TButton", background=[('active', '#45a049')])

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

        self.tree = ttk.Treeview(self.tree_frame, style="Custom.Treeview")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Add a scrollbar for the tree view
        tree_scroll = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Create the file list
        self.file_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.file_frame, weight=1)

        self.file_list = ttk.Treeview(self.file_frame, columns=("Name", "Size", "Last Modified"), show="headings", style="Custom.Treeview")
        self.file_list.heading("Name", text="File Name", anchor=tk.W)
        self.file_list.heading("Size", text="Size (KB)", anchor=tk.W)
        self.file_list.heading("Last Modified", text="Last Modified", anchor=tk.W)
        self.file_list.pack(fill=tk.BOTH, expand=True)

        # Add a scrollbar for the file list
        file_scroll = ttk.Scrollbar(self.file_frame, orient="vertical", command=self.file_list.yview)
        self.file_list.configure(yscrollcommand=file_scroll.set)
        file_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a toolbar with buttons
        self.toolbar = ttk.Frame(self)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Search Entry
        self.search_entry = ttk.Entry(self.toolbar, font=("Helvetica", 10), width=15)  # Further reduced width and font size
        self.search_entry.grid(row=0, column=0, padx=5, pady=5, columnspan=2, sticky="ew")

        # Define button properties
        button_properties = [
            ("Refresh", self.refresh_file_list),
            ("New Folder", self.create_new_folder),
            ("New Text File", self.create_text_file),
            ("Rename File", self.rename_file_gui),
            ("Move File", self.move_file_gui),
            ("Remove Folder", self.remove_folder_gui),
            ("Delete File", self.delete_file_gui),
            ("Compress File", self.compress_file_gui),
            ("Decompress File", self.decompress_file_gui),
            ("Search", self.search_files),
        ]

        # Create buttons in two columns
        for index, (text, command) in enumerate(button_properties):
            button = ttk.Button(self.toolbar, text=text, command=command, style="TButton")
            column = index % 2  # Determine column (0 or 1)
            row = index // 2    # Determine row
            button.grid(row=row + 1, column=column, padx=5, pady=5, sticky="ew")

        # Configure grid columns to expand
        self.toolbar.columnconfigure(0, weight=1)
        self.toolbar.columnconfigure(1, weight=1)

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
                    self.tree.insert(parent, 'end', text=item, values=(full_path,))
                elif os.path.isfile(full_path):
                    self.tree.insert(parent, 'end', text=item, values=(full_path,))
        except PermissionError:
            messagebox.showwarning("Access Denied", f"Cannot access directory: {path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_tree_expand(self, event):
        """Load directories when a node is expanded."""
        selected_item = self.tree.focus()
        path = self.tree.item(selected_item, "values")[0]
        if not self.tree.get_children(selected_item):
            self.populate_tree(path, selected_item)

    def on_tree_select(self, event):
        """Update the file list when a directory is selected."""
        selected_item = self.tree.focus()
        selected_path = self.tree.item(selected_item, "values")[0]
        self.previous_directories.append(self.current_directory)
        self.current_directory = selected_path
        self.update_file_list(selected_path)

    def on_file_double_click(self, event):
        """Open the selected file on double click."""
        selected_item = self.file_list.focus()
        file_name = self.file_list.item(selected_item, "values")[0]
        file_path = os.path.join(self.current_directory, file_name)

        if os.path.isfile(file_path):
            if file_name.lower().endswith('.txt'):
                subprocess.run(['notepad', file_path])
            else:
                os.startfile(file_path)

    def update_file_list(self, directory):
        """Update the file list based on the selected directory."""
        self.file_list.delete(*self.file_list.get_children())
        try:
            for file_name in os.listdir(directory):
                file_path = os.path.join(directory, file_name)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path) // 1024  # Size in KB
                    mod_time = os.path.getmtime(file_path)
                    mod_date = datetime.datetime.fromtimestamp(mod_time).strftime("%m-%d-%Y %I:%M %p")  # 12-hour format
                    self.file_list.insert("", "end", values=(file_name, size, mod_date))  # Insert file info
        except PermissionError:
            messagebox.showwarning("Access Denied", f"Cannot access directory: {directory}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def search_files(self, event=None):
        """Search files by name, extension, or last modified date in the current directory."""
        search_term = self.search_entry.get().lower()
        self.file_list.delete(*self.file_list.get_children())
        
        try:
            # Attempt to parse the date if the search term is in the correct format
            search_date = None
            if len(search_term) == 10:  # mm-dd-yyyy format
                try:
                    search_date = datetime.datetime.strptime(search_term, "%m-%d-%Y").date()
                except ValueError:
                    search_date = None  # Invalid date format

            for file_name in os.listdir(self.current_directory):
                file_path = os.path.join(self.current_directory, file_name)
                is_file = os.path.isfile(file_path)

                if is_file:
                    # Get file modification date
                    mod_time = os.path.getmtime(file_path)
                    mod_date = datetime.datetime.fromtimestamp(mod_time).date()

                    # Check if the search term is in the file name or if it matches the file extension
                    matches_name_or_extension = (search_term in file_name.lower() or
                                                (search_term.startswith('.') and file_name.lower().endswith(search_term)))

                    # If a search date was provided, check if it matches the modification date
                    if (matches_name_or_extension or search_date) and (search_date is None or mod_date == search_date):
                        size = os.path.getsize(file_path) // 1024  # Size in KB
                        mod_date_str = datetime.datetime.fromtimestamp(mod_time).strftime("%m-%d-%Y %I:%M %p")  # 12-hour format
                        self.file_list.insert("", "end", values=(file_name, size, mod_date_str))  # Insert file info

        except PermissionError:
            messagebox.showwarning("Access Denied", f"Cannot access directory: {self.current_directory}")
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
                self.refresh_file_list()
                messagebox.showinfo("Success", f"Folder '{folder_name}' created successfully.")
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
                    new_file.write("")
                self.refresh_file_list()
            except FileExistsError:
                messagebox.showwarning("Warning", "File already exists.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def move_file_gui(self):
        """Move selected file(s) to a target directory."""
        selected_items = self.file_list.selection()
        if not selected_items:
            move_all = messagebox.askyesno("Move Files", "No files selected. Do you want to move all files?")
            if move_all:
                selected_items = self.file_list.get_children()
            else:
                messagebox.showwarning("No files selected", "Please select files to move.")
                return

        target_directory = filedialog.askdirectory(title="Select Target Directory")
        if not target_directory:
            return

        moved_items = []
        for selected_item in selected_items:
            file_name = self.file_list.item(selected_item, "values")[0]
            source_path = os.path.join(self.current_directory, file_name)
            destination_path = os.path.join(target_directory, file_name)

            try:
                os.rename(source_path, destination_path)
                moved_items.append(file_name)
                self.file_list.delete(selected_item)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to move file '{file_name}': {str(e)}")
                return

        if moved_items:
            success_message = f"Moved {len(moved_items)} file(s):\n" + \
                              "\n".join(moved_items) + \
                              f"\nTo directory: {target_directory}"
            messagebox.showinfo("Move Successful", success_message)

        self.refresh_file_list()

    def delete_file_gui(self):
        """Delete selected file(s) after confirmation."""
        selected_items = self.file_list.selection()
        if not selected_items:
            messagebox.showwarning("No files selected", "Please select files to delete.")
            return

        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected file(s)?"):
            deleted_items = []

            for selected_item in selected_items:
                file_name = self.file_list.item(selected_item, "values")[0]
                file_path = os.path.join(self.current_directory, file_name)

                try:
                    os.remove(file_path)
                    deleted_items.append(file_name)
                    self.file_list.delete(selected_item)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete file '{file_name}': {str(e)}")
                    return

            if deleted_items:
                success_message = f"Deleted {len(deleted_items)} file(s):\n" + \
                                  "\n".join(deleted_items)
                messagebox.showinfo("Deletion Successful", success_message)

    def rename_file_gui(self):
        """Rename selected file(s) after confirmation."""
        selected_items = self.file_list.selection()
        if not selected_items:
            messagebox.showwarning("No files selected", "Please select a file to rename.")
            return

        selected_item = selected_items[0]
        current_file_name = self.file_list.item(selected_item, "values")[0]
        new_file_name = simpledialog.askstring("Rename File", "Enter new file name:", initialvalue=current_file_name)
        if new_file_name:
            if new_file_name != current_file_name:
                new_file_path = os.path.join(self.current_directory, new_file_name)
                if os.path.exists(new_file_path):
                    messagebox.showwarning("Warning", "A file with that name already exists.")
                    return

                old_file_path = os.path.join(self.current_directory, current_file_name)
                try:
                    os.rename(old_file_path, new_file_path)
                    self.refresh_file_list()
                    messagebox.showinfo("Rename Successful", f"File renamed to '{new_file_name}'")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to rename file: {str(e)}")

    def remove_folder_gui(self):
        """Remove selected folder after confirmation."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("No folder selected", "Please select a folder to remove.")
            return

        folder_path = self.tree.item(selected_item, "values")[0]
        if messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove the folder '{os.path.basename(folder_path)}'?"):
            try:
                os.rmdir(folder_path)
                self.tree.delete(selected_item)
                self.refresh_file_list()
                messagebox.showinfo("Removal Successful", f"Folder '{os.path.basename(folder_path)}' removed successfully.")
            except OSError as e:
                messagebox.showerror("Error", f"Failed to remove folder: {str(e)}")

    def compress_file_gui(self):
        """Compress selected file(s) into a ZIP archive."""
        selected_items = self.file_list.selection()
        if not selected_items:
            messagebox.showwarning("No files selected", "Please select files to compress.")
            return

        # Prompt for the name of the zip file
        zip_file_name = simpledialog.askstring("Compress Files", "Enter name for the zip file (without .zip):")
        if zip_file_name:
            zip_file_path = os.path.join(self.current_directory, f"{zip_file_name}.zip")
            try:
                with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                    for selected_item in selected_items:
                        file_name = self.file_list.item(selected_item, "values")[0]
                        file_path = os.path.join(self.current_directory, file_name)
                        zipf.write(file_path, arcname=file_name)  # Add file to the ZIP
                messagebox.showinfo("Compression Successful", f"Files compressed into '{zip_file_path}'")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to compress files: {str(e)}")

    def decompress_file_gui(self):
        """Decompress a selected ZIP file."""
        zip_file_path = filedialog.askopenfilename(title="Select ZIP File", filetypes=[("ZIP files", "*.zip")])
        if not zip_file_path:
            return

        try:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(self.current_directory)
            messagebox.showinfo("Decompression Successful", f"Files extracted to '{self.current_directory}'")
            self.refresh_file_list()  # Refresh the file list to show the new files
        except zipfile.BadZipFile:
            messagebox.showerror("Error", "The selected file is not a valid ZIP file.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decompress files: {str(e)}")

if __name__ == "__main__":
    app = FileExplorer()
    app.mainloop()
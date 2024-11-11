from tkinter import *
from tkinter import filedialog, messagebox, simpledialog
import main_file_operations
import os
import subprocess
import zipfile

# Tooltip class to show button descriptions
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip = Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.attributes('-alpha', 0.9)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = Label(self.tooltip, text=self.text, background="#333333",
                      foreground="white", borderwidth=1, relief="solid")
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()

# Functionality for file operations
def select_directory():
    return filedialog.askdirectory(title="Select Directory")

def create_folder_gui():
    directory = select_directory()
    if directory:
        folder_path = main_file_operations.create_folder(directory)
        messagebox.showinfo("Success", f"Folder created at: {folder_path}")

def create_file_gui():
    directory = select_directory()
    if directory:
        file_path = main_file_operations.create_file(directory)
        messagebox.showinfo("Success", f"File created at: {file_path}")

def copy_file_gui():
    src = filedialog.askopenfilename(title="Select File to Copy")
    if src:
        dst = filedialog.askdirectory(title="Select Destination Directory")
        if dst:
            main_file_operations.copy_file(src, os.path.join(dst, os.path.basename(src)))
            messagebox.showinfo("Success", "File copied successfully.")

def delete_file_gui():
    file_path = filedialog.askopenfilename(title="Select File to Delete")
    if file_path:
        main_file_operations.delete_file(file_path)
        messagebox.showinfo("Success", "File deleted successfully.")

def rename_file_gui():
    old_name = filedialog.askopenfilename(title="Select File to Rename")
    if old_name:
        new_name = simpledialog.askstring("Rename File", "Enter new name:")
        if new_name:
            main_file_operations.rename_file(old_name, os.path.join(os.path.dirname(old_name), new_name))
            messagebox.showinfo("Success", "File renamed successfully.")

def move_file_gui():
    src = filedialog.askopenfilename(title="Select File to Move")
    if src:
        dst = filedialog.askdirectory(title="Select Destination Directory")
        if dst:
            main_file_operations.move_file(src, os.path.join(dst, os.path.basename(src)))
            messagebox.showinfo("Success", "File moved successfully.")

def list_files_gui():
    directory = select_directory()
    if directory:
        files = main_file_operations.list_files(directory)

        for widget in search_results_frame.winfo_children():
            widget.destroy()

        search_results_frame.pack_forget()
        search_results_frame.pack(fill='both', padx=20, pady=10)

        if files:
            Label(search_results_frame, text="Files in Directory:", font=("Helvetica", 12), bg="#333333", fg="white").pack(anchor="w")
            for file in files:
                file_label = Label(search_results_frame, text=file, font=("Helvetica", 10), bg="#333333", fg="white", anchor="w", cursor="hand2")
                file_label.pack(fill='x', padx=10, pady=5)
                file_label.bind("<Button-1>", lambda e, path=os.path.join(directory, file): open_file(path))
        else:
            Label(search_results_frame, text="No files found in directory", font=("Helvetica", 12), bg="#333333", fg="white").pack(anchor="w")

def compress_files_gui():
    file_paths = filedialog.askopenfilenames(title="Select Files to Compress")
    if file_paths:
        zip_file_path = filedialog.asksaveasfilename(defaultextension=".zip",
                                                     filetypes=[("Zip files", "*.zip")],
                                                     title="Save Compressed File As")
        if zip_file_path:
            zip_dir = os.path.dirname(zip_file_path)
            if not os.path.exists(zip_dir):
                messagebox.showerror("Error", "The specified directory does not exist.")
                return
            try:
                with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                    for file in file_paths:
                        zipf.write(file, os.path.basename(file))
                messagebox.showinfo("Success", "Files compressed successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to compress files: {e}")

def decompress_file_gui():
    zip_file_path = filedialog.askopenfilename(title="Select Zip File to Decompress",
                                               filetypes=[("Zip files", "*.zip")])
    if zip_file_path:
        extract_dir = filedialog.askdirectory(title="Select Destination Directory")
        if extract_dir:
            with zipfile.ZipFile(zip_file_path, 'r') as zipf:
                zipf.extractall(extract_dir)
            messagebox.showinfo("Success", "Files decompressed successfully.")

def search_files_gui(search_term):
    directory = select_directory()
    if directory:
        if search_term:
            found_files = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if search_term.lower() in file.lower():
                        found_files.append(os.path.join(root, file))

            search_results_frame.pack_forget()
            search_results_frame.pack(fill='both', padx=20, pady=10)

            if found_files:
                for widget in search_results_frame.winfo_children():
                    widget.destroy()

                Label(search_results_frame, text="Search Results:", font=("Helvetica", 12), bg="#333333", fg="white").pack(anchor="w")
                for file in found_files:
                    result_label = Label(search_results_frame, text=file, font=("Helvetica", 10), bg="#333333", fg="white", anchor="w", cursor="hand2")
                    result_label.pack(fill='x', padx=10, pady=5)
                    result_label.bind("<Button-1>", lambda e, path=file: open_file(path))
            else:
                Label(search_results_frame, text="No files found", font=("Helvetica", 12), bg="#333333", fg="white").pack(anchor="w")

def open_file(path):
    try:
        if os.name == 'nt':
            os.startfile(path)
        elif os.name == 'posix':
            subprocess.call(('xdg-open', path))
        elif os.name == 'darwin':
            subprocess.call(('open', path))
        else:
            messagebox.showerror("Error", "Unsupported OS")
    except Exception as e:
        messagebox.showerror("Error", f"Cannot open file: {e}")

def on_enter(e):
    e.widget['background'] = '#76c7c0'

def on_leave(e):
    e.widget['background'] = '#66b2b2'

# Create the main window
root = Tk()
root.title("Enhanced File Manager")
root.geometry("500x700")
root.configure(bg="#333333")

# Create a canvas for scrolling
canvas = Canvas(root, bg="#333333")
scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas, bg="#333333")

# Configure the scrollable frame
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create a window in the canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Link the scrollbar and canvas
canvas.configure(yscrollcommand=scrollbar.set)

# Pack the scrollbar and canvas
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# Add title label
title_label = Label(scrollable_frame, text="File Manager", font=("Helvetica", 18, "bold"), bg="#333333", fg="white")
title_label.pack(pady=20)

# Frame for buttons
button_frame = Frame(scrollable_frame, bg="#333333")
button_frame.pack(pady=20)

# Button configurations
button_style = {
    "font": ("Helvetica", 12, "bold"),
    "background": "#66b2b2",
    "foreground": "white",
    "activebackground": "#5ca0a0",
    "width": 20,
    "pady": 10,
    "relief": "raised",
    "borderwidth": 0
}

# Create and style buttons
buttons = [
    {"text": "Create Folder", "command": create_folder_gui, "tooltip": "Create a new folder"},
    {"text": "Create File", "command": create_file_gui, "tooltip": "Create a new file"},
    {"text": "Copy File", "command": copy_file_gui, "tooltip": "Copy a file to another location"},
    {"text": "Delete File", "command": delete_file_gui, "tooltip": "Delete a selected file"},
    {"text": "Rename File", "command": rename_file_gui, "tooltip": "Rename the selected file"},
    {"text": "Move File", "command": move_file_gui, "tooltip": "Move a file to another location"},
    {"text": "List Files", "command": list_files_gui, "tooltip": "List all files in a directory"},
    {"text": "Compress Files", "command": compress_files_gui, "tooltip": "Compress Selected Files in Directory"},
    {"text": "Decompress Files", "command": decompress_file_gui, "tooltip": "Decompress a Zip File"}
]

for button in buttons:
    btn = Button(button_frame, text=button["text"], command=button["command"], **button_style)
    btn.pack(pady=10)
    ToolTip(btn, button["tooltip"])

# Search bar frame
search_frame = Frame(scrollable_frame, bg="#333333")
search_frame.pack(pady=20)

# Search label and entry
search_label = Label(search_frame, text="Search for a file:", font=("Helvetica", 12), bg="#333333", fg="white")
search_label.pack(side=LEFT)
search_entry = Entry(search_frame, font=("Helvetica", 12), width=30)
search_entry.pack(side=LEFT, padx=10)

# Search button
search_button = Button(search_frame, text="Search", font=("Helvetica", 12), bg="#66b2b2", fg="white", relief="raised",
                       command=lambda: search_files_gui(search_entry.get()))
search_button.pack(side=LEFT)

# Frame for search results
search_results_frame = Frame(scrollable_frame, bg="#333333")
search_results_frame.pack(fill='both', padx=20, pady=10)

# Run the main event loop
root.mainloop()

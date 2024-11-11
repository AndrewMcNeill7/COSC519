# As of 10.12.24
import os
import shutil

# Function to create a folder


def create_folder(directory):
    folder_name = "NewFolder"
    folder_path = os.path.join(directory, folder_name)
    # Creates the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

# Function to create a file with dynamic name and extension


def create_file(directory, file_name="example", file_extension=".txt"):
    file_path = os.path.join(directory, f"{file_name}{file_extension}")
    with open(file_path, 'w') as f:
        f.write(f"This is an example {
                file_extension} file created inside the new folder.")
    return file_path

# Function to copy a file from source to destination


def copy_file(src, dst):
    try:
        shutil.copy(src, dst)  # Copies the file
        print(f"File copied from {src} to {dst}")
    except Exception as e:
        print(f"Error copying file: {e}")

        import shutil  # Required for moving files


def move_file(src, dst):
    try:
        shutil.move(src, dst)  # Moves the file from src to dst
    except Exception as e:
        print(f"Error moving file: {e}")
        raise


def list_files(directory):
    try:
        # List only files (not directories) in the given directory
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except Exception as e:
        print(f"Error listing files: {e}")
        raise

# Main function to interact with the user


def main():
    # Ensure the directory exists first
    directory = "C:/path/to/folder"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Ask user for file name and extension
    file_name = input("Enter the file name (without extension): ")
    file_extension = input(
        "Enter the file extension (e.g., .txt, .csv, .json): ")

    # Create the file with the user's inputs
    created_file = create_file(
        directory, file_name=file_name, file_extension=file_extension)
    print(f"File created: {created_file}")


# Ensure the main function runs only when the script is executed directly
if __name__ == "__main__":
    main()

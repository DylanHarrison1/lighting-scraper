import os

#col-12 col-md-6 bg-light p-3
#search for this

def GetFolderNames(directory):
    """
    Returns a list of folder names in the given directory.
    
    :param directory: Path to the directory
    :return: List of folder names
    """
    try:
        # List all entries in the directory
        entries = os.listdir(directory)
        # Filter out entries that are not directories
        folders = [entry for entry in entries if os.path.isdir(os.path.join(directory, entry))]
        return folders
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def StringSearch(file_path, search_string):
    """
    Takes a file path and the string to be searched, and returns lines it is present in.
    """
    matching_lines = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                if search_string in line:
                    matching_lines.append((line_number, line.strip()))
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return matching_lines

def CompanySearch(file_path: str) -> list:
    """
    Returns info for company
    """   
def BranchSearch(file_path: str) -> list:
    """
    Returns info for each branch
    """

folders = GetFolderNames(os.getcwd() + "\\HTML files")
folders = [os.getcwd() + "\\HTML files\\" +i + "\\index.html" for i in folders]
print(folders)

"""
# Example usage:
file_path = 'example.html'  # Replace with the path to your HTML file
search_string = 'your_search_string'  # Replace with the string you want to search for

result = StringSearch(file_path, search_string)
for line_number, line in result:
    print(f"Line {line_number}: {line}")
""" 

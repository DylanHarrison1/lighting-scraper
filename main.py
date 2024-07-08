import os
import re
#from bs4 import BeautifulSoup

#col-12 col-md-6 bg-light p-3
#search for this

#2851
#2855
#2874

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

def CompanySearch(path: str) -> list:
    """
    Returns info for company
    """
    entry = list()   

    # Company Name
    nameline = StringSearch(path, '<h4 class="mb-0">')
    entry.append(CleanGetLines(nameline, path))

    # Company/Branch
    entry.append("Company")

    # Location
    nameline = StringSearch(path, '<div class="col-12 col-sm-6 col-md-5 col-lg-6 mb-3 mb-sm-0">')

    # Phone
    # Email
    # Website
    # Date Added

def BranchSearch(file_path: str) -> list:
    """
    Returns info for each branch
    """
    entry = list()
    # Company Name
    
    # Company/Branch
    entry.append("branch")
    # Location
    # Phone
    # Email
    # Website
    # Date Added
def BranchesExist(file_path: str) -> bool:
    """
    Checks if a company has branches
    """
    
    lines = StringSearch(file_path, "Branch address")
    if lines == []:
        return False
    elif len(lines) == 1:
        return True
    else:
        print("Multiple instances of 'Branch address' for " + file_path)

def GetLines(line_numbers, file_path):
    """
    Given a list of line numbers and an HTML file, return the corresponding lines.

    Parameters:
    line_numbers (list of int): List of line numbers to extract.
    file_path (str): Path to the HTML file.

    Returns:
    list of str: List of strings corresponding to the given line numbers.
    """
    lines = []
    with open(file_path, 'r') as file:
        all_lines = file.readlines()
        
        for line_number in line_numbers:
            # Ensure the line number is within the valid range
            if 1 <= line_number <= len(all_lines):
                lines.append(all_lines[line_number - 1].strip())
            else:
                lines.append('')  # Optionally handle out-of-range lines

    return lines

def RemoveHtmlTags(html_line):
    # Use regular expression to remove tags
    clean_text = re.sub(r'<[^>]*>', '', html_line)
    return clean_text

def CleanGetLines(line_numbers, file_path):
    """
    A combination of GetLines and RemoveHtmlTags
    """
    strings = GetLines(line_numbers, file_path)
    return RemoveHtmlTags(strings[0])

folders = GetFolderNames(os.getcwd() + "\\HTML files")
folders = [os.getcwd() + "\\HTML files\\" + i + "\\index.html" for i in folders]

for file in folders:
    entry = CompanySearch(file)
    if BranchesExist(file):
        entry2 = BranchSearch(file)
"""
# Example usage:
file_path = 'example.html'  # Replace with the path to your HTML file
search_string = 'your_search_string'  # Replace with the string you want to search for

result = StringSearch(file_path, search_string)
for line_number, line in result:
    print(f"Line {line_number}: {line}")
""" 

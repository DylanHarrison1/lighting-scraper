import os
import re
from bs4 import BeautifulSoup
from datetime import datetime

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
    entry.append(CleanGetLines(nameline[0], path))

    # Company/Branch
    entry.append("Company")

    #Town
    nameline = StringSearch(path, '<div class="col-12 col-sm-6 col-md-5 col-lg-6 mb-3 mb-sm-0">')
    text = FetchWholeTag(file, nameline[0])
    capitalWords = re.findall(r'\b[A-Z]+\b', text)
    entry.append(capitalWords[0])

    # Location
    nameline = StringSearch(path, '<div class="col-12 col-sm-6 col-md-5 col-lg-6 mb-3 mb-sm-0">')
    text = FetchWholeTag(file, nameline[0])
    entry.append(RemoveHtmlTags(text))

    # Phone
    nameline = StringSearch(path, '<a href="tel:')
    entry.append(CleanGetLines(nameline[0], path))
    #will yield multiple results for branches

    # Email
    nameline = StringSearch(path, '<div class="col-10 text-truncate">')
    text = FetchWholeTag(file, nameline[0])
    entry.append(RemoveHtmlTags(text))
    
    # Website
    nameline = StringSearch(path, '<div class="col-10 text-truncate">')
    text = FetchWholeTag(file, nameline[1])
    entry.append(RemoveHtmlTags(text))
    #Same tag exists for email and website

    # Date Added
    current_date = datetime.now().date()
    current_date_str = current_date.strftime("%Y-%m-%d")
    entry.append(current_date_str)

    entry = [entry]
    return entry

def BranchSearch(path: str) -> list:
    """
    Returns info for each branch
    """
    branchno = len(StringSearch(path, '<a href="#" class="branch-preview">'))
    entry = [[] for i in range(branchno)]

    for i in range(branchno):

    
        # Company Name
        nameline = StringSearch(path, '<h4 class="mb-0">')
        entry.append(CleanGetLines(nameline[0], path))
        
        # Company/Branch
        entry[i].append("Branch")

        # Town 
        nameline = StringSearch(path, '<a href="#" class="branch-preview">')
        text = FetchWholeTag(file, nameline[i])
        entry[i].append(RemoveHtmlTags(text))

        # Location
        nameline = StringSearch(path, '<div class="col-6">')
        text = FetchWholeTag(file, nameline[i * 2])
        entry[i].append(RemoveHtmlTags(text))
        #Same divider used for Address and Phone

        # Phone
        nameline = StringSearch(path, '<a href="tel:')
        if len(nameline) != branchno + 1:
            entry[i].append("")
        else:
            text = FetchWholeTag(file, nameline[i + 1])
            entry[i].append(RemoveHtmlTags(text))
            

        # Email
        nameline = StringSearch(path, '<a href="mailto:')
        if len(nameline) != branchno + 3:
            entry[i].append("")
        else:
            text = FetchWholeTag(file, nameline[i + 1])
            entry[i].append(RemoveHtmlTags(text))
        #3 extra emails, 1 for business and 2 for EDA
        
        # Website
        entry[i].append("") #Assume none

        # Date Added
        current_date = datetime.now().date()
        current_date_str = current_date.strftime("%Y-%m-%d")
        entry[i].append(current_date_str)
    
    return entry

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

def FetchWholeTag(file_path, start_line):
    # Read the HTML file
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Join the lines to create a full HTML string
    html_content = ''.join(lines)
    
    # Check if the starting line is within the range of the file's lines
    if start_line < 1 or start_line > len(lines):
        raise ValueError("start_line is out of the range of the file's lines")
    
    # Extract the content from the specified starting line
    starting_content = ''.join(lines[start_line-1:])
    
    # Use BeautifulSoup to parse the HTML and find the first tag from the starting line
    soup = BeautifulSoup(starting_content, 'html.parser')
    
    # Find the first tag
    first_tag = None
    for element in soup.find_all():
        if str(element).startswith('<'):
            first_tag = element
            break
    
    if first_tag is None:
        raise ValueError("No tags found starting from the specified line")
    
    # Extract and return the text inside the first tag
    return first_tag.get_text()


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

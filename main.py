import os
import re
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

#Company Name,Company/Branch,Town,Location,Phone,Email,Website,Date Added

#col-12 col-md-6 bg-light p-3
#search for this

#2851
#2855
#2874
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def StringSearch(file_path, search_string):
    """
    Takes a file path and the string to be searched, and returns lines it is present in.
    """
    matching_lines = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                if search_string in line:
                    matching_lines.append(line_number)
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


    matching_lines = [int(i) for i in matching_lines]
    return matching_lines
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def CompanySearch(path: str) -> tuple[list, bool]:
    """
    Returns info for company
    """
    entry = list()   

    # Company Name
    nameline = StringSearch(path, '<h4 class="mb-0">')
    text = FetchWholeTag(file, nameline[0])
    entry.append(RemoveHtmlTags(text))

    # Company/Branch
    entry.append("Company")

    #Town
    nameline = StringSearch(path, '<div class="col-12 col-sm-6 col-md-5 col-lg-6 mb-3 mb-sm-0">')
    text = FetchWholeTag(file, nameline[0])
    capitalWords = re.findall(r'\b[A-Z-]{2,}\b', text)
    text = re.sub(r'^\s+|\s+$', '', capitalWords[0])
    entry.append(text)

    # Location
    nameline = StringSearch(path, '<div class="col-12 col-sm-6 col-md-5 col-lg-6 mb-3 mb-sm-0">')
    text = FetchWholeTag(file, nameline[0])
    text = re.sub(r'^[\s"]+|[\s"]+$', '', text) #Remove spaces / ""
    entry.append(RemoveHtmlTags(text))


    # Phone
    nameline = StringSearch(path, '<a href="tel:')
    text = FetchWholeTag(file, nameline[0])
    entry.append(RemoveHtmlTags(text))
    #will yield multiple results for branches

    # Email
    nameline = StringSearch(path, '<div class="col-10 text-truncate">')
    text = FetchWholeTag(file, nameline[0])
    if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', text) is not None:
        entry.append(RemoveHtmlTags(text))
        mailCheck = True
    else:
        entry.append("")
        mailCheck = False

    
    # Website
    nameline = StringSearch(path, '<div class="col-10 text-truncate">')
    if len(nameline) < 2:
        if mailCheck == True:
            text = ""
        else:
            text = FetchWholeTag(file, nameline[0])
    else:
        text = FetchWholeTag(file, nameline[1])
    entry.append(RemoveHtmlTags(text))
    #Same tag exists for email and website

    # Date Added
    current_date = datetime.now().date()
    current_date_str = current_date.strftime("%Y-%m-%d")
    entry.append(current_date_str)

    entry = [entry]
    return entry, mailCheck
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def BranchSearch(path: str, mailCheck: bool) -> list:
    """
    Returns info for each branch
    """
    townNum = len(StringSearch(path, '<a href="#" class="branch-preview">'))
    

    branchnum = 0
    emailAdjuster = 0
    phoneAdjuster = 0

    bpt = []    #branches per town
    townstr = []
    foundStrs = []
    mainNameLine = StringSearch(path, '<a href="#" class="branch-preview">')

    for i in range(townNum):
        text = FetchWholeTag(file, mainNameLine[i])
        text = re.sub(r'^\s+|\s+$', '', text)
        foundStrs.append(text)


        #check if there is more than 1 branch for this town
        match = re.search(r"(.*)\s\((\d+)\)$", foundStrs[i])
        if match:
            # Extract the main part of the string and the integer
            main_string = match.group(1)
            integer_part = int(match.group(2))
            townstr.append(main_string)
            bpt.append(integer_part)
        else:
            townstr.append(foundStrs[i])
            bpt.append(1)

    retList = []

    for i in range(townNum):
        for j in range(bpt[i]):
            entry = []
    
            # Company Name safe
            nameline = StringSearch(path, '<h4 class="mb-0">')
            text = FetchWholeTag(file, nameline[0])
            entry.append(RemoveHtmlTags(text))

            
            # Company/Branch safe
            entry.append("Branch")

            # Town safe
            entry.append(townstr[i])
            
            #x is our new "html index"
            x = 0
            for k in range(i):
                x += bpt[k] #add all previous branches
            x += j # Find current place

            #Address safish
            nameline = StringSearch(path, '<div class="col-6">')
            
            text = FetchWholeTag(file, nameline[x * 2])
            text = re.sub(r'^[\s"]+|[\s"]+$', '', text) #Remove spaces / ""
            entry.append(RemoveHtmlTags(text))
            #Same divider used for Address and Phone

            # Phone safeish
            """
            nameline = StringSearch(path, '<a href="tel:')
            if len(nameline) != sum(bpt) + 1:
                entry.append("")
            else:
                text = FetchWholeTag(file, nameline[x + 1])
                entry.append(RemoveHtmlTags(text))
            """

            nameline = StringSearch(path, '<a href="tel:')
            nameline.pop(0)

            curline = None
            lowerBound = mainNameLine[i]
            upperBound = 1000000 if len(mainNameLine) == i+1 else mainNameLine[i+1]
            filtered = [line for line in nameline if lowerBound <= line <= upperBound]
            if len(filtered) == bpt[i]:
                curline = nameline[i+j + phoneAdjuster]
            else:
                phoneAdjuster -= 1

                
            if curline != None:
                text = FetchWholeTag(file, curline)
                entry.append(RemoveHtmlTags(text))
            else:
                entry.append("")    




            # Email safeish
            nameline = StringSearch(path, '<a href="mailto:')
            if mailCheck:
                nameline.pop(0)
            nameline.pop(-1)
            nameline.pop(-1)#3 extra emails, 1 for business and 2 for EDA
            

            curline = None
            lowerBound = mainNameLine[i]
            upperBound = 1000000 if len(mainNameLine) == i+1 else mainNameLine[i+1]
            filtered = [line for line in nameline if lowerBound <= line <= upperBound]
            if len(filtered) == bpt[i]:
                curline = nameline[i+j +emailAdjuster]
            else:
                emailAdjuster -= 1
                
            if curline != None:
                text = FetchWholeTag(file, curline)
                entry.append(RemoveHtmlTags(text))
            else:
                entry.append("")    
            
            
            # Website safe
            entry.append("") #Assume none

            # Date Added safe
            current_date = datetime.now().date()
            current_date_str = current_date.strftime("%Y-%m-%d")
            entry.append(current_date_str)

            retList.append(entry)
    
    return retList
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def GetLines(line_number, file_path):
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
        
        
        # Ensure the line number is within the valid range
        if 1 <= line_number <= len(all_lines):
            lines.append(all_lines[line_number - 1].strip())
        else:
            lines.append('')  # Optionally handle out-of-range lines

    for line in lines:
        line = re.sub(r'\n', '', line)
        line = re.sub(r'\s+', ' ', line)
        #regex removing new lines and excess whitespace characters

    return line
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def RemoveHtmlTags(html_line):
    # Use regular expression to remove tags
    clean_text = re.sub(r'<[^>]*>', '', html_line)
    return clean_text
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def CleanGetLines(line_numbers, file_path):
    """
    A combination of GetLines and RemoveHtmlTags
    """
    strings = GetLines(line_numbers, file_path)
    return RemoveHtmlTags(strings[0])
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
    text = first_tag.get_text()

    text = re.sub(r'\n', '', text)
    text = re.sub(r'\s+', ' ', text)
    #regex removing new lines and excess whitespace characters

    return text
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def AppendRows(df, new_rows, cols):
    """
    Appends each inner list in new_rows as a new row in the DataFrame.
    """
    
    new_rows_df = pd.DataFrame(new_rows,columns=cols)
    
    df = df.append(new_rows_df, ignore_index=True)
    
    return df
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
folders = GetFolderNames(os.getcwd() + "\\HTML files")
#folders = [i for i in folders if int(i) >= 3100]
folders = [os.getcwd() + "\\HTML files\\" + i + "\\index.html" for i in folders]

datapath = os.getcwd() + "\\data.csv"

df = pd.read_csv(datapath, index_col=False)

for file in folders:
    print(file)
    entry, mailCheck = CompanySearch(file)
    df = AppendRows(df, entry, df.columns)

    if BranchesExist(file):
        entry2 = BranchSearch(file, mailCheck)
        df = AppendRows(df, entry2, df.columns)
    #print(df)

    df.to_csv(datapath, index=False)
    


#Fix added columns  (check entry no items?)
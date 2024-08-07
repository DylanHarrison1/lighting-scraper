import json
import csv
import pandas as pd
import os
import numpy as np

def ConvertData():
    # Load the GeoJSON data
    with open('export(1).geojson', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Prepare CSV file
    with open('towns.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'latitude', 'longitude']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for feature in data['features']:
            # Extract the name and coordinates
            name = feature['properties'].get('name')
            coordinates = feature['geometry']['coordinates']
            longitude, latitude = coordinates[0], coordinates[1]

            # Write to CSV
            writer.writerow({'name': name, 'latitude': latitude, 'longitude': longitude})

    print("CSV file has been created successfully.")

def Alphabetise(filename):
    filename = os.getcwd() + filename
    df = pd.read_csv(filename, index_col=False)
    
    # Sort the DataFrame by the first column
    df_sorted = df.sort_values(by=df.columns[0])
    
    # Write the sorted DataFrame to a new CSV file
    df_sorted.to_csv(filename, index=False)

def append_matching_rows(file1, file2, output_file):
    # Read the CSV files into DataFrames
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    
    # Convert the column of df2 that we will search into a numpy array
    search_array = list(df2[df2.columns[0]])
    
    # Function to perform binary search
    def binary_search(array, target):
        target = target.lower()
        left, right = 0, len(array) - 1
        while left <= right:
            mid = (left + right) // 2
            if array[mid].lower() == target:
                return mid
            elif array[mid].lower() < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1
    
    # List to hold the results
    results = []

    # Iterate through the values in the 3rd column of df1
    for index, row in df1.iterrows():
        target_value = row[df1.columns[2]]
        search_index = binary_search(search_array, target_value)
        
        if search_index != -1:
            # If a match is found, append the matching row from df2 to the current row of df1
            matched_row = df2.iloc[search_index].to_list()
            combined_row = row.tolist() + matched_row
            results.append(combined_row)
        else:
            # If no match is found, just append the current row of df1
            combined_row = row.tolist() + [np.nan] * len(df2.columns)
            results.append(combined_row)
    
    # Create a DataFrame from the results
    combined_columns = list(df1.columns) + list(df2.columns)
    combined_df = pd.DataFrame(results, columns=combined_columns)
    
    # Write the combined DataFrame to a new CSV file
    combined_df.to_csv(output_file, index=False)

#Alphabetise("\\towns.csv")

append_matching_rows(os.getcwd() + "\\pre-data.csv", os.getcwd() + "\\towns.csv", os.getcwd() + "\\compiled.csv")
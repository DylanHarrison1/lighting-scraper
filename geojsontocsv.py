import json
import csv
import pandas as pd
import os

def ConvertData():
    # Load the GeoJSON data
    with open('export.geojson', 'r', encoding='utf-8') as f:
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
Alphabetise("towns.csv")
import tkinter as tk
from tkinter import messagebox
import re
import numpy as np
import os
import pandas as pd

# Create the main application window
root = tk.Tk()
root.title("Basic GUI")


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth's surface.
    """
    # Radius of the Earth in kilometers
    R = 6371.0
    
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c
    
    return distance

def filter_within_distance(path, lat, lon, distance_km):
    """
    Filter rows in the DataFrame within a specified distance from the given latitude and longitude.
    """
    df = pd.read_csv(path, index_col=False)
    def within_distance(row):
        try:
            row_lat = float(row[3])
            row_lon = float(row[4])
        except ValueError:
            return False
        return haversine(lat, lon, row_lat, row_lon) <= distance_km
    
    filtered_df = df[df.apply(within_distance, axis=1)].copy()

    index = 0
    outputpath = os.getcwd() + "\\local-data.csv"
    while os.path.exists(outputpath):
        index += 1
        outputpath = os.getcwd() + "\\local-data(" + str(index) + ").csv"
    filtered_df.to_csv(outputpath, index=False)

# Create a function that will be called when the start button is clicked
def on_start():
    lat = entry1_part1.get()
    long = entry1_part2.get()
    rad = entry2.get()
    file = entry3.get()
    #messagebox.showinfo("Info", f"Input 1: {lat}\nInput 2: {long}")
    pattern = r'^-?\d+(\.\d+)?$'
    path = os.getcwd() + "\\" + file

    if not lat or not long or not rad:
        messagebox.showwarning("Warning", "Both input fields must be filled!" )
    elif not bool(re.match(pattern, lat)):
        messagebox.showwarning("Warning", "Latitude must be a number!")
    elif not bool(re.match(pattern, long)):
        messagebox.showwarning("Warning", "Longitude must be a number!")
    elif not bool(re.match(pattern, rad)):
        messagebox.showwarning("Warning", "Radius must be a number!")
    elif not os.path.exists(path):
        messagebox.showwarning("Warning", "File not found. Please make sure the file is in the same folder as this program, and not in any sub-folders.")
    else:
        filter_within_distance(path, float(lat), float(long), float(rad))
        messagebox.showinfo("Completed","Process completed! A new CSV file should have appeared. (If not, please make sure your inputted values were correct).")

# Create and place the first text prompt and entry field
label1 = tk.Label(root, text="Please enter the latitude/ longitude of your centre point (default = Halifax: 53.7229229,-1.8604874)")

label1.pack(pady=5)
frame1 = tk.Frame(root)
frame1.pack(pady=5)

entry1_part1 = tk.Entry(frame1)
entry1_part1.insert(0, "53.7229229")
entry1_part1.pack(side=tk.LEFT, padx=5)

entry1_part2 = tk.Entry(frame1)
entry1_part2.insert(0, "-1.8604874")
entry1_part2.pack(side=tk.LEFT, padx=5)

# Create and place the second text prompt and entry field
label2 = tk.Label(root, text="Please enter the radius (in km) you'd like the emails to be sent in. (The UK is around 1000km from North to South)")
label2.pack(pady=5)
entry2 = tk.Entry(root)
entry2.insert(0, "50")
entry2.pack(pady=5)

# Create and place the third text prompt and entry field
label3 = tk.Label(root, text="Please enter the name of the csv file you want to read from (default = data.csv)")
label3.pack(pady=5)
entry3 = tk.Entry(root)
entry3.insert(0, "data.csv")
entry3.pack(pady=5)

# Create and place the start button
start_button = tk.Button(root, text="Start", command=on_start)
start_button.pack(pady=20)

# Start the main event loop
root.mainloop()
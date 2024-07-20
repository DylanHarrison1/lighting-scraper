import requests
from math import radians, sin, cos, sqrt, atan2

def get_coordinates(postcode):
    url = 'https://api.opencagedata.com/geocode/v1/json'
    params = {
        'q': postcode,
        'key': 'YOUR_OPENCAGE_API_KEY',
        'countrycode': 'gb'
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data['results']:
        latitude = data['results'][0]['geometry']['lat']
        longitude = data['results'][0]['geometry']['lng']
        return latitude, longitude
    else:
        raise ValueError("Invalid postcode")

def haversine_distance(coord1, coord2):
    # Coordinates in decimal degrees (e.g. 52.2296756, 21.0122287)
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    # Convert decimal degrees to radians 
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    distance = r * c

    return distance

def main(postcode1, postcode2):
    coord1 = get_coordinates(postcode1)
    coord2 = get_coordinates(postcode2)
    distance = haversine_distance(coord1, coord2)
    return distance

postcode1 = "SW1A 1AA"  # Example postcode 1
postcode2 = "EC1A 1BB"  # Example postcode 2

distance = main(postcode1, postcode2)
print(f"The distance between {postcode1} and {postcode2} is {distance:.2f} kil
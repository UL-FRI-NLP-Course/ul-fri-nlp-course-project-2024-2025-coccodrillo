import pandas as pd
import math
from geopy.geocoders import Nominatim
import time


def load_data(file_path):

    df = pd.read_csv(file_path, sep=",", encoding="ISO-8859-1")
    return df


def get_column_for_city(df, city_name, column_name):
    # Filtra la città e la colonna specificata
    city_data = df[df['Destination'].str.lower() == city_name.lower()]
    
    if city_data.empty:
        return f"Nessuna città trovata con il nome '{city_name}'."
    
    if column_name not in df.columns:
        return f"La colonna '{column_name}' non esiste."
    
    return city_data[column_name].values[0]



def haversine(lat1, lon1, lat2, lon2):
    # Earth Radius in km
    R = 6371.0
    
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c  # in km
    return distance



def get_distance(lat1,long1,lat2,long2):
    distance = haversine(lat1,long1,lat2,long2)
    return distance


def get_nodo_closest(lat, long, city):
    file_path = f"dataset/city/{city}.csv"
    df = load_data(file_path)

    min_distance = float("inf")
    nodo_start_index = 0  #default

    for index, row in df.iterrows():
        dist = get_distance(float(lat), float(long), row['lat'], row['long'])
        if dist < min_distance:
            min_distance = dist
            nodo_start_index = index  # <-- Qui salviamo l'indice

    return nodo_start_index






def get_lat_long_from_place(place_name):
    geolocator = Nominatim(user_agent="your_app_name_here_geopy_123456", timeout=10)
    try:
        location = geolocator.geocode(place_name)
        time.sleep(1)  # rispetto delle policy
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        return None, None



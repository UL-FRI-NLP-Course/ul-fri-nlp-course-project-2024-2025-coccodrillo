import pandas as pd
import math


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


file_path = "geo_europa/destinations.csv"
df = load_data(file_path)


city_name1 = "Rome"  
city_name2 = "Florence"
lat = "Latitude"
long = "Longitude"            
lat_city1 = float(get_column_for_city(df, city_name1, lat))
lat_city2 = float(get_column_for_city(df, city_name2, lat))
long_city1 = float(get_column_for_city(df, city_name1, long))
long_city2 = float(get_column_for_city(df, city_name2, long))
distance = haversine(lat_city1,long_city1,lat_city2,long_city2)
print(distance)



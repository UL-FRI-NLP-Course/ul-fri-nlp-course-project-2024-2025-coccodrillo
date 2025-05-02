from geopy.geocoders import Nominatim

def get_country(city_name):
    geolocator = Nominatim(user_agent="myGeolocationApp-v1")  # Aggiungi un nome specifico per la tua app
    location = geolocator.geocode(city_name)

    if location:
        # Restituisce il paese della città
        return location.address.split(",")[-1].strip()
    else:
        return ""


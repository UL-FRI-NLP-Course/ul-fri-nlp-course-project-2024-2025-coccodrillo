import pandas as pd
from fuzzywuzzy import fuzz
import spacy
# Carica il modello di lingua di spaCy (con word vectors)
nlp = spacy.load("en_core_web_sm")

escludi = ['train']

def upload_data(file_csv,header):
    df = pd.read_csv(file_csv)
    return df[header].tolist()



def get_best_city(citta_input,file_csv = './dataset/destinations.csv',header='Destination'):
    #se destination ha piu di una parola deov analizzarle tutte e prende quella con la miglior somiglianza
    if citta_input.lower() in escludi:
         return None
    destinations = upload_data(file_csv,header)
    somiglianza_max = 0
    destinazione_max = ""
    for city in destinations:
        somiglianza = fuzz.ratio(citta_input.lower(), city.lower())  
        if somiglianza > somiglianza_max:
            somiglianza_max = somiglianza
            destinazione_max = city

    if somiglianza_max <= 75:
        return None
    return destinazione_max


def get_best_period(word,file_csv= "./dataset/periods.csv",header="Period"):
        destinations = upload_data(file_csv,header)
        somiglianza_max = 0
        destinazione_max = ""
        for city in destinations:
            somiglianza = fuzz.ratio(word.lower(), city.lower())  
            if somiglianza > somiglianza_max:
                somiglianza_max = somiglianza
                destinazione_max = city

        if somiglianza_max <= 80:
            return None
        return destinazione_max



def get_celebrities(text,file_csv= "./dataset/singer.csv",header="Singer"):
    
        events = upload_data(file_csv,header)
        somiglianza_max = 0
        destinazione_max = ""
        traditions = []
        tokens = nlp(text)
        for token in tokens:
            for city in events:
                somiglianza = fuzz.ratio(token.text.lower(), city.lower())  
                if somiglianza > somiglianza_max:
                    somiglianza_max = somiglianza
                    destinazione_max = city
            if somiglianza_max > 85:
                 traditions.append(destinazione_max)
                 somiglianza_max = 0
        return traditions

   
from fuzzywuzzy import fuzz

# Dizionario con chiave più leggibile e valore originale
genre_dict = {
    "Alternative": "alternative",
    "Blues": "blues",
    "Christian Gospel": "christian-gospel",
    "Classical": "classical",
    "Country": "country",
    "Comedy": "comedy",
    "Electronic": "electronic",
    "Folk": "folk",
    "Hip Hop": "hip-hop",
    "Jazz": "jazz",
    "Latin": "latin",
    "Metal": "metal",
    "Pop": "pop",
    "Punk": "punk",
    "R&B / Soul": "rnb-soul",
    "Reggae": "reggae",
    "Rock": "rock",
    "All Genres": "all-genres"
}

# Funzione per ottenere il valore più simile
def get_genres(input_string):
    max_similarity = 0
    best_match = None
    doc = nlp(input_string)
    for token in doc:
        for readable_genre in genre_dict.keys():
            similarity = fuzz.ratio(token.text.lower(), readable_genre.lower())
            if similarity > max_similarity:
                max_similarity = similarity
                best_match = readable_genre

    # Soglia opzionale per escludere match poco simili
    if max_similarity < 80:
        return ""
    
    return genre_dict[best_match]



def get_all_gen():
     return genre_dict.values()
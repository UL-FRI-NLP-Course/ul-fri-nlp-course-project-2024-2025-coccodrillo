from typical_food import get_nation
import random
from pathlib import Path


ls_particual_name = [
                    'België / Belgique / Belgien',
                    'Bosna i Hercegovina / Босна и Херцеговина',
                    'Suomi / Finland',
                    'Éire / Ireland',
                    'Kosova / Kosovo',
                    'Crna Gora / Црна Гора',
                    'Schweiz/Suisse/Svizzera/Svizra'
                     ]






def extract_name(dish):
    """Estrae la prima parola (nome del piatto) fino al primo salto di riga"""
    end = dish.find("\n")
    return dish[:end].strip()    


def convert_to_decimal(value):
    try:
        # Prova a convertire la stringa in un numero decimale
        return float(value.replace(",", "."))
    except ValueError:
        # Se la conversione fallisce, ritorna 0
        return 0

def extract_info(city, file_path):

    file_path =  Path(file_path)
    with open(file_path, 'r',encoding='utf-8') as file:
        data = file.read()
    
    # Dividi i dati in piatti
    dishes = data.split("name=")
    
    result_location = []
    result_no_location = []
    
    for dish in dishes:
        if city.lower() in dish.lower() or "location=n/a" in dish.lower():
            # Estrai il tipo di piatto, recensione e descrizione
            name = extract_name(dish)
            location = extract_field(dish, "location=")
            review = extract_field(dish, "review=")
            review = convert_to_decimal(review)
            food_type = extract_field(dish, "food_type=")
            description = extract_field(dish, "description=")
            if location.lower() == city.lower():
                result_location.append({
                    "name": name,
                    "location": location,
                    "review": review,
                    "food_type": food_type,
                    "description": description
                })
            elif location.lower() == "n/a":
                result_no_location.append({
                    "name": name,
                    "location": location,
                    "review": review,
                    "food_type": food_type,
                    "description": description
                })
    
    return result_location,result_no_location


def extract_field(dish, field):
    """Estrae il valore di un campo dato da un piatto"""
    start = dish.find(field)
    if start == -1:
        return None
    start += len(field)
    end = dish.find("\n", start)
    return dish[start:end].strip()




def get_best_food(city):
    nation = get_nation.get_country(city)
    if nation in ls_particual_name:
        nation = nation.split('/')[0].strip()
    #nation = translate.get_translate(nation,"en").lower()
    try:
        file_path ="dataset/typical_food_europe/"+nation.lower()+".txt"

        dishes_info_location,dishes_info_no_location = extract_info(city, file_path)
        # Ordinare la lista di dizionari in base alla recensione (review) in ordine decrescente
        dishes_info_location = sorted(dishes_info_location, key=lambda x: x["review"], reverse=True)
        dishes_info_no_location = sorted(dishes_info_no_location, key=lambda x: x["review"], reverse=True)

        weights = [dish["review"] for dish in dishes_info_location]
        weights2 = [dish["review"] for dish in dishes_info_no_location]
        if len(dishes_info_location) <= 3:
            n = len(dishes_info_location)
        else:
            n = random.randint(3,15)
        if len(dishes_info_no_location) <= 3:
            n2 = len(dishes_info_no_location)
        else:
            n2 = random.randint(3,15)
        selected_dishes_location = []
        selected_dishes_no_location = []
        if dishes_info_location:
            selected_dishes_location = random.choices(dishes_info_location, weights=weights, k=n)
        if dishes_info_no_location:
            selected_dishes_no_location = random.choices(dishes_info_no_location, weights=weights2, k=n2)
        if len(selected_dishes_location) < 3:
            total = selected_dishes_location
            total.extend(selected_dishes_no_location)
            return total
        else:
            return selected_dishes_location
    except:
        print("Error: File not found or empty")
        return []
    



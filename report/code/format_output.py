from datetime import datetime
import re
from pandas import Timestamp


def get(diz,id):
    if id == 0:
        return output_id0(diz)
    if id == 1:
        return output_id1(diz)
    if id == 2:
        return output_id2(diz)
    if id == 3:
        return output_id3(diz)
    if id == 4:
        return output_id4(diz)
    if id == 5:
        return output_id5(diz)
    if id == 6:
        return output_id6(diz)
    if id == 7:
        return output_id7(diz)




def output_id0(diz):
    # Loop through each country and its associated data
    output = ""
    for country, data in diz.items():
        if "_doc" not in country:
            output += (f"🌍 *{country}*:\n" + "-" * 40)
            output +="\n"
            
            # Display the articles or news data
            for entry in data:
                entry = entry.replace('\n', ' ').strip()
                entry = re.sub(r'\s+', ' ', entry).strip()
                output+=(f"📰 {entry}\n\n")

            # Check if a document related to the country exists dynamically
            doc_key = f'{country.lower()}_doc'  # Build the doc key dynamically, e.g., 'france_doc', 'spain_doc'
            if doc_key in diz:
                doc_date, doc_content = diz[doc_key]
                output+=(f"📅 *Document Date*: {doc_date}\n")
                output+=(f"📄 *Document Content*: {doc_content}\n" + "=" * 40)
                output+="\n"
    return output

# Function to format and display the news data in a readable way
def format_news_data(city, news_data):
    output = ""
    output +=(f"🌆 News for {city}:\n")
    output +=("=" * 40)
    output += "\n"
    
    for news_item in news_data:
        # Split the text by newlines to separate parts
        parts = news_item.split('\n')
        
        # Extract the date and description from the split parts
        date_info = parts[0] if len(parts) > 0 else "Date not available"
        description = " ".join(parts[1:]) if len(parts) > 1 else "Description not available"
        
        # Print the formatted information
        output +=(f"📅 Date and Time: {date_info}\n")
        output +=(f"📝 Description: {description}\n")
        output +=("—" * 40)
        output +="\n"
    return output

def output_id1(diz):
    # Itera su tutte le città e stampa le notizie
    output = ""
    for city, news_list in diz.items():
        output += format_news_data(city, news_list)
        output+="\n"
        output+=("\n" + "=" * 40 + "\n\n")
    return output

def output_id2(diz):
    output = []

    for city, (places, duration) in diz.items():
        rounded_duration = round(duration)  # Approximate to nearest hour
        output.append(f"🗺️ Here's the itinerary for {city}:")
        output.append(f"⏳ Total estimated time: {rounded_duration} hours\n")
        output.append("📍 Places to visit:")

        for name, status in places:
            if status == '1':
                output.append(f"  ✅ {name}")
            else:
                output.append(f"  ❌ {name} (temporarily closed)")

        output.append("")  # blank line between cities

    return "\n".join(output)



# Funzione per formattare i dati degli eventi
def format_event_data(city, city_data):
    output = ""
    output+=(f"🌆 Events in {city}\n:")
    output+=("=" * 40)
    output+="\n"
    for event in city_data:
        singer = event['Singer']
        event_name = event['Event_Name']
        description = event['Description']
        date_and_time = event['Date_and_Time']
        location = event['Location']

        output+=(f"🎤 *{event_name}* - {singer}\n")
        output+=(f"📅 Date and Time: {date_and_time}\n")
        output+=(f"🏙️ Location: {location}\n")
        output+=(f"📝 Description: {description}\n")
        output+=("—" * 40)
        output+="\n"

    return output

def output_id3(diz):
   # Itera su tutte le città e stampa gli eventi
    output = ""
    for city, events_list in diz.items():
        # Appiattisci la lista, poiché gli eventi sono dentro una lista di lista
        events = [event for sublist in events_list for event in sublist]
        
        # Ordina gli eventi per data
        sorted_events = sorted(events, key=lambda x: x['Date_and_Time'])
        
        # Stampa i dati formattati
        output += format_event_data(city, sorted_events)
        output +="\n"
        output+=("\n" + "=" * 40 + "\n")
        output+="\n"
    return output



def format_restaurant_data(city_data):
    output = ""
    for r in city_data:
        name = r['Name']
        location = r['Location']
        rating = float(r['Reviews'])

        # Generazione delle stelle
        stars = "⭐" * int(round(rating)) + f" ({rating:.1f})"

        output+=(f"🍴 *{name}*\n")
        output+=(f"📍 Zone: {location}\n")
        output+=(f"🧾 Review: {stars}\n")
        output+=("—" * 40)
        output+="\n"
    return output



def output_id4(diz):
    # Itera su tutte le città e stampa i dati
    output = ""
    for city, restaurants in diz.items():
        output+=(f"🏙️ Restaurants in {city}:\n")
        output+=("=" * 40)
        output+="\n"
        # Ordina i ristoranti per valutazione decrescente
        sorted_restaurants = sorted(restaurants, key=lambda x: float(x['Reviews']), reverse=True)
        output += format_restaurant_data(sorted_restaurants)
        output+=("\n" + "=" * 40 + "\n\n")
    return output







def deduplicate_food_items(food_list):
    seen = set()
    unique_items = []
    for item in food_list:
        key = (item["name"].lower().strip(), item["location"].lower().strip())
        if key not in seen:
            seen.add(key)
            unique_items.append(item)
    return unique_items

def output_id5(diz):
   # Function to deduplicate items based on name and location
    # Process and display data
    output = ""
    for city, items in diz.items():
        output+=(f"\nTop food items in {city}:\n")
        
        unique_items = deduplicate_food_items(items)
        sorted_items = sorted(unique_items, key=lambda x: x["review"], reverse=True)
        
        for item in sorted_items:
            output+=(f"🍽️ *{item['name']}* ({item['food_type']})\n")
            output+=(f"📝 {item['description']}\n")
            output+=(f"⭐ Review: {item['review']:.1f}/5.0\n")
            output+=("—" * 40)
            output+="\n"
    return output




def output_id6(diz):
    output = ""
    for city, forecasts in diz.items():
        for forecast in forecasts:
            # Estraggo la data (assumo che tutti i timestamp siano dello stesso giorno)
            date_obj = forecast['Day'][0]
            date_str = datetime.strftime(date_obj, "%A, %B %d, %Y")

            output += f"### 📍 **Weather Forecast for {city}**\n\n"
            output += f"📅 **{date_str}**\n\n"
            output += "```\n"
            output += "|   Time   | Temperature |   Rain   |   Wind      |\n"
            output += "|----------|-------------|----------|-----------  |\n"

            for time, temp, rain, wind in zip(forecast['Hour'], forecast['Temperatura'], forecast['Precipitazioni'], forecast['Wind']):
                # Emoji meteo
                rain_icon = "☀️" if rain == "absent" else "🌧️"
                output += f"|  {time:<7} |   {temp:<9} | {rain_icon} {rain:<6} | 💨 {wind:<8} |\n"
            output += "```\n\n"
    return output




def is_valid_trip(entry):
    return (
        isinstance(entry.get('departure'), str) and entry['departure'].startswith("Departs at") and
        isinstance(entry.get('arrive'), str) and entry['arrive'].startswith("Arrives at")
    )

def output_id7(data):
    result = ""

    for transport, directions in data.items():
        result += f"\n🚍🚆 {transport.upper()}\n"

        for direction, trips in directions.items():
            result += f"\n  {'➡️ Outbound' if direction == 'andata' else '⬅️ Return'}:\n"
            valid_found = False

            for trip in trips:
                if not is_valid_trip(trip):
                    continue  # Skip if fields are not properly formatted

                valid_found = True
                result += f"    🕒 Departure: {trip['departure']}\n"
                result += f"    🛬 Arrival: {trip['arrive']}\n"
                result += f"    ⏱️ Duration: {trip.get('duration', 'N/A')}\n"

                if 'std_class' in trip:
                    result += f"    💺 Standard: {trip['std_class']}\n"
                if 'first_class' in trip:
                    result += f"    🥂 First class: {trip['first_class']}\n"
                result += "    ─────────────────────────────\n"

            if not valid_found:
                result += "    ⚠️ No valid trips found.\n"

    return result


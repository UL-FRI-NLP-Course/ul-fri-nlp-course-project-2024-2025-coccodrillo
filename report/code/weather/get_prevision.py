import requests
from bs4 import BeautifulSoup
import os
import csv
from datetime import datetime
import re
import translate
from dateparser import parse
import re


def get_data_from_time(df, start_time):
    """
    Funzione che filtra il DataFrame per restituire tutte le righe a partire da un orario specificato.
    La ricerca dell'orario viene effettuata riga per riga e i dati vengono stampati solo una volta che l'orario di inizio è raggiunto.
    
    :param df: DataFrame contenente i dati meteo
    :param start_time: Orario di inizio (formato 'HH:MM', ad esempio '20:00')
    :return: DataFrame filtrato contenente solo i dati a partire da start_time
    """
    # Converte la colonna 'Time' in formato datetime (solo l'orario, senza data)
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M').dt.strftime('%H:%M')

    # Iniziamo una lista vuota per raccogliere i dati da stampare
    result = []
    start_printing = False
    
    # Itera riga per riga nel DataFrame
    for _, row in df.iterrows():
        if start_printing or row['Time'] >= start_time:
            result.append(row)
            start_printing = True  # Dopo il primo match, inizia a stampare tutte le righe successive
    
    # Restituisce un DataFrame contenente solo le righe selezionate
    return pd.DataFrame(result)


def clean_text(text):
    # Mantieni solo lettere (alfabetiche) e rimuovi i caratteri speciali
    cleaned_text = re.sub(r'[^a-zA-Z]', '', text)  # rimuove tutto tranne lettere maiuscole e minuscole
    return cleaned_text

def get_parameters(hourly, day, filename="weather_forecast.csv"):
    headers = ["Time", "Temperatura", "Precipitazioni", "Wind"]
    
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        if file.tell() == 0:
            writer.writerow(["Day"] + headers)

        
        for forecast in hourly:
            ora = forecast.find('td').text.strip()
            temp = forecast.find('td', {'data-value': 'temperatura'}).text.strip()
            prec_elem = forecast.find_all('td')[3]
            prec_text = prec_elem.find('span').text.strip() if prec_elem.find('span') else "0 mm"
            vento_elem = forecast.find_all('td')[5]
            vento_info = "".join([char for char in vento_elem.text.strip().replace("\n", " ") if not char.isupper()])
            parsed_date = parse(day, settings={'PREFER_DATES_FROM': 'future', 'DATE_ORDER': 'DMY'})
            
            prec_text = clean_text(prec_text)
            vento_info = clean_text(vento_info)
            prec_text = translate.get_translate(prec_text,"it","en")
            vento_info = translate.get_translate(vento_info,"it","en")
            if parsed_date:
                writer.writerow([parsed_date.strftime("%d/%m/%Y"), f"{ora}:00", f"{temp}˚C", "".join(re.findall(r"[a-zA-Z]+", prec_text)), "".join(re.findall(r"[a-zA-Z]+", vento_info))])
                
            else:
                writer.writerow([day, f"{ora}:00", f"{temp}˚C", "".join(re.findall(r"[a-zA-Z]+", prec_text)), "".join(re.findall(r"[a-zA-Z]+", vento_info))])
            






def analyze_url(url, headers, filename="weather_forecast.csv"):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        forecast_days = soup.find_all('li', class_='forecast_day_selector__list__item')
        
        for day in forecast_days:
            date_element = day.find('span', class_='forecast_day_selector__list__item__link__date')
            if date_element:
                giorno_settimana = date_element.contents[0].strip()
                giorno_numero = date_element.find('span').text.strip()
                giorno_completo = f"{giorno_settimana} {giorno_numero}"
            else:
                continue
            
            link = day.find('a', href=True)
            link_url = link['href'] if link else None
            if link_url:
                daily_response = requests.get(link_url, headers=headers)
                if daily_response.status_code == 200:
                    daily_soup = BeautifulSoup(daily_response.text, 'lxml')
                    weather_tables = daily_soup.find_all('table', class_='weather_table')
                    
                    if weather_tables:
                        hourly_forecasts = daily_soup.find_all('tr', class_=['dialog-open forecast_3h',
                                                                             'dialog-open hidden forecast_3h ok_temperatura',
                                                                             'dialog-open hidden forecast_1h ok_temperatura'])
                        if hourly_forecasts:
                            get_parameters(hourly_forecasts, giorno_completo, filename)
    else:
        print("Error fetching data from URL")



def filter_weather_by_date(filename, target_date):
    target_day = datetime.strptime(target_date, "%d/%m/%Y").day
    
    with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)
        output = ""

        
        for row in reader:
            day_info = row[0].split(" ")
            if len(day_info) == 2 and day_info[1].isdigit():
                if int(day_info[1]) == target_day:
                    output += ", ".join(row) + "\n"

    return output


def run(city):
    city = translate.get_translate(city,"en","it")
    url = f'https://www.ilmeteo.it/meteo/{city}'
    

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    long_term_link = ""
    path_file = "weather.csv"
    if os.path.exists(path_file):
        with open(path_file, "w") as fp:
            pass  

    analyze_url(url,headers,path_file)
    if (long_term_link != ""):
        analyze_url(long_term_link,headers,path_file)







import pandas as pd
from datetime import datetime

def get_data_by_day(input_day):
    df = pd.read_csv("weather.csv")
    df['Day'] = pd.to_datetime(df['Day'], format='%d/%m/%Y')  
    if input_day != "":
        input_date = datetime.strptime(input_day, '%d/%m/%Y')
        filtered_df = df[df['Day'] == input_date]
    else:
        filtered_df = df
    return filtered_df


import pandas as pd

def get_forecast_by_time_of_day(df, part_of_day):
    try:
        """
        :param df: DataFrame contenente i dati del meteo
        :param part_of_day: La parte della giornata (può essere 'mattina', 'pomeriggio', 'sera', 'notte')
        :return: Un DataFrame con le previsioni corrispondenti alla parte della giornata
        """
        # Sostituiamo "24:00" con "00:00" per evitare problemi di formato
        df['Time'] = df['Time'].replace("24:00", "00:00")
        
        # Assicurati che la colonna 'Time' sia in formato datetime
        df['Time'] = pd.to_datetime(df['Time'], format='%H:%M')
        
        # Estrai solo l'ora dalla colonna Time e crea una colonna separata 'Hour'
        df['Hour'] = df['Time'].dt.strftime('%H:%M')

        # Crea un dizionario per gli intervalli orari delle varie parti della giornata
        time_intervals = {
            'morning': (5, 12),       # 5:00 - 11:00
            'afternoon': (12, 19),   # 11:00 - 18:00
            'evening': (18, 22),         # 18:00 - 21:00
            'night': (22, 3),          # 22:00 - 5:00
            'all_day': (5 , 22)
        }

        # Prendi l'intervallo di tempo per la parte della giornata
        if part_of_day in time_intervals:
            start_hour, end_hour = time_intervals[part_of_day]
            
            if part_of_day == 'night':
                # La notte va oltre la mezzanotte, quindi gestiamo l'intervallo separatamente
                night_filter = (df['Time'].dt.hour >= start_hour)     # Dalle 00:00 alle 5:00
                morning_filter =  (df['Time'].dt.hour < end_hour)
                filtered_df = df[night_filter | morning_filter]
                filtered_df = get_data_from_time(filtered_df,"20:00")
                
            else:
                filtered_df = df[(df['Time'].dt.hour >= start_hour) & (df['Time'].dt.hour < end_hour)]
            
            # Restituisci solo le colonne 'Day' e 'Hour'
            dizionario = filtered_df[['Day', 'Hour','Temperatura' ,'Precipitazioni' , 'Wind']].to_dict(orient='list')
            return dizionario
        else:
            return f"Error"

    except:
         return pd.DataFrame([])






def get_prevsioni_day_time(city,day,time):
    run(city)
    #if day is "" ritorna tutto
    df = get_data_by_day(day)
    if day == "":
        return df
    data = get_forecast_by_time_of_day(df, time)
    if type(data) == str:
        return "Sorry, i cannot calculate this."
    if len(data) == 0:
        return "Sorry, i cannot calculate this."
    return data


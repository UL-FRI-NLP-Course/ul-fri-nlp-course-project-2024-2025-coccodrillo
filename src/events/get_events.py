from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re  
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import spacy

nlp = spacy.load("en_core_web_sm")
options = Options()

web = "https://www.bandsintown.com/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
    

def coockie(driver):
    try:
        # Il pulsante di accettazione dei cookie ha una classe comune
        accept_button = driver.find_element(By.CLASS_NAME, "UywwFc-RLmnJb")
        accept_button.click()
        print("Cookie accettati!")
    except Exception as e:
        print("Errore nell'accettare i cookie:", e)






def naviga(web,citta,data_start,data_end,genere,driver):
    
    driver.get(web)
    try:
        button = driver.find_element(By.CLASS_NAME, "_H_WpH0XePsSga7aKadV")
        button.click()  
        time.sleep(2)
        location_input = driver.find_element(By.XPATH, "//input[@data-test='popularEvents__locationInput']")
        location_input.clear()
        location_input.send_keys(citta)
        location_input.send_keys(Keys.RETURN)

        time.sleep(3)
        button = driver.find_element(By.CLASS_NAME, "tS0JgXsot1MbDfv2jv5T")
        button.click()  
        time.sleep(2)

        current_url = driver.current_url

        match = re.search(r"city_id=([^&]+)", current_url)
        if match:
            city_id = match.group(1)
            new_page = f"https://www.bandsintown.com/choose-dates/genre/{genere}?city_id={city_id}&calendarTrigger=false&date={data_start}T00%3A00%3A00%2C{data_end}T23%3A00%3A00"
            driver.get(new_page)
        else:
            return None

        time.sleep(3)
        current_url = driver.current_url
        response = requests.get(current_url, headers=headers)
        if response.status_code == 200:
            return response

    except:
        return None


def get_events(html,driver):
    output = ""
    soup = BeautifulSoup(html, 'lxml')
    events = soup.find_all('a', class_='HsqHp2xM2FkfSdjy1mlU')
    for event in events:
        event_name = event.find('div', class_='_5CQoAbgUFZI3p33kRVk').text.strip()
        description = event.find('div', class_='bqB5zhZmpkzqQcKohzfB').text.strip()
        date_time = event.find('div', class_='r593Wuo4miYix9siDdTP').text.strip()
        cantante = event.find('div', class_='_5CQoAbgUFZI3p33kRVk').text.strip()
        output += f"Singer:   {cantante}"   + "\n" \
                  f"Event Name: {event_name}"   + "\n" \
                  f"Description: {description}" + "\n" \
                  f"Date and Time: {date_time}" + "\n" 
      
        event_link = event['href']
        driver.get(event_link)
        time.sleep(3)  # Aspetta che la nuova pagina si carichi
        event_page_soup = BeautifulSoup(driver.page_source, 'lxml')
        location = event_page_soup.find('div', class_='e6YFaVBz8eqoPeVSqavc') 
        if location:
            output += f"Location: {location.text.strip()}" + "\n"
        else:
            output += "Location: Not found\n"

        output += '-' * 40 +"\n"
    driver.quit()
    return output




def get_tables(response):
    try:
        soup = BeautifulSoup(response.text, 'lxml')
        table = soup.find_all('div', class_='MtafMVpvYyCTdxtbFglz')
        table = str(table)
        html = table[1:-1]
        return html
    except:
        return []

gen = [ 
    'alternative',
    'blues',
    'christian-gospel',
    'classical',
    'country',
    'comedy',
    'electronic',
    'folk',
    'hip-hop',
    'jazz',
    'latin',
    'metal',
    'pop',
    'punk',
    'rnb-soul',
    'reggae',
    'rock',
    'all-genres'
]




def run(start,end,city,genres):

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.minimize_window()
    pagina_html = naviga(web,city,start,end,genres,driver)
    table = get_tables(pagina_html)
    if table == []:
        events = ""
    else:
        events = get_events(table,driver)
    fp = open("events.txt","w")
    fp.write(events)
    fp.close()









def search_event_singer(start,end,city,singer,gen='all-genres'):
    start = datetime.strptime(start, "%d/%m/%Y").strftime("%Y-%m-%d")
    end = datetime.strptime(end, "%d/%m/%Y").strftime("%Y-%m-%d")
    if singer != "":
        gen = 'all-genres'                              #perche non devo porre vincoli di ricerca su generi!
    
    run(start,end,city,gen)
    eventi_singer = []
    with open("events.txt", "r", encoding="utf-8", errors="ignore") as file:
        linee = file.readlines()

    for i in range(0, len(linee), 6):
        cantante = linee[i].strip().split(":")[1]  # La riga sopra il nome dell'evento
        nome_evento = linee[i + 1].strip().split(":")[1]  # Il nome dell'evento
        descrizione = linee[i + 2].strip().split(":")[1]  # Descrizione
        data_ora = linee[i + 3].strip().split(":")[1]  # Data e ora
        luogo = linee[i + 4].strip().split(":")[1]  # Luogo
        
        # Verifica se la parola "singer" è nel cantante
        if singer != "":
            cantante = cantante.strip()
            if cantante.lower().startswith(singer.lower()):
                eventi_singer.append({
                    'Singer': cantante.strip(),
                    'Event_Name': nome_evento.strip(),
                    'Description': descrizione.strip(),
                    'Date_and_Time': data_ora.strip(),
                    'Location': luogo.strip()
                })
        else:
            eventi_singer.append({
                    'Singer': cantante.strip(),
                    'Event_Name': nome_evento.strip(),
                    'Description': descrizione.strip(),
                    'Date_and_Time': data_ora.strip(),
                    'Location': luogo.strip()
                })
        
    return eventi_singer



def filter_city_period(city, city_period_list):
    result = []

    for record in city_period_list:
        city_name = record[0]
        if city_name == city:
            result.append(record)  

    return result





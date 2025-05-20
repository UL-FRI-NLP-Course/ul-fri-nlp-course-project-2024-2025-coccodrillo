from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from datetime import datetime
import random
from hotel import get_nation
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


options = Options()
options.headless = True             #true if not want see the browser


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
    


def save_info(driver,city,start,end,sort):
        fp = open("temp.txt","w")
        web = f"https://www.expedia.com/Hotel-Search?destination={city}&endDate={end}&sort={sort}&startDate={start}"
        driver.get(web)
        time.sleep(40)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-stid='property-listing-results']"))
            )
            time.sleep(5)  # Attendi qualche secondo in più per il caricamento completo
        except Exception as e:
            print("Errore durante il caricamento:", e)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        hotels = soup.find_all("div", class_="uitk-spacing uitk-spacing-margin-blockstart-three")
        n = random.randint(3,10)
        number = min(n, len(hotels))
        for i in range(number):
            try:
                name = hotels[i].find("h3", class_="uitk-heading").text.strip()
                rating_tag = hotels[i].find("span", class_="uitk-badge-base-text")
                rating = rating_tag.text.strip() if rating_tag else "N/A"
                link_tag = hotels[i].find("a", class_="uitk-card-link")
                link = "https://www.expedia.com" + link_tag["href"] if link_tag else ""
                fp.write(name+";"+rating+";"+link+"\n")

            except Exception as e:
               continue
        driver.quit()
        fp.close()
        #return  hotels_data

def extract_distances(text):
    # Trova la sezione che inizia con "View in a map"
    match = re.search(r"View in a map\n(.*)", text, re.DOTALL)
    if not match:
        return []

    # Estrai solo la parte dopo "View in a map"
    filtered_text = match.group(1)

    # Rimuove caratteri speciali (es. \u202a e \u202c)
    filtered_text = filtered_text.replace("\u202a", "").replace("\u202c", "")

    # Divide il testo in righe
    lines = filtered_text.split("\n")

    # Filtra solo le righe che contengono nomi di luoghi e distanze
    distances = []
    for i in range(len(lines) - 1):
        name = lines[i].strip()
        distance = lines[i + 1].strip()

        # Controlla che la distanza abbia un formato valido (es. "10 min walk", "9 min drive")
        if re.match(r"^\d+\s\w+\s\w+$", distance):
            distances.append((name, distance))

    # Stampa i risultati
    final = []
    for name, distance in distances:
        if "walk" in distance or "drive" in distance:
            final.append((name,distance))
        else:
            break
    return final


def get_info():
    
    fp = open("temp.txt","r",encoding='utf-8')
    hotels_data = []
    for line in fp:
        record = line.split(";")
        name = record[0]
        rating = record[1]
        link = record[2]    
        distances = {}        
        if link != "":
            driver = webdriver.Firefox(options=options)
            driver.get(link)
            time.sleep(15)
            text = extract_text(driver)
            driver.quit()
            places = extract_distances(text)
            for tupla in places:
                   distances[tupla[0]] = tupla[1]
        hotel_info = {
            "name": name,
            "rating": rating,
            "distances": distances
        }
        print(hotel_info)
        hotels_data.append(hotel_info)
    
    return hotels_data








def run(city,start,end,sort):
    nation = get_nation.get_country(city)
    place = city + " " + nation
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    start = datetime.strptime(start, "%d/%m/%Y").strftime("%Y-%m-%d")
    end = datetime.strptime(end, "%d/%m/%Y").strftime("%Y-%m-%d")
    save_info(driver,place,start,end,sort)
    info = get_info()
    return info


def extract_text(driver):
    try:
        # Aspetta che gli elementi siano presenti
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "uitk-layout-flex"))
        )

        # Trova tutti gli elementi con Selenium
        distances_elements = driver.find_elements(By.CLASS_NAME, "uitk-layout-flex")

        # Estrai il testo da ogni elemento trovato
        distances = [element.text.strip() for element in distances_elements]
        return " ".join(distances)

    except Exception as e:
        return ""







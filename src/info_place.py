from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import random
import query_bert
import re

def extract_lat_long(text):
    # Trova tutte le stringhe numeriche (numeri con decimali)
    numbers = re.findall(r"-?\d+\.\d+", text)
    
    # Se ci sono almeno due numeri, possiamo assumere che siano latitudine e longitudine
    if len(numbers) >= 2:
        lat = numbers[0]
        long = numbers[1]
        return lat, long
    else:
        print("Non sono riuscito a trovare latitudine e longitudine.")
        return 0, 0


def run(name):
    options = Options()
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.5735.90 Safari/537.36")
    options.headless = False  # Imposta a True se non vuoi che si apra la finestra del browser
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    # Crea l'URL di ricerca su DuckDuckGo
    driver.get(f"https://duckduckgo.com/?q={name}+lat+e+long&t=h_&ia=web&assist=true")
    time.sleep(random.uniform(15, 20))  # Attendere che la pagina carichi
    lat = 0
    long = 0
    try:
        # Trova l'elemento che contiene il testo con i dati di latitudine e longitudine
        element = driver.find_element(By.CSS_SELECTOR, '.VrBPSncUavA1d7C9kAc5.FQ2XxQQbwcMwCtbtebpY')

        # Estrai il testo dell'elemento
        text = element.text

        # Usa la funzione per estrarre latitudine e longitudine
        lat, long = extract_lat_long(text)

    except Exception as e:
        driver.get(f"https://duckduckgo.com/?q={name}+lat+e+long&t=h_&ia=web&assist=true")
        time.sleep(random.uniform(2, 5))  # Attendere che la pagina carichi
        try:
            # Trova l'elemento che contiene il testo con i dati di latitudine e longitudine
            element = driver.find_element(By.CSS_SELECTOR, '.VrBPSncUavA1d7C9kAc5.FQ2XxQQbwcMwCtbtebpY')

            # Estrai il testo dell'elemento
            text = element.text

            # Usa la funzione per estrarre latitudine e longitudine
            lat, long = extract_lat_long(text)
        except:
            print(f"Errore durante l'estrazione dei dati: {e}")
   
    driver.get(f"https://duckduckgo.com/?t=h_&q={name}+duration+visit&ia=web&assist=true")
    time.sleep(random.uniform(15, 20))  # Attendere che la pagina carichi
    try:
        # Trova l'elemento che contiene il testo con i dati di latitudine e longitudine
        element = driver.find_element(By.CSS_SELECTOR, '.VrBPSncUavA1d7C9kAc5.FQ2XxQQbwcMwCtbtebpY')

        # Estrai il testo dell'elemento
        text = element.text
        #chiedo a bert duration visit leggendo questo
        duration = query_bert.ask_model(text,"Duration visit?")[0]
        driver.quit()
        return lat,long,duration

    except Exception as e:
        driver.quit()
        return lat,long,0

    

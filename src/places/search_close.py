from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions as ec
import time
from bs4 import BeautifulSoup
import random
import re






def cookie(driver):
    driver.maximize_window()       # ingrandisce la finestra
    WebDriverWait(driver, 10).until( # aspetta finche il bottone è cliccabile e poi lo clicca
        ec.element_to_be_clickable(
        (
            By.XPATH,
            '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button'
        )
    )).click()




def check_closed(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    text = re.sub(r'\s+', '', soup.text.lower())
    if "chiusotemporaneamente" in text or "closedtemporarily" in text or "temporarilyclosed"  in text or  "temporaneamentechiuso"  in text:
        return 0
    else:
        return 1



def search_museum(name,driver):
    # Trova il campo di ricerca (basato su quello che vedo nel tuo screenshot: name="q")
    search_box = driver.find_element(By.NAME, "q")
    search_box.clear()
    # Scrivi la query
    search_box.send_keys(name)

    # Premi INVIO per cercare
    search_box.send_keys(Keys.RETURN)

    # Aggiungi un ritardo per dare tempo a Google Maps di mostrare i risultati
    time.sleep(random.uniform(5, 7))


def wait_for_details(driver):
    try:
        # Aspetta che compaia il titolo del luogo (puoi modificare con un altro selettore)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1')))
    except Exception as e:
        print("Dettagli non caricati:", e)



def run(name):
    options = Options()
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.5735.90 Safari/537.36")
    options.headless = False
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.google.pl/maps/place/")
    time.sleep(random.uniform(1, 2))
    cookie(driver)
    time.sleep(1)
    search_museum(name,driver)
    wait_for_details(driver)
    open = check_closed(driver)
    return open




def run_vector(places):
    vector = []
    if len(places) != 0:
        options = Options()
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.5735.90 Safari/537.36")
        options.headless = False
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://www.google.pl/maps/place/")
        time.sleep(random.uniform(1, 2))
        cookie(driver)
        for place in places:
            search_museum(place,driver)
            wait_for_details(driver)
            open = check_closed(driver)
            vector.append((place,str(open)))
    
    return vector



from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

from urllib.parse import urlencode, parse_qs, urlparse

def cookie(driver):
        try:
            accept_cookies = driver.find_element(By.ID, "onetrust-accept-btn-handler")
            accept_cookies.click()
        except:
            pass



def change_time(url,start):

    # Parse the URL and get the query parameters,
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    # Replace the dates with new values
    query_params['outwardDate'] = [start]
    #query_params['inwardDate'] = [end]

    # Rebuild the URL with the updated query parameters
    new_query = urlencode(query_params, doseq=True)
    new_url = parsed_url._replace(query=new_query).geturl()
    return new_url



def get_ticket(start,end,time_start,tipo):
    web = "https://www.thetrainline.com/"
    options = Options()
    options.headless = True
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    #driver.minimize_window()
    driver.get(web)
    time.sleep(5)
    cookie(driver)
    # Wait for the page to load
    wait = WebDriverWait(driver, 10)
    prices = []
    biglietti = []
    try:
        # Locate the input fields for the origin and destination
        parteza = wait.until(EC.presence_of_element_located((By.ID, "jsf-origin-input")))
        arrivo = wait.until(EC.presence_of_element_located((By.ID, "jsf-destination-input")))
        
        # Clear the fields with JavaScript to ensure it's cleared
        driver.execute_script("arguments[0].value = '';", parteza)
        driver.execute_script("arguments[0].value = '';", arrivo)
        time.sleep(5)
        # Simulate typing the cities and press "Enter"
        start = start + " (Any)"
        end = end + " (Any)"
        parteza.send_keys(start)
        time.sleep(2)
        parteza.send_keys(Keys.RETURN)
        arrivo.send_keys(end)
        # Wait for suggestions to load, if needed (e.g., press backspace to clear suggestions)
        time.sleep(1)
        # Simulate pressing the "Enter" key to submit (or interact with suggestions)
        arrivo.send_keys(Keys.RETURN)
        #ritorno = wait.until(EC.presence_of_element_located((By.ID, "return")))
        #ritorno.send_keys(Keys.RETURN)
        # Wait for results or further actions (if necessary)
        time.sleep(1)
        element2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ij0QOYehWsFFE0Wct06k")))  # Adjust class name if needed
        time.sleep(1)
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "TxiNhQMRe627x_m6sjmD")))  # Adjust class name if needed
        element2.click()
        time.sleep(1)
        # Click the element (if it's a clickable element)
        element.click()
        time.sleep(15)   #diamo  il tempo di  caricare        
        new_url = change_time(driver.current_url,time_start)
        ##poi cerco i biglietti migliori
        driver.get(new_url)
        time.sleep(7)   #diamo  il tempo di  caricare
        cookie(driver)
        time.sleep(5)   #diamo  il tempo di  caricare
        #volendo posso controllare treni e pulmman
        #input id train o input id coach
        tipo_button = driver.find_element(By.ID, tipo)
        tipo_button.click()
        time.sleep(15)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        # Trova tutte le sezioni dei risultati dei treni
        results = soup.find_all("div", class_="_5l6ub9")
        i = 0
        enter = 0
        while 1:    #da capire quando fermare il ciclo e poi prendere il prezzo ed eventualmente per classi
                    #cioe capire come collegare boh e boh2 con i prezz,altrimenti li levo
            if i == 0:
                dep_time = results[0].find("span", {"class": "_1eil35u"}).text.strip()
            else:
                dep_time = results[0].find_all("span", {"class": "_1eil35u"})[i].text.strip()
            i += 1
            arr_time = results[0].find_all("span", {"class": "_1eil35u"})[i].text.strip()
            i += 1
            duration = results[0].find_all("span", {"class": "_1eil35u"})[i].text.strip()
            i += 1
            boh  = results[0].find_all("span", {"class": "_1eil35u"})[i].text.strip()
            i += 1
            boh2  = results[0].find_all("span", {"class": "_1eil35u"})[i].text.strip()
            if enter == 0:
                enter = 1
                price = soup.find_all("div", class_="_1e867qro")
                
                for div in price:
                    # Cerca i div che contengono il prezzo per il biglietto standard e di prima classe
                    standard_price = div.find("div", {"data-test": lambda x: x and 'standard-ticket-price' in x})
                    first_class_price = div.find("div", {"data-test": lambda x: x and 'first-class-ticket-price' in x})

                    # Se è stato trovato un prezzo, aggiungilo alla lista
                    if standard_price:
                        price = standard_price.find("span").text.strip()
                        prices.append(price)
                    if first_class_price:
                        price = first_class_price.find("span").text.strip()
                        prices.append(price)

            i+=3
            
            biglietti.append({
                'departure': dep_time,
                'arrive': arr_time,
                'duration':duration
            })
    except Exception as e:
        k = 0
        for j in range(len(biglietti)):
            try:
                biglietti[j]['std_class'] = prices[k]
                k+=1
                biglietti[j]['first_class'] = prices[k]
                k +=1
            except:
                break
    driver.quit()
    return biglietti



def get_all_ticket(start,end,time_start,time_end):
    diz = {}
    diz['train'] = dict()
    andata = get_ticket(start,end,time_start,'train')
    ritorno = get_ticket(end,start,time_end,'train')
    diz['train']['andata'] = andata
    diz['train']['ritorno'] = ritorno
    diz['coach'] = dict()
    andata = get_ticket(start,end,time_start,'coach')
    ritorno = get_ticket(end,start,time_end,'coach')
    diz['coach']['andata'] = andata
    diz['coach']['ritorno'] = ritorno
    return diz



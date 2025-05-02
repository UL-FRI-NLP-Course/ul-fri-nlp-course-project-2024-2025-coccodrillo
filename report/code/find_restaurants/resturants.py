from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def extract_items(driver):
    start = 0
    restaurant_list = []
    while True:
        elements = driver.find_elements(By.CLASS_NAME, 'y-css-snigah')
        if elements == [] or start > 30:
            break
        for element in elements:
            restaurant = {}  # Ogni ristorante è un dizionario vuoto
            try:
                name = element.find_element(By.XPATH, './/a').text
            except:
                name = ""  # Se non trova il nome, assegna una stringa vuota
            restaurant["Name"] = name

            try:
                location = element.find_element(By.CLASS_NAME, 'y-css-yvhxeq').text
            except:
                location = ""  # Se non trova la location, assegna una stringa vuota
            restaurant["Location"] = location

            try:
                reviews = element.find_element(By.CLASS_NAME, 'y-css-f73en8').text
            except:
                reviews = ""  # Se non trova le recensioni, assegna una stringa vuota
            restaurant["Reviews"] = reviews
            
            restaurant_list.append(restaurant)



        current_url = driver.current_url
        start+=10
        try:
            index_position = current_url.index("start=")
        except:
            current_url += "&start=" + str(start)
            index_position = current_url.index("start=")
        new_url = current_url[:index_position + 6] + str(start)
        driver.get(new_url)
        time.sleep(3)
    return restaurant_list









def get_restaurants(city):
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=service, options=options)
    driver.minimize_window()
    web = f"https://www.yelp.ie/search?find_desc=Restaurants&find_loc={city}"
    driver.get(web)
    time.sleep(3)
    #search_description = driver.find_element(By.XPATH, '//input[@id="search_description"]')
    #search_description.send_keys("Restaurants")
    #search_description.send_keys(Keys.RETURN)
    #time.sleep(5)
    #search_location = driver.find_element(By.XPATH, '//input[@id="search_location"]')
    #search_location.clear()
    #search_location.send_keys(city)
    #search_location.send_keys(Keys.RETURN)
    #time.sleep(2)
    restaurants = extract_items(driver)
    driver.quit()
    return restaurants



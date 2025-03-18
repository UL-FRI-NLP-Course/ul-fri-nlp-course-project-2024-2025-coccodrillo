from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re  
import requests
from bs4 import BeautifulSoup





def naviga(web,citta,data_start,data_end,genere):
    
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


def get_events(html):
    output = ""
    soup = BeautifulSoup(html, 'lxml')
    events = soup.find_all('a', class_='HsqHp2xM2FkfSdjy1mlU')
    for event in events:
        event_name = event.find('div', class_='_5CQoAbgUFZI3p33kRVk').text.strip()
        description = event.find('div', class_='bqB5zhZmpkzqQcKohzfB').text.strip()
        date_time = event.find('div', class_='r593Wuo4miYix9siDdTP').text.strip()
        output += f"Event Name: {event_name}"   + "\n" \
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
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find_all('div', class_='MtafMVpvYyCTdxtbFglz')
    table = str(table)
    html = table[1:-1]
    return html

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

start = "2025-03-20"
end = "2025-03-21"
citta = "Rome"


geckodriver_path = "geckodriver"  
options = Options()
options.headless = False                     #true if not want see the browser
driver = webdriver.Firefox(options=options)

web = "https://www.bandsintown.com/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
    

pagina_html = naviga(web,citta,start,end,gen[-2])
table = get_tables(pagina_html)
events = get_events(table)
fp = open("events.txt","w")
fp.write(events)
fp.close()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time

def extract_items():
    global fp
    start = 0
    while True:
        elements = driver.find_elements(By.CLASS_NAME, 'y-css-snigah')
        if elements == []:
            break
        for element in elements:
            try:
                output = ""
                name = element.find_element(By.XPATH, './/a').text
                output += f"Name: {name}" +"\n"
                location = element.find_element(By.CLASS_NAME, 'y-css-4p5f5z').text
                output += f"Location: {location}" +"\n"
                reviews = element.find_element(By.CLASS_NAME, 'y-css-1ugd8yy').text
                output += f"Reviews: {reviews}" +"\n"
                output += '-' * 40 +"\n"
                fp.write(output)

            except Exception as e:
                continue

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
        


citta = "roma"
path = citta + "_restaurants.txt"
fp = open(path,"w")
options = Options()
options.headless = True 
driver = webdriver.Firefox(options=options)
web = "https://www.yelp.com/"
driver.get(web)
time.sleep(3)
search_description = driver.find_element(By.XPATH, '//input[@id="search_description"]')
search_description.send_keys("Restaurants")
search_description.send_keys(Keys.RETURN)
time.sleep(5)
search_location = driver.find_element(By.XPATH, '//input[@id="search_location"]')
search_location.send_keys(citta)
search_location.send_keys(Keys.RETURN)
time.sleep(2)
extract_items()

driver.quit()
fp.close()



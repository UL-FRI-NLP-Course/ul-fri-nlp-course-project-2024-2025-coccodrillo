from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests



def get_acronym_from_file(nation):
    with open("dataset/countries.txt", "r") as file:
        for line in file:
            country, acronym = line.strip().split('=')
            if country.lower() == nation.lower():
                return acronym
    return None  

def get_paper(nation):
    acronym = get_acronym_from_file(nation)
    if acronym:
        url = f"https://www.viaggiaresicuri.it/schede_paese/pdf/{acronym}.pdf"
        response = requests.get(url)
        if response.status_code == 200:
            with open(f"result/{nation}_paper.pdf", "wb") as file:
                file.write(response.content)
            return 1
        else:
            return -1
    else:
        return -1


def download_acronimi():
    url = "https://www.viaggiaresicuri.it/find-country"
    driver = webdriver.Firefox()
    driver.set_window_size(1920, 1080)
    driver.get(url)
    time.sleep(2)
    with open("nations.txt", "w") as file:
        while True: 
            flags = driver.find_elements(By.CSS_SELECTOR, "a.cursor-pointer")
            for index in range(len(flags)):
                try:
                    flags = driver.find_elements(By.CSS_SELECTOR, "a.cursor-pointer")
                    flag = flags[index]  
                    country_name = flag.find_element(By.CSS_SELECTOR, ".country_name").text.strip()
                    driver.execute_script("arguments[0].click();", flag)
                    time.sleep(0.75) 
                    current_url = driver.current_url
                    file.write(current_url[-3:] + "\n")
                    driver.back()
                    time.sleep(2)  
                except Exception as e:
                    print(f" Error {country_name}: {e}")
            break  



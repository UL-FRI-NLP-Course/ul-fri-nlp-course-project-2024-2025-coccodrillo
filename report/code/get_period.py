import extract_date
import check_similarity
import spacy
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import re




geckodriver_path = "geckodriver" 
nlp = spacy.load("en_core_web_sm")

def search_dates(stringa):
    firefox_options = Options()
    firefox_options.add_argument("--headless")  # Esegui in modalità headless (senza GUI)
    # Avvia il WebDriver di Firefox
    driver = webdriver.Firefox(executable_path=geckodriver_path, options=firefox_options)
    # Visita l'URL
    driver.get(f"https://duckduckgo.com/?q={stringa}+date&t=h_&ia=web")
    time.sleep(3.5)
    try:
        # Trova l'elemento usando la classe fornita
        element = driver.find_element(By.CSS_SELECTOR, '.VrBPSncUavA1d7C9kAc5.FQ2XxQQbwcMwCtbtebpY')
        # Estrai il testo dell'elemento
        text = element.text
        v  = extract_date.get_dates(text)
        v2 = []
        for element in v:
            if not re.match("^[a-zA-Z\s]*$", element):
                v2.append(element)
        return v2
    except Exception as e:
        return []


def get_date(first,second):    
    doc = nlp(first)
    vector_date = []
    date_regex = r'\b(\d{1,2})\s*[\/\-]\s*(\d{1,2})\s*[\/\-]\s*(\d{2,4})\b'
    for ent in doc:
            if not ent.is_stop:
                p = check_similarity.get_best_period(ent.text)
                if p != None:
                    vector_date.append(p)
                else:
                    vector_date.append(ent.text)
    if vector_date != []:
        v = extract_date.get_dates(" ".join(vector_date))
        #da qui devono uscire per forza date numeriche, se non sono uscite numeriche le butto
        v_new = []
        for data in v:
             if re.match(date_regex, data):
                  v_new.append(data)
        v = v_new
        if v != []:
            A_diff = list(set(vector_date) - set(v))
            return A_diff,v
         
    doc2 = nlp(second)
    for ent in doc2:
            if not ent.is_stop:
                p = check_similarity.get_best_period(ent.text)
                if p != None:
                    vector_date.append(p)
                else:
                    vector_date.append(ent.text)
    
    v = extract_date.get_dates(" ".join(vector_date))
    v_new = []
    for data in v:
            if re.match(date_regex, data):
                v_new.append(data)
    v = v_new
    A_diff = list(set(vector_date) - set(v))
    return A_diff,v




def get_period_dictionary(first,second):
    to_analize,complete = get_date(first,second)   #get date non mi da la data per friday!
    diz = {}
    diz['dates'] = []
    to_analize = " ".join(to_analize)
    to_analize = nlp(to_analize)
    for element in to_analize:   #devo rimuovere le stopword
            if re.match("^[a-zA-Z\s]*$", element.text) and not element.is_stop:
                values = search_dates(element.text)
                if values != []:
                    diz[element.text] = values
    for element in complete:
            diz["dates"].append(element)
    return diz







     
#print(extract_date.get_dates("hello i sleep today, tomorrow, friday and next week and 19/04/2004 from 18/03/2000 to 19/03/2001"))




'''
1. Opere in ristrutturazione
    Cerca: "[nome della città] renovation works" 

2. Eventi di emergenza (guerre, conflitti)
    "security situation [nome della città]"

3. Catastrofi naturali o meteo estremo
    Cerca: "severe weather warning [nome della città]".


4. Eventi locali o manifestazioni
    Cerca: "local events [nome della città]"

5. Situazione sanitaria (pandemie o emergenze sanitarie)
    Cerca: "health situation [nome della città]" 

7. Situazioni politiche locali
    Cerca: "political situation [nome della città]" o "strikes protests [nome della città]".
'''

from bs4 import BeautifulSoup
import requests




def get_url_articles(stringa):
     url = f"https://www.bing.com/news/search?q={stringa}"
     return url



def get_articles(stringa, num_doc):
    url = get_url_articles(stringa)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    container = soup.find(class_="content-refresh-container")  
    ls_link = []
    if container:
        articles = container.find_all('div', class_='news-card newsitem cardcommon')
        doc = min(num_doc, len(articles))
        for i in range(doc):
            article = articles[i]
            link = article.get('data-url') 
            if not link:  
                a_tag = article.find('a', class_='title')
                if a_tag:
                    link = a_tag.get('href')
            if link:
                ls_link.append(link)
        return ls_link
         
    else:
        return []


l = get_articles("severe weather warning florence",3)
print(l)




from bs4 import BeautifulSoup
import requests
import random
from news import topic_analysis
from news import get_nation
from news import viaggiare_sicuri
from transformers import pipeline, BartTokenizer
import translate



origin="en"


             

def summarize_text(text, max_length=150, min_length=50):
    try:
        # Inizializzare il summarizer con il modello preaddestrato BART
        summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
        tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')  # Tokenizer per BART
        
        # Tokenizza il testo e calcola la lunghezza dei token
        input_ids = tokenizer.encode(text, return_tensors='pt', truncation=True)  # Tronca se supera il limite di token
        
        input_length = len(input_ids[0])  # Lunghezza dei token
        
        # Se l'input è più breve di un certo numero di parole, riduci max_length
        if input_length <= 50:  # Se il testo è piuttosto breve
            max_length = min(max_length, input_length // 2)  # Riduci max_length
        elif input_length <= 100:
            max_length = min(max_length, input_length)  # Riduci max_length ma non meno del 50% dell'input
        
        # Suddividere il testo in porzioni più piccole se è troppo lungo
        max_token_length = 1024  # Limite massimo di token per BART
        if input_length > max_token_length:  # Se il testo è più lungo dei limiti di BART
            # Dividi il testo in blocchi più piccoli per evitare il limite dei token
            chunk_size = max_token_length  # Dimensione del chunk in base ai token
            chunks = [input_ids[0][i:i + chunk_size] for i in range(0, input_length, chunk_size)]  # Chunking basato sui token
            
            # Riassumi ogni blocco separatamente
            summaries = []
            for chunk in chunks:
                chunk_text = tokenizer.decode(chunk, skip_special_tokens=True)  # Decodifica i token in testo
                summary = summarizer(chunk_text, max_length=max_length, min_length=min_length, do_sample=False)
                summaries.append(summary[0]['summary_text'])
            
            # Unisci i riassunti dei singoli blocchi
            return ' '.join(summaries)
        else:
            # Se il testo non è troppo lungo, esegui il riassunto direttamente
            summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            return summary[0]['summary_text']
    except:
        return text


translations = {
    "0": {
        "United Kingdom": ("security situation","en"),
        "Italia": ("situazione di sicurezza","it"),
        "France": ("situation de sécurité","fr"),
        "España": ("situación de seguridad","es")
    },
    "1": {
        "United Kingdom": ("severe weather warning","en"),
        "Italia": ("avviso di maltempo","it"),
        "France": ("avertissement de mauvais temps","fr"),
        "España": ("advertencia de mal tiempo","es")
    }
}



def get_url_articles(stringa):
     url = f"https://www.bing.com/news/search?q={stringa}"
     return url


def search(stringa, num_doc):
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
        return ls_link,stringa
         
    else:
        return [],""



def get_articles(places,intent):
    global origin
    nation = get_nation.get_country(places)
    if nation in translations[intent]:
        value = translations[intent][nation][0]
        origin = translations[intent][nation][1]
    else:
        value = translations[intent]['United Kingdom']
        origin = "en"
    n = random.randint(4,8)
    value = value + " "+ places
    articles,stringa = search(value,n)
    return articles,stringa




def read_articles(ls_articles):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edge/91.0.864.59"
    }
    output = []
    for article in ls_articles:
        try:
            response = requests.get(article, headers=headers, timeout=10)  
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                paragraphs = soup.find_all('p')
                # Trova la data di pubblicazione (vari tentativi)
                date_tag = soup.find('time')
                if not date_tag:
                    date_tag = soup.find('span', class_=lambda c: c and 'date' in c.lower())
                if not date_tag:
                    date_tag = soup.find('div', class_=lambda c: c and 'date' in c.lower())

                date = date_tag.get_text().strip() if date_tag else ''
                text = ' '.join([para.get_text() for para in paragraphs])
                if text != "" and text != " ":
                    output.append(date +"?!?"+text)

                else:
                    continue
               
            else:
                continue
        except requests.exceptions.RequestException as e:
            continue
    return output



def run(places,intent):
    articles,stringa = get_articles(places,intent)
    output = read_articles(articles)
    output = topic_analysis.get_real_articles(output,stringa)
    new_output = []
    for text in output:
        data = text.split("?!?")[0]
        testo = text.split("?!?")[1]
        summarize = summarize_text(testo)
        summarize = data +"\n"+testo
        if origin != "en" and summarize != "":
            summarize = translate.get_translate(summarize,origin,"en")
        if summarize != "":
            new_output.append(summarize)

    return new_output




def get_nat(city):
    nation = get_nation.get_country(city)
    return nation


def get_paper(nation):
    s = viaggiare_sicuri.get_paper(nation)
    return s



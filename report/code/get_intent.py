from sentence_transformers import SentenceTransformer, util
import spacy
import json
import check_similarity



nlp = spacy.load("en_core_web_sm")
geckodriver_path = "geckodriver" 
# Modello SBERT pre-addestrato (puoi cambiarlo con un altro più potente)
model = SentenceTransformer('all-MiniLM-L6-v2')


INTENTS = []

# Define the function to load the files
def load_file():
    global INTENTS
    try:
        with open('intents.json', 'r') as intents_file:
            INTENTS = json.load(intents_file)
    except FileNotFoundError:
        print("intents.json file not found")
    except json.JSONDecodeError:
        print("Error decoding intents.json file")


def associa_citta_giorni(lista_citta, lista_giorni):

    index_city = 0
    index_giorni = 0
    associations = []
    if lista_giorni == []:
        for element in lista_citta:
            associations.append((element[0].capitalize(),''))
        return associations
    if lista_citta == []:
        for element in lista_giorni:
            associations.append(('',element[0].capitalize()))
        return associations
    city_current = lista_citta[index_city]
    period_current = lista_giorni[index_giorni]
    
    while 1:
        if city_current[1] < period_current[1]:
            try:
                if lista_citta[index_city+1][1] >  period_current[1]:
                    associations.append((city_current[0].capitalize(), period_current[0].capitalize()))
                    index_giorni+=1
                    period_current = lista_giorni[index_giorni]
                elif lista_citta[index_city+1][1] <  period_current[1]:
                    index_city = index_city+1
                    associations.append((lista_citta[index_city][0].capitalize(), period_current[0].capitalize()))
                    city_current = lista_citta[index_city]
            except:
                 #le citta sono finite quindi continuo fino alla fine dei peridi,ma l'ho messa quella che sto analizzando?
                 associations.append((lista_citta[index_city][0].capitalize(), period_current[0].capitalize()))
                 try:
                    index_giorni+=1
                    period_current = lista_giorni[index_giorni]
                    if city_current[1] < period_current[1]:
                        associations.append((lista_citta[index_city][0].capitalize(), period_current[0].capitalize()))
                    else:
                        break
                 except:
                    break
        else:
            associations.append((city_current[0].capitalize(), period_current[0].capitalize()))
            try:
                index_giorni+=1
                period_current = lista_giorni[index_giorni]
            except:
                break
    association_new = []
    for i in range(len(associations)-1):
            if associations[i][1] != associations[i+1][1]:
                association_new.append(associations[i])
    if len(associations) > 0:
        association_new.append(associations[-1])
    return association_new



def get_intent(sentence):
    embeddings_labels = model.encode(INTENTS, convert_to_tensor=True)
    embedding_input = model.encode(sentence, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(embedding_input, embeddings_labels)
    best_match_idx = similarities.argmax().item()
    best_match = INTENTS[best_match_idx]
    return best_match


def get_info(sentence):
    tokens = nlp(sentence)
    cities = []
    periods = []
    remains = []
    i = 0
    for token in tokens:
        if not token.is_stop and not token.text.isdigit() and not token.text.lower() == "day" and not token.text.lower() == "days":
               if token.ent_type_ == "GPE":
                   cities.append((token.text,i))
               elif token.ent_type_ == "DATE" or token.ent_type_ == "TIME" or token.ent_type_ == "EVENT":
                    periods.append((token.text,i))
               elif token.pos_ == "VERB":
                   continue
               else:
                   remains.append((token.text,i))
        i += 1
    for element in remains:
        is_city = check_similarity.get_best_city(element[0])
        if is_city == None:
            is_period = check_similarity.get_best_period(element[0])
            if is_period != None:
                periods.append((is_period,element[1]))
        else:
            cities.append((is_city,element[1]))

    cities = sorted(cities, key=lambda x: x[1])
    periods = sorted(periods,key=lambda x:x[1])
    associations= associa_citta_giorni(cities,periods)
    return associations,cities

def main(sentence):
    load_file()
    intent = get_intent(sentence)
    associations,cities = get_info(sentence)  
    #ora devo convertire ogni periodo in una data precisa e poi faccio un check 
    #intent 0,1,2,4,5 il periodo non mi serve
    if INTENTS.index(intent) == 0 or INTENTS.index(intent) == 1 or INTENTS.index(intent) == 4 or INTENTS.index(intent) == 5:
        new_association = []
        for associaton in associations:
            record = (associaton[0].capitalize(),"")
            new_association.append(record)
        return new_association,INTENTS.index(intent)
    #mi serve solo per intent 3, 6, 7, 8 
    #diciamo che ognuno di questi puo avere uno o due periodi 
    #places tutti possono avere 1 o piu place ma intent 7 ne puo avere solo 2
    #se intent 7 trovo solo un posto in realtà può esserci il caso che l'ho perso quindi faccio un piccolo re-check
    if INTENTS.index(intent) == 7:
        #controllo che ci sono solo due citta
        new_association = []
        city = []
        for element in associations:
            if element[0] not in city:
                city.append(element[0])
                new_association.append(element)
        if len(new_association) < 2:
            if len(cities) < 2:
                return None,INTENTS.index(intent)
            else:
                cities = cities[:2]   #ci sono due citta dentro cities
                ass = []
                if len(new_association) == 1:   #devo capire se la citta è la prima di cities o la seconda
                    city_first = new_association[0][0]
                    if city_first == cities[0][0]:
                        ass.append((cities[0][0].capitalize(),new_association[0][1])) 
                        ass.append((cities[1][0],"")) 
                    else:
                         ass.append((cities[0][0].capitalize(),"")) 
                         ass.append((cities[1][0].capitalize(),new_association[0][1])) 
                else:
                    ass.append((cities[0][0].capitalize(),"")) 
                    ass.append((cities[1][0].capitalize(),"")) 
                         
                return ass,INTENTS.index(intent)
        else:
            new_association = new_association[:2]
            return new_association,INTENTS.index(intent)
    else:
        return associations,INTENTS.index(intent)
    


int = [
    "security situation",
    "warnings and alerts",
    "places to visit",
    "concerts and event",
    "best restaurants",
    "typical food",
    "future weather",
    "travel"
]


def get_name(index):
    return int[index]
import get_intent
import create_graph_place
import query_bert
import re
from weather import get_prevision
import convert_date
import get_food
from events import get_events
from datetime import datetime
from find_restaurants import resturants
import get_news
import check_similarity
import read_pdf
import travel
from places import search_close
from places import get_geo
import create_text
import format_output


sentence = ""
metadata = None

def change_time(stringa):
    date_obj = datetime.strptime(stringa, "%d/%m/%Y")
    date_with_time = date_obj.replace(hour=8, minute=0, second=0)
    formatted_date = date_with_time.strftime("%Y-%m-%dT%H:%M:%S")

    return formatted_date


def get_days(stringa):
    # Cerca il primo numero nella stringa usando una regular expression
    match = re.search(r'\d+', stringa)
    
    # Se c'è un numero, restituisce il numero come intero, altrimenti restituisce 0
    if match:
        return int(match.group())
    else:
        return 0
    

def get_intent2():
    n_day = query_bert.ask_model(sentence,"How much day?")[0]
    n_day = get_days(n_day)
    diz = {}
    for record in metadata:
        city = record[0]
        period = record[1]
        if city not in diz:
            importance_time_visit= 0.0
            importance_beauty = 0.7
            importance_edge = 0.3
            address = input("Where is your initial point?Train Station?Address? write your initial point: ")
            lat,long = get_geo.get_lat_long_from_place(address)
            try:
                nodo_start = get_geo.get_nodo_closest(lat,long,city.lower())
            except:
                nodo_start = 0
            place,name,hours = create_graph_place.run(city.lower(),importance_time_visit,importance_beauty,importance_edge,nodo_start,n_day)
            places = [name[i] for i in place]
            diz[city] = (places,hours)

    for city,values in diz.items():
        h = values[1]
        places = values[0]
        places_new = search_close.run_vector(places)
        diz[city] = (places_new,h)

    return diz



def get_intent3():
    diz = {}
    tupla = query_bert.ask_model(sentence,"What is the name of the singer?")
    singer = tupla[0]
    probability = tupla[1]
    singer = singer.split()[0].capitalize()
    if probability < 0.85:
        singer = ""
    gen = query_bert.ask_model(sentence,"What is the genres?")[0]
    gen = check_similarity.get_genres(gen)
    if gen == "":
        gen = 'all-genres'
    cities = []
    #all_gen = check_similarity.get_all_gen()
    for record in metadata:
        city = record[0]
        if city not in cities:
            cities.append(city)
            diz[city] = []
    for city in cities:
        filterd = get_events.filter_city_period(city,metadata)
        for i in range(0, len(filterd), 2):  # Cicla di due in due
            start = filterd[i][1]
            start = convert_date.extract_date_from_text(start)
            if i == len(filterd)-1:
                end = filterd[i][1]
            else:
                end = filterd[i+1][1]
            end = convert_date.extract_date_from_text(end)
            #se sono vuoti devo dire che non ho capito per quando cercare
            if end == "" and start != "":
                end = start
            if start == "" and end !="":
                start = end
            elif end == "" and start == "":
                diz[city].append("period_not_found")
            else:
                events = get_events.search_event_singer(start,end,city,singer,gen)
                diz[city].append(events)
    return diz


def get_intent4():
    cities = []
    diz = {}
    for record in metadata:
        if record[0] not in cities and record[0] != "":
            cities.append(record[0])
            diz[record[0]] = resturants.get_restaurants(record[0])   
    return diz

def get_intent5():
    diz = {}
    for record in metadata:
        city = record[0]
        if city != "":
            if city not in diz:
                dishes = get_food.get_best_food(city)
                diz[city] = dishes
            
    return diz

def get_intent6():
    diz = {}
    for record in metadata:
        city = record[0]
        if city != "":
            data = convert_date.extract_date_from_text(record[1])
            #vedere se specifica nella mattina pomeriggio etc o tutto il giorno
            if data != "" and convert_date.is_near(data):
                previsioni = get_prevision.get_prevsioni_day_time(city,data,"all_day")
                if city not in diz:
                    diz[city] = [previsioni]
                else:
                    diz[city].append(previsioni)
    return diz

def get_intent1():
    cities = []
    diz = {}
    for record in metadata:
        if record[0] not in cities:
            cities.append(record[0])
            articles =get_news.run(record[0],"1")
            diz[record[0]] = articles
    return diz


def get_intent0():
    cities = []
    diz = {}
    nat_visited = set()
    for record in metadata:
        if record[0] not in cities:
            cities.append(record[0])
            articles =get_news.run(record[0],"0")
            diz[record[0]] = articles
            nation = get_news.get_nat(record[0]).lower()
            if nation not in nat_visited:
                nat_visited.add(nation)
                s = get_news.get_paper(nation)
                if s == 1:
                    tupla = read_pdf.summerize("./result/"+nation+"_paper.pdf")
                    diz[nation+"_doc"] = tupla

    return diz


def get_intent7():
    if metadata == None:
        return {}
    else:
        start = metadata[0][0]
        end = metadata[1][0]
        period_start = metadata[0][1]
        period_end = metadata[1][1]
        if period_start != "" and period_end !="":
            period_start = convert_date.extract_date_from_text(period_start)
            period_end = convert_date.extract_date_from_text(period_end)
            if period_start != "" and period_end !="":
                time_start = change_time(period_start)
                time_end = change_time(period_end)
                ticket = travel.get_all_ticket(start,end,time_start,time_end)

            else:
                #i periodi ci sono ma non sono riuscito a trasformarli quindi posso chiedere tipo
                print("Cosa intendi per period_start o period_end?")
                return {}
        else:
            return {}
    #devo filtrarlo ed eliminare quelli che hanno cose strane come departure o arrive non un orario, etc...
    return ticket





# Mappa gli idx_intent ai rispettivi metodi
# Fondamentlae: gestione errori, il programma può creashare da un momento all'altro, può chiedermi se sono un bot, puo non prendere la connessione
# in questi e in altri casi devo gestirlo
intent_mapping = {
    0: get_intent0,   #news work e gestione errori sembra ok 
    1: get_intent1,   #news work e gestione errori sembra ok 
    2: get_intent2,   #place to visit, work e gestione degli errori sembra ok (si vede interfaccia grafica MAPS)
    3: get_intent3,   #concert work work,  gestione errori sembra ok se metto nazione invece che city ti trova la prima cosa simile al nome nazione
    4: get_intent4,   #restaurants, work,  gestione errori sembra ok
    5: get_intent5,   #typical food work,  gestione errori sembra ok
    6: get_intent6,   #temperature  work,  gestione errori sembra ok
    7: get_intent7    #travel, funziona ma se metto nazione invece che city ti trova la prima cosa simile al nome nazione, devo inseire dei ritardi perche capisce che sono un bot
}





# TO DO LIST
#  place to visit: dt di ogni city (per ora solo roma)


#  rivedere summerize(potrebbe dare in errore qualche volta, in quel caso se riesco ritorno il testo iniziale)  dovrei averlo fatto 
#  controllare se ci sono erorri quindi testarlo tante volte
#  se va in bug/non prende/capisce che sono un bot devo chiudere tutto e scrivere "Errore riprovare + tardi"
#  sistemare tutti gli output, renderli + user readble
#  cosa succede se scrivo una naizone e non una città?  non crasha?




def main(stringa):
    global sentence
    sentence = stringa
    global metadata
    metadata, idx_intent = get_intent.main(sentence)
    #return idx_intent    #only for intent testing
    #if metadata == None:  #only for error testing
      #  return []         #only for error testing
    #return metadata       #only for error testing
    name_intent = get_intent.get_name(idx_intent)
    text = create_text.genera_frase_bigram(name_intent)
    #print(metadata)
    #print(idx_intent)
    diz = intent_mapping.get(idx_intent, get_intent2)()   #devo mettere un timeout anche qui
    return text,diz,idx_intent
    print(text)
    print(diz)




stringa = input("Insert your sentence: ")
text,diz,id = main(stringa)
print(text)
final_output = format_output.get(diz,int(id))
print(final_output)



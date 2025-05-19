import random
from collections import defaultdict, Counter
#Bi-grams

# Step 1: Dataset
corpus = [
    "hello, here is the information you requested",
    "hi, sending you the details you asked for",
    "hey, this is the information you needed",
    "greetings, providing you the requested details",
    "hello, I’m giving you the information you asked for",
    "hi, here are the details you requested",
    "hey, sharing the information you were asking for",
    "greetings, delivering the information you needed",
    "hello, the requested information is here",
    "hi, sending the details as you asked",
    "hey, here’s what you wanted to know",
    "greetings, here’s the information you were looking for",
    "hello, here are the details you needed",
    "hi, these are the answers you asked for",
    "hey, giving you the information you requested",
    "greetings, sharing the information you asked about",
    "hello, this is the information you asked me for",
    "hi, here’s the requested information",
    "hey, I’m providing the information you needed",
    "greetings, sending you the answers you requested",
    "hello, here’s everything you wanted to know",
    "hi, these are the requested details",
    "hey, delivering the information you asked",
    "greetings, passing you the information you requested",
    "hello, here is the data you needed",
    "hi, sending the details you wanted",
    "hey, these are the details you asked for",
    "greetings, providing the information you asked for",
    "hello, responding with the information you wanted",
    "hi, sharing the information you requested earlier",
    "hey, sending over the requested information",
    "greetings, giving you the details you asked for",
    "hello, I have the information you needed",
    "hi, here’s the information you were looking for",
    "hey, forwarding you the details you requested",
    "greetings, answering with the information you requested",
    "hello, giving you the requested information",
    "hi, here’s the data you asked for",
    "hey, sending you all the information you requested",
    "greetings, here’s the reply to your request",
    "hello, delivering the requested information",
    "hi, passing the information you needed",
    "hey, providing the answers you asked for",
    "greetings, offering the details you requested",
    "hello, responding to your request with these details",
    "hi, forwarding the information you needed",
    "hey, handing over the requested information",
    "greetings, these are the details you asked me for",
    "hello, I’m sending you the requested information",
    "hi, giving you the requested data",
    "hey, offering you the details you asked for",
    "greetings, providing what you asked for",
    "hello, this is the answer to your request",
    "hi, sending you the complete information you asked for",
    "hey, here’s what you requested",
    "greetings, I’m giving you the information you needed",
    "hello, here’s everything you asked for",
    "hi, passing the details you wanted",
    "hey, these are the requested answers",
    "greetings, delivering what you needed",
    "hello, here is what you asked for",
    "hi, giving you all the details you requested",
    "hey, here’s the full information you wanted",
    "greetings, sending you the answers you needed",
    "hello, offering the details you asked for",
    "hi, sharing everything you requested",
    "hey, these are the details you needed",
    "greetings, this is the information you needed",
    "hello, providing you with the answers you requested",
    "hi, sharing with you the requested information",
    "hey, delivering the requested data",
    "greetings, this is what you wanted to know",
    "hello, passing you the information you were asking for",
    "hi, here’s what you needed",
    "hey, responding with the requested information",
    "greetings, sharing the answers you were looking for",
    "hello, I’m giving you the full details you asked for",
    "hi, handing over the information you requested",
    "hey, sending you the information you asked for",
    "greetings, these are the details you were looking for",
    "hello, providing the full information you needed",
    "hi, here’s all the information you requested",
    "hey, offering you the information you needed",
    "greetings, sending over what you requested",
    "hello, providing the details you were asking for",
    "hi, giving you the answers you asked for",
    "hey, this is the data you wanted",
    "greetings, I’m providing you the answers you needed",
    "hello, offering the information you asked for",
    "hi, these are the details you requested earlier",
    "hey, responding to your request with information",
    "greetings, providing you the requested information now",
    "hello, here’s the information you asked for recently",
    "hi, forwarding you the details you needed",
    "hey, sharing with you the requested answers",
    "greetings, delivering you the information you asked for",
]


# Step 2: Tokenizzazione e conteggio bigrammi
bigrams = defaultdict(Counter)

for frase in corpus:
    parole = frase.lower().split()
    for i in range(len(parole) - 1):
        parola_corrente = parole[i]
        parola_successiva = parole[i+1]
        bigrams[parola_corrente][parola_successiva] += 1

# Step 3: Funzione di generazione con inserimento naturale dell'argument
def genera_frase_bigram(argument, max_length=20):
    # Scegli una frase casuale dal corpus
    frase = random.choice(corpus).lower().split()
    
    # Costruisci la frase con bigrammi
    for _ in range(max_length - 1):
        parola = frase[-1]
        if parola not in bigrams or not bigrams[parola]:
            break
        parole_successive = list(bigrams[parola].elements())
        parola_successiva = random.choice(parole_successive)
        frase.append(parola_successiva)
    
    # Inserisci l'argument in modo naturale
    insert_positions = [i for i, word in enumerate(frase) if word in {"information", "details", "answers", "data"}]
    
    if insert_positions:
        pos = random.choice(insert_positions)
        frase.insert(pos + 1, f"about {argument}")
    else:
        # Se non trova punti buoni, aggiungilo alla fine
        frase.append(f"about {argument}")

    frase_finale = ' '.join(frase).capitalize() + "."
    return frase_finale


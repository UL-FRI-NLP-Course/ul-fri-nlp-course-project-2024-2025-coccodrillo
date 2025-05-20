singer = [
    "Blanco",
    "Sfera Ebbasta",
    "Fedez",
    "Salmo",
    "Ultimo",
    "Mara Sattei",
    "Måneskin",  # La band che ha preso d'assalto le classifiche
    "Holly",
    "Lazza",
    "Gianluca Grignani",  # Continua a essere un'icona, ma con nuovi progetti
    "Rkomi",
    "Coez",
    "Lele Blade",
    "Madame",
    "I Cani",  # Seppur meno mainstream, sempre un cult in Italia
    "Mahmood",
    "Anna",  # Cantante emergente molto popolare
    "Ariete",  # Nuova promessa della scena musicale italiana
    "Nina Zilli",  # Nonostante sia un po' più “retro”, continua ad avere un pubblico affezionato
    "Emma Muscat",  # Sempre più affermata nella scena musicale
    "Tananai",  # Aggiungiamo anche qualche nome emergente dalle ultime classifiche
]

import csv



# Creazione del file CSV
filename = "singer.csv"
with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Singer"])  # Intestazione della colonna
    for song in singer:
        writer.writerow([song])

print("CSV file 'singer.csv' has been created.")

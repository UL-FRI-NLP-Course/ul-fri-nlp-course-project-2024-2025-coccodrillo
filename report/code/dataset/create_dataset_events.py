import csv

# Lista di periodi comuni
periods = [
        "New Year",
    "Epiphany",
    "Carnival",
    "Easter",
    "Easter Monday",
    "Labour Day",
    "Republic Day",
    "St. John's Day",
    "Fête de la Musique",
    "Bastille Day",
    "Assumption of Mary",
    "Oktoberfest",
    "St. Patrick's Day",
    "Halloween",
    "All Saints' Day",
    "Day of the Dead",
    "Armistice Day",
    "Constitution Day",
    "Christmas",
    "St. Stephen's Day",
    "Victory Day",
    "Immaculate Conception",
    "Valentine's Day",
    "Mardi Gras",
    "Pancake Day",
    "St. Joseph's Day",
    "National Liberation Day",
    "St. Lawrence's Day",
    "St. Andrew's Day",
    "Beer Festival",
    "Liberation Day",
    "King's Day",
    "Harvest Festival",
    "Republic Day",
    "Labor Day",
    "Victory Day",
    "Assumption Day",
    "National Day",
    "May Day",
    "St. George's Day",
    "Epiphany",
    "Fête Nationale",
    "Reformation Day",
    "Spring Bank Holiday",
    "Ascension Day",
    "Feast of St. Nicholas",
    "St. Martin's Day",
    "Day of the Constitution",
    "Mother's Day",
    "Father's Day",
    "Christmas",
    "Boxing Day"

]



# Creazione del file CSV
filename = "events.csv"
with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Events"])  # Intestazione della colonna
    for period in periods:
        writer.writerow([period])

print("CSV file 'events.csv' has been created.")

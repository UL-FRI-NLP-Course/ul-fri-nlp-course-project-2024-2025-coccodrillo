import csv

def ordina_csv_per_colonna(input_csv, output_csv, colonna_index):
    """Ordina un file CSV in base alla colonna specificata, trattando la colonna come numerica."""
    
    # Leggi i dati dal file CSV
    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Leggi l'intestazione (prima riga)
        rows = list(reader)  # Leggi tutte le righe

    # Ordina le righe in base alla colonna specificata (colonna_index è l'indice della colonna)
    # Convertiamo la colonna in numerica (ad esempio int o float)
    rows.sort(key=lambda x: float(x[colonna_index]) if x[colonna_index].replace('.', '', 1).isdigit() else 0)

    # Scrivi i dati ordinati in un nuovo file CSV
    with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)  # Scrivi l'intestazione
        writer.writerows(rows)  # Scrivi le righe ordinate

    print(f"File CSV ordinato e salvato come {output_csv}")

# Esegui la funzione
input_csv = 'rome.csv'  # Sostituisci con il nome del tuo file CSV di input
output_csv = 'rome_sorted.csv'  # Sostituisci con il nome del file CSV di output
colonna_index = 1  # Indice della colonna (0 è la prima colonna, 1 è la seconda, ecc.)

ordina_csv_per_colonna(input_csv, output_csv, colonna_index)

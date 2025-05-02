import csv
import info_place  # Assumiamo che la funzione `run` di questo modulo ritorni lat, long e una stringa

def leggi_e_scrivi_csv(input_csv, output_csv):
    # Apro il file di input (rome_sorted.csv) in modalità lettura
    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Leggi l'intestazione (prima riga)
        
        # Aggiungi le nuove colonne per latitudine, longitudine e stringa
        header.extend(['Latitudine', 'Longitudine', 'Duration'])

        # Apro il file di output (rome_complete.csv) in modalità scrittura
        with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header)  # Scrivi l'intestazione nel nuovo file

            # Leggo ogni riga dal file di input
            for row in reader:
                nome = row[0]  # Supponiamo che il nome sia nella prima colonna
                # Chiama la funzione info_place.run(nome), che restituisce una tupla (lat, long) e una stringa
                lat, long, duration = info_place.run(nome)  # Adattato secondo la tua descrizione
                
                # Aggiungi latitudine, longitudine e descrizione alla riga
                row.extend([lat, long, duration])
                
                # Scrivi la riga aggiornata nel file di output
                print(row)
                writer.writerow(row)

    print(f"File CSV creato con successo: {output_csv}")

# Esegui la funzione
input_csv = 'rome_sorted.csv'  # Sostituisci con il nome del tuo file CSV di input
output_csv = 'rome_complete.csv'  # Sostituisci con il nome del file CSV di output

leggi_e_scrivi_csv(input_csv, output_csv)

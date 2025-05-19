import os
import csv

def extract_name_from_file(file_path):
    """Estrai il nome dalla prima riga del file."""
    try:
        with open(file_path, 'r',encoding='utf-8') as f:
            first_line = f.readline()
            # Estrai il nome dalla riga, assumendo che sia prima del carattere '|'
            name = first_line.split('|')[0].strip()  # strip rimuove eventuali spazi
        return name
    except Exception as e:
        print(f"Errore nell'aprire o leggere il file {file_path}: {e}")
        return None

def create_csv_from_directories(root_directory, output_csv):
    """Crea un file CSV con nome e vecchio nome dei file."""
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['place', 'ranking'])  # Scrivi l'intestazione del CSV

        # Scorri tutte le directory nel percorso root_directory
        for dirpath, dirnames, filenames in os.walk(root_directory):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                
                # Estrai il nome dal file
                name = extract_name_from_file(file_path)
                ranking = filename[:-4]
                if name:
                    # Scrivi la riga nel file CSV
                    # filename è il vecchio nome del file (il numero)
                    csv_writer.writerow([name, ranking])
                    print(f"Aggiunto: {name}, {filename}")
                else:
                    print(f"Saltato il file {filename} (nome non trovato o errore)")

# Esegui la funzione
root_directory = './europe/italy/rome'  # Sostituisci con il percorso della tua directory principale
output_csv = 'output_file.csv'  # Sost
create_csv_from_directories(root_directory,output_csv)

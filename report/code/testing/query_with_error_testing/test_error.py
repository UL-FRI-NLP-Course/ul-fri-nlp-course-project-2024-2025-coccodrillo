import csv
import run

# File di input
input_file = './testing/dt_error.csv'
output_file = './testing/error_evaluation_output.csv'

with open(input_file, newline='', encoding='utf-8') as csvfile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    
    reader = csv.reader(csvfile, delimiter=';')
    writer = csv.writer(outfile, delimiter=';')
    
    # Scrive intestazione
    writer.writerow(["Sentence", "Comment", "Metadata"])
    
    for row in reader:
        if len(row) != 2:
            continue  # Salta righe mal formattate
        sentence, comment = row
        metadata = run.main(sentence)
        writer.writerow([sentence, comment, metadata])

print(f"File scritto con successo in {output_file}")

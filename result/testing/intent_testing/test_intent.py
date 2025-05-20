import csv
from collections import defaultdict
import run
from pathlib import Path


# File di input
input_file = './testing/intent_sentences.csv'
output_file = './testing/intent_evaluation_output.txt'
input_file = Path(input_file)
output_file = Path(output_file)

# Metriche
total = 0
correct = 0
confusion_matrix = defaultdict(int)
header = 0
errors = []  # Lista per memorizzare gli errori




with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        if header == 0:
            header = 1
            continue
        if len(row) != 2:
            continue  # Salta righe mal formattate

        sentence, true_intent = row
        true_intent = int(true_intent)
        predicted_intent = run.main(sentence)  # Funzione di predizione

        total += 1
        if predicted_intent == true_intent:
            correct += 1
        else:
            confusion_matrix[(true_intent, predicted_intent)] += 1
            errors.append((sentence, true_intent, predicted_intent))  # Aggiungi l'errore alla lista

# Scrittura dei risultati
with open(output_file, 'w', encoding='utf-8') as f:
    accuracy = correct / total if total > 0 else 0
    f.write(f"Size of test set: {total}\n")
    f.write(f"Accuracy: {accuracy:.2%}\n\n")
    f.write("Confusions:\n")
    
    # Scrivi la matrice di confusione
    for (true_intent, predicted_intent), count in confusion_matrix.items():
        f.write(f"Intent {true_intent} confused with Intent {predicted_intent}: {count} times\n")
    
    # Scrivi le frasi che hanno causato errori
    if errors:
        f.write("\nErrors:\n")
        for sentence, true_intent, predicted_intent in errors:
            f.write(f"Sentence: \"{sentence}\" | True Intent: {true_intent} | Predicted Intent: {predicted_intent}\n")

print(f"Risultati salvati in {output_file}")

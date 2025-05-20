from transformers import pipeline, BartTokenizer
import torch

# Carica il modello di sintesi e il tokenizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')

def summarize_text(text):
    # Controlla se il testo è vuoto o contiene solo spazi
    if not text.strip():
        return "[ERRORE]: Il testo è vuoto o contiene solo spazi."
    
    # Pulisci il testo da caratteri non stampabili
    cleaned_text = ''.join(c for c in text if c.isprintable())
    
    # Tokenizza il testo per ottenere il numero di token
    input_ids = tokenizer.encode(cleaned_text, return_tensors="pt")
    input_length = input_ids.size(1)  # Ottieni la lunghezza dei token
    
    print(f"[DEBUG] Lunghezza dei token nel testo: {input_length}")

    # Limita la lunghezza a 1024 token (limite massimo di BART)
    max_token_length = 1024
    if input_length > max_token_length:
        # Dividi il testo in chunk da max_token_length e riassumi ciascuno
        chunked_texts = [cleaned_text[i:i + max_token_length] for i in range(0, len(cleaned_text), max_token_length)]
        summaries = []
        for chunk in chunked_texts:
            try:
                summary = summarizer(chunk, max_length=150, min_length=40, do_sample=False)
                summaries.append(summary[0]['summary_text'])
            except Exception as e:
                print(f"[DEBUG] Errore durante il riassunto del chunk: {e}")
                summaries.append("[ERRORE]: Riassunto fallito")
        # Combina i riassunti dei singoli chunk
        return " ".join(summaries)
    
    try:
        # Usa il modello per riassumere il testo se è abbastanza corto
        summary = summarizer(cleaned_text, max_length=150, min_length=40, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"[DEBUG] Errore durante il riassunto: {e}")
        return f"[ERRORE]: {e}"


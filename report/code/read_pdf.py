import PyPDF2
import re
from typical_food import summarize
import translate
from pathlib import Path

def read(file_path):
    # Open the PDF file in read-binary mode
    txt = ""
    file_path =  Path(file_path)
    with open(file_path, 'rb') as pdf:
        reader = PyPDF2.PdfReader(pdf)
        
        if reader.is_encrypted:
            return -1
        
        # Loop through all pages and extract text
        for page in reader.pages:
            text = page.extract_text()
            if text:
                txt += text
        
    return txt.lower()


def get_update(txt):
    match = re.search(r'ultimo aggiornamento\s*[:\-]?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})', txt, re.IGNORECASE)
    if match:
        return match.group(1)
    else:
        return None

def get_vaccinazioni(testo):
    lines = testo.splitlines()
    paragrafo = ""
    collecting = False
    started_collecting = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Trova la riga con solo "Vaccinazioni"
        if not collecting and stripped.lower() == "vaccinazioni":
            paragrafo += "Vaccinazioni:\n"
            collecting = True
            continue

        if collecting:
            # Salta righe vuote iniziali dopo "Vaccinazioni"
            if not started_collecting:
                if stripped == "":
                    continue
                else:
                    started_collecting = True

            # Condizione di uscita: riga vuota + riga successiva non vuota
            if stripped == "" and i + 1 < len(lines) and lines[i + 1].strip() != "":
                break

            # Aggiungi il contenuto alla stringa finale
            paragrafo += " " + stripped

    return paragrafo.strip() if paragrafo else None



def get_safety(txt):
    lines = txt.splitlines()
    paragrafo = ""
    collecting = False
    for i, line in enumerate(lines):
        stripped = line.strip()

        # Trova la riga con solo "Vaccinazioni"
        if not collecting and stripped.lower() == "sicurezza":
            paragrafo += "Sicurezza:\n"
            collecting = True
            continue
        if stripped.lower() == 'mobilita\'':
            collecting = False
        if collecting:
            if stripped != "" and stripped != "\n":
                paragrafo += " " + stripped

    return paragrafo.strip() if paragrafo else None




def summerize(path):
    t = read(path)
    update = get_update(t)
    total = get_safety(t)
    riassunto = summarize.summarize_text(total)
    riassunto = translate.get_translate(riassunto,"it","en")
    return (update,riassunto)




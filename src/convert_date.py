import parsedatetime
from datetime import datetime

# Funzione per analizzare la data dalla frase
def extract_date_from_text(text):
    if text.lower() == "week":
        text = "next week"
    cal = parsedatetime.Calendar()
    
    # Cerca di interpretare la data dalla frase
    time_struct, parse_status = cal.parse(text)
    
    # Se la data è stata trovata, ritorna la data in formato dd/mm/yyyy
    if parse_status == 1:  # Status 1 indica che la data è stata interpretata correttamente
        parsed_date = datetime(*time_struct[:6])
        return parsed_date.strftime('%d/%m/%Y')
    else:
        return ""

from datetime import datetime

def is_near(period):
    # Converte la stringa 'period' nel formato d/m/Y in un oggetto datetime
    try:
        input_date = datetime.strptime(period, "%d/%m/%Y").date()  # Solo la data
    except ValueError:
        return False  # Se la data non è nel formato corretto, restituisce False
    
    # Ottieni la data odierna con ore e minuti a 00:00
    today = datetime.now().date()  # Solo la data, senza ore
    
    # Calcola la differenza in giorni tra la data odierna e la data fornita
    date_diff = (input_date - today).days
    
    # Se la data è nel futuro e non supera 7 giorni, o è oggi, ritorna True
    if (0 < date_diff <= 7) or (input_date == today):
        return True
    else:
        return False


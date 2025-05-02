from googletrans import Translator
import nltk

# Scarica i dati necessari (solo la prima volta)
nltk.download('punkt')

from nltk.tokenize import sent_tokenize

translator = Translator()

def get_translate(text, src, dest):
    try:
        trad = translator.translate(text, src=src, dest=dest)
        return trad.text
    except Exception as e:
        return text  # fallback

def translate_long_text(text,src,dest):
    sentences = sent_tokenize(text)  # divide in frasi
    translated_sentences = []

    for sentence in sentences:
        translated = get_translate(sentence, src, dest)
        translated_sentences.append(translated)

    return ' '.join(translated_sentences)
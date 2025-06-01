import subprocess
import sys


libraries = [
    'googletrans==4.0.0-rc1',
    'pyPDF2',
    'numpy',
    'spacy',
    'sentence_transformers',
    'parsedatetime',
    'opencv-python',
    'fuzzywuzzy',
    'dateparser',
    'torch==2.6.0',
    'geopy',
    'pyautogui',
    'scikit-learn',
    'webdriver-manager',
    'selenium',
    'bs4',
    'nltk',
]

for library in libraries:
    print(f"Installing: {library}")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', library])

print("\n✅ All libraries have been successfully installed.")

import nltk
from transformers import BertTokenizer, BertForQuestionAnswering
from sentence_transformers import SentenceTransformer
import spacy
from transformers import pipeline, BartTokenizer

subprocess.check_call([sys.executable,'-m','spacy','download','en_core_web_sm'])

nltk.download('punkt')
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
nlp = spacy.load("en_core_web_sm")
summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
tokenizer2 = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
model2 = SentenceTransformer('all-MiniLM-L6-v2')


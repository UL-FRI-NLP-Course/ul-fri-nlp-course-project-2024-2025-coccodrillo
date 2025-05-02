from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# === INPUT ===
query = "apprendimento automatico e reti neurali"
documenti = [
    "L'apprendimento automatico è una branca dell'intelligenza artificiale",
    "Le reti neurali sono un modello ispirato al cervello umano",
    "La cucina italiana è famosa per la pasta e la pizza",
    "I modelli di deep learning usano molteplici strati di neuroni e di apprendimento automatico"
]

# === STEP 1: Costruisci vettori TF-IDF ===
# La query va unita ai documenti per avere lo stesso vocabolario
corpus = documenti + [query]  # query alla fine
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus)

# === STEP 2: Estrai i vettori ===
query_vector = tfidf_matrix[-1]  # ultimo elemento
document_vectors = tfidf_matrix[:-1]  # tutti tranne l'ultimo

# === STEP 3: Calcola cosine similarity ===
similarità = cosine_similarity(query_vector, document_vectors).flatten()

# === OUTPUT ===
for i, score in enumerate(similarità):
    print(f"Similarità con Documento {i+1}: {score:.4f}")

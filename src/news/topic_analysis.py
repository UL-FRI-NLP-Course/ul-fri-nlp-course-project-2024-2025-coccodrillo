from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_real_articles(articles,stringa):
    try:
        # === STEP 1: Costruisci vettori TF-IDF ===
        # La query va unita ai documenti per avere lo stesso vocabolario
        corpus = articles + [stringa]  # query alla fine
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(corpus)

        # === STEP 2: Estrai i vettori ===
        query_vector = tfidf_matrix[-1]  # ultimo elemento
        document_vectors = tfidf_matrix[:-1]  # tutti tranne l'ultimo
        # === STEP 3: Calcola cosine similarity ===
        similarità = cosine_similarity(query_vector, document_vectors).flatten()
        vector = []
        # === OUTPUT ===
        for i, score in enumerate(similarità):
            if score >= 0.1:
                vector.append(articles[i])
        return vector
    except:
        return []

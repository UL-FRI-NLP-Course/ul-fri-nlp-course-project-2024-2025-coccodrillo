
# 🐊 NLP Project: `crocodile`

## Description

**Crocodile** is an intelligent natural language assistant. It is capable of interpreting complex requests regarding travel, weather, restaurants, events, safety, and much more. It uses advanced NLP models to understand user intents, extract relevant entities, correct errors, and generate structured responses.

---

## 🎯 Supported Intents

The system recognizes 8 main intents:

0. 📍 **Safety updates for a location** – _"Is it safe?"_
   - Sources: [Bing News](https://www.bing.com/news/search?) + [Viaggiare Sicuri](https://www.viaggiaresicuri.it)
   
1. 🌪️ **Weather alerts and extreme weather conditions**
   - Sources: [Bing News](https://www.bing.com/news/search?)
   
2. 🗺️ **Recommended places to visit**
   - Data: Dataset downloaded from [Lonely Planet](https://www.lonelyplanet.com/), with the help of Python scripts based on Selenium and BeautifulSoup.
   - Integration: Uses Google Maps to check the availability of locations (for example, to know if a place is temporarily closed).
   
3. 🎶 **Information on concerts and events**
   - Sources: [Bandsintown](https://www.bandsintown.com/)
   
4. 🍽️ **Best restaurants to eat**
   - Sources: [Yelp](https://www.yelp.ie/search)
   
5. 🍝 **Recommendations on typical dishes or foods**
   - Data: Dataset downloaded from [TasteAtlas](https://www.tasteatlas.com/), using Python scripts with Selenium and BeautifulSoup.
   
6. 🌤️ **Future weather forecasts**
   - Sources: [Il Meteo](https://www.ilmeteo.it/meteo/)
   
7. 🚄 **Information on trains, flights, and buses**
   - Sources: [TheTrainLine](https://www.thetrainline.com/)

---

## 📂 How to Run the Project

To run the project, execute the `run.py` file from the main project directory. You can do this using the command:

```bash
python run.py
```

## ⚙️ How It Works

- The user enters a natural language phrase in `run.py`
- The `BERT` model `all-MiniLM-L6-v2` is used to classify the intent of the request
- The text is analyzed to extract **cities**, **dates**, and other entities through:
  - 🧠 Question Answering with:
    ```python
    tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    ```
   - If information is missing (e.g., date), the system detects this and asks the user for clarification.
   - The system handles spelling errors and formatting through semantic checks.

- Downloaded datasets and information available on the web (using Python libraries like Selenium and BeautifulSoup) are used to search for all the necessary data.
- The output is presented to the user in a well-structured format.

---

## 🧾 System Output

**First Response:**  
An introductory sentence generated with a bi-grams model based on a simple dataset, explaining that the system is searching for information.

**Second Response:**  
A structured output of all the information found.

## 💡 Strengths

### ✅ Automatic Correction

The system automatically corrects small errors in city names or dates, thanks to spelling checks and semantic similarity logic.

---

### 📅 Support for Multiple Cities and Dates

The user can make complex requests, including **multiple destinations and time periods** within the same sentence.

---

### 🌍 Local News + Automatic Translation

For safety requests regarding foreign cities or countries:

- News is searched in the **local language** to maximize accuracy.
- Texts are **summarized and translated** using the following tools:

```python
from transformers import pipeline, BartTokenizer

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
```

#### 📎 Selecting the Most Relevant News

To filter articles and return only the most relevant ones to the query, the **similarity between the user query and found articles** is calculated:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus)
query_vector = tfidf_matrix[-1]
document_vectors = tfidf_matrix[:-1]
similarity = cosine_similarity(query_vector, document_vectors).flatten()
```

Only articles with similarity above a predefined threshold are included in the response.

#### 🛡️ Verified Safety Sources

- [Viaggiare Sicuri (Farnesina)](https://www.viaggiaresicuri.it/)
- Reliable international news websites
- Automatic summaries via `Bart`

---

### 🗺️ Custom Travel Recommendations

The system constructs a **graph of places to visit**:

- **Nodes** = points of interest (tourist attractions, monuments, museums, etc.)
- **Edges** = distances between places
- Each node has two weights:
  - **Beauty of the place**
  - **Estimated visit time**

#### 🔍 Optimizing the Route

- The system calculates the optimal route using a **minimum-cost algorithm**, which considers:
  - **Beauty of the place**
  - **Duration of the visit**
  - **Distance between places**

- It is assumed the user has **8 hours per day** available for sightseeing.

### Availability:
- For each location, the system checks the availability via **Google Maps**, ensuring the site is open on the specified day (e.g., avoiding temporarily closed or under-construction locations).

#### Example:
> If the user stays in Rome for 3 days → 8h x 3 = 24h  
> The system selects the **k best places** where the total of visit times and walking distances does not exceed 24 hours.
> The starting point of the route is chosen by the user.

### 🎫 Events and Concerts

The user can search for events specifying:

- City
- Dates
- Artist
- Music genre

The system connects to public APIs (e.g., **Bandsintown**) to show updated events.

---

### 🍽️ Restaurants and Local Food

- Suggests the **best restaurants** based on the area
- Recommends **typical dishes** based on location

---

### ☁️ Weather and Alerts

The weather module provides:

- **Detailed forecasts** for cities and dates
- **Automatic detection** of extreme events or abnormal conditions

---

### ✈️ Transport

The system provides up-to-date information on:

- Trains
- Buses

---

## ⚠️ Weaknesses

While the system is robust and flexible, it has some technical limitations that are currently being improved:

### 🚌 Train and Bus Search

- The transport website, if constantly queried, can **block automated traffic** detecting it as suspicious activity.
- In these cases, the search may fail or return incomplete results.

### 🌐 Article Translation

- Long articles may cause errors in the translation phase.
- The system splits texts into **individual sentences**, but sometimes **even a single sentence is too long** to be translated correctly.
- In these cases, the result is provided in the original language.

### 🎫 Travel Ticket Data

- Some search results (e.g., flights or trains) may contain **incorrect information**.

---

## 📌 Example Use Case

**User:**  
*What can I visit in Barcelona next weekend?*

**System Response:**  
1. Recognizes the intent → `places to visit`  
2. Extracts the city `Barcelona` and the date `next weekend`  
3. Generates an **introductory sentence** using language generation models  
4. Asks (optional) for a starting point.
5. Provides a list of main attractions based on **beauty, distance, and estimated visit time**  

---

## 🔧 Technologies Used

- **Language:** Python `3.10+`
- **NLP Models:**  
  - `BERT` (for Question Answering and Named Entity Recognition)  
  - `MiniLM` (for intent classification)  
  - `BART` (for summarization and translation)

- **Main Libraries:**  
  - `transformers`, `sentence-transformers`  
  - `scikit-learn`, `networkx`, `geopy`  
  - `nltk`, `spacy`, `pandas`, `requests`  
  - `beautifulsoup4`, `selenium`

---

## ✅ Testing

The system has been tested using real-world natural language phrases to verify its reliability and effectiveness in real scenarios. Three main types of tests were conducted to assess various aspects of the system:

1. **Test on ambiguous and incomplete requests**  
   Examples with incomplete or ambiguous phrases were used to verify how the system handles request interpretation and the processing of missing information.  
   The results of these tests are available in the `testing/query_with_error_testing` folder.

2. **Intent classification test**  
   This test verified if the system can correctly classify the user intent, even in the presence of complex phrases or multiple intents.  
   The results of these tests are available in the `testing/intent_testing` folder.

3. **Real request and output test**  
   In this test, real examples of requests were used, executing a complete simulation from query formulation to the system-generated output. The goal was to evaluate the quality of the responses generated and the overall system reliability.  
   The results of these tests are available in the `testing/final_output_testing` folder.

### Testing Details:
- In some cases, **spelling errors** were deliberately introduced in the requests to test the system's ability to correct them automatically.
- Multiple cities or dates were also included in a single request to verify how the system handles complex scenarios.

These tests helped identify and fix any weaknesses, improving the overall system reliability.

## 📬 Contact

Do you have suggestions, bugs to report, or want to contribute?

👉 Open an issue or contact me directly on [GitHub](https://github.com/daivdebelcastro-sig) or [GitHub](...)

---
	 
	 
	 
	 

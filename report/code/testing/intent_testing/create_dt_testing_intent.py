import csv
import random

intents = {
0: [
    "Is it safe to travel right now?",
    "Any updates on local safety?",
    "What's the latest on the security situation?",
    "Are there any safety concerns in the area?",
    "Tell me about current security conditions.",
    "Is it safe to visit Paris at the moment?",
    "Are there any travel advisories for Rome?",
    "What’s the security situation in Berlin?",
    "Is London currently safe for tourists?",
    "Are there any alerts about safety in Milan?",
    "Amsterdam, last news about the security",
    "Are there any ongoing security issues in Zurich?",
    "How is the safety situation in Vienna right now?",
    "Safety news or dangers during this period in Rome",

],

1: [
    "Are there any weather alerts today?",
    "Should I expect severe weather soon?",
    "Is there a storm warning?",
    "Any meteorological warnings in effect?",
    "What are the current weather warnings?",
    "Any weather alerts in London this week?",
    "Are there any heavy storms expected in Rome?",
    "What’s the forecast for extreme weather in Berlin?",
    "Are there any hurricane warnings in Barcelona?",
    "Weather-related disasters in Florence, updates and latest news.",

],

2: [
    "Can you suggest tourist attractions in Paris?",
    "What are must-see places in Rome?",
    "Where should I go if I visit Tokyo?",
    "Best spots to explore in Barcelona?",
    "What are the top sights in London?",
    "Where can I go for monuments in Berlin?",
    "What are the best places to visit in Madrid?",
    "Can you recommend some landmarks in Amsterdam?",
    "What are the most famous attractions in Vienna?",
    "Where should I visit in Milan?",
    "What are the best tourist destinations in Zurich?",
    "What’s worth seeing in Prague?",
    "Tell me about the famous attractions in Lisbon?",
    "Where can I go for visit Paris?",
    "What are the best museums in Florence?",
    "Best things to visit in Naples for 1 day",
    "Tell me the best things to visit in Rome for 5 days",
    "Send me a complete path about the most beautiful places to visit in Prague."
],

    3: [
    "What concerts are happening this week?",
    "Are there events in the city this weekend?",
    "Tell me about upcoming festivals.",
    "Is there a music event soon?",
    "Any local cultural events?",
    "What music festivals are taking place in Paris this month?",
    "Are there any concerts in London this weekend?",
    "When is the next art exhibition in Milan?",
    "Can you tell me about the upcoming jazz festival in Vienna?",
    "What events are scheduled for this week in Berlin?",
    "Are there any theater shows in Rome this weekend?",
    "What’s the schedule for classical music events in Amsterdam?",
    "Are there any cultural exhibitions in Zurich this month?",
    "What’s the next big festival in Madrid?",
    "Concert by Ultimo in Rome today",
    "Concert rock in Milan tomorrow"
],

4: [
    "What are the top-rated restaurants nearby?",
    "Where can I get the best food here?",
    "Any suggestions for great places to eat?",
    "Which restaurant is the most recommended?",
    "Tell me the best dining spots in town.",
    "Can you suggest a fancy restaurant in Rome?",
    "What's the most popular restaurant in this area?",
    "Where should I go for a good dinner tonight?",
    "Is there a top-reviewed restaurant near me?",
    "Best places to eat according to locals?",
    "Name a good place to eat Italian food.",
    "Where can I find high-end restaurants in Milan?",
    "Suggest a budget-friendly restaurant in London.",
    "What restaurant is trending in Tokyo?",
    "Any 5-star restaurants open now?",
    "Tell me the best place where i can eat in Naples"
],

    5: [
    "What traditional food should I try in Spain?",
    "Tell me the typical dishes of Italy.",
    "What's the best sweet in Naples?",
    "Give me a list of popular foods in Greece.",
    "Which dishes are famous in Germany?",
    "What should I eat in Thailand to taste the culture?",
    "What’s a must-try dish in Morocco?",
    "What local food is a must in Mexico?",
    "Name a traditional dessert from France.",
    "What is the national dish of Vietnam?",
    "Any signature meals I should try in Japan?",
    "What do people usually eat in Turkey?",
    "Tell me about local delicacies in India.",
    "What’s the most typical breakfast in the UK?",
    "Can you list traditional Portuguese dishes?",
    "What is the best thing to eat in Spain?"
],

   6: [
    "What's the weather forecast for next week?",
    "Can you tell me tomorrow's weather?",
    "Is it going to rain in the next few days?",
    "Give me the future weather outlook.",
    "What will the temperature be this weekend?",
    "What’s the forecast for the coming week in Paris?",
    "Will it be sunny in Berlin tomorrow?",
    "How warm will it be in Madrid next week?",
    "What’s the weather like in Rome for the weekend?",
    "Tell me the weather for tomorrow in London.",
    "Will there be snow in Prague this week?",
    "How hot is it expected to be in Athens?",
    "Can you give me a weather update for Zurich?",
    "What’s the temperature forecast for Vienna?"
],

7: [
    "Give me train schedules for tomorrow.",
    "When is the next bus to Milan?",
    "What are the flight times to Berlin?",
    "Tell me the transport options to get to Paris.",
    "How can I travel to Rome by train?",
    "What’s the next train to Florence?",
    "When does the flight to Amsterdam depart?",
    "Give me information on trains from Berlin to Prague.",
    "What time is the next bus to Barcelona?",
    "How can I get to Venice from Milan by train?",
    "What’s the schedule for flights to Zurich?",
    "When is the next bus to Lisbon?",
    "Tell me about train services from Paris to Brussels.",
    "How do I get to Munich from Vienna?",
    "What are the flight times from Milan to Rome?"
]
}

# Salva 100 frasi totali senza duplicati
all_sentences = []
for intent_index, examples in intents.items():
    for sentence in examples:
        all_sentences.append((sentence, intent_index))

# Mescola le frasi e salva le prime 100
random.shuffle(all_sentences)
dataset = all_sentences

# 💾 Salva su CSV
from pathlib import Path
output_path = "./testing/intent_sentences.csv"
output_path = Path(output_path)
with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    for sentence, intent_index in dataset:
        writer.writerow([sentence, intent_index])

print("✅ Dataset generato correttamente senza duplicati.")

from transformers import BertTokenizer, BertForQuestionAnswering, BertModel
import torch
import spacy
import check_similarity

tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
nlp = spacy.load("en_core_web_sm")




def replace(context,words):
    tokens = nlp(context)
    words = nlp(words)
    vector = check_similarity.get_most(tokens,words)
    for tupla in vector:
         par1 = tupla[1]
         par2 = tupla[0]
         new_context = context.replace(par1,par2)
         context = new_context
         
    return new_context



def is_correct(entity, label):
    doc = nlp(entity)
    for ent in doc.ents:
        if ent.label_ == label:
            return True
    return False







def ask_model(context, question):
    inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    start_scores = outputs.start_logits.squeeze()
    end_scores = outputs.end_logits.squeeze()
    start_index = torch.argmax(start_scores)
    end_index = torch.argmax(end_scores)
    start_index = max(0, start_index.item())  
    end_index = min(len(inputs['input_ids'][0]) - 1, end_index.item()) 
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][start_index:end_index+1]))
    start_prob = torch.softmax(start_scores, dim=0)[start_index].item()
    end_prob = torch.softmax(end_scores, dim=0)[end_index].item()
    answer_prob = start_prob * end_prob  
    return answer,answer_prob



def get_speaker(context):
    tupla = ask_model(context,"Who is the speaker?")
    speaker = ""
    if tupla[1] >= 0.90:
        speaker = tupla[0].capitalize()
        new_context = context.replace(speaker.lower(),"")
        context = new_context
    return context,speaker


def get_location(context,question="Where does he want?"):                              
    tupla = ask_model(context,question)
    destination = tupla[0]  
    if not is_correct(destination,"GPE"):
        dest_compared = check_similarity.get_best_city(destination)
        if  dest_compared == None:           
            destination = ""
        else:
            context = replace(context,dest_compared)
            destination = dest_compared
    return context,destination




def get_period(context,question="When?"):
    tupla = ask_model(context,question)
    period = tupla[0]
    if not (is_correct(period, "DATE") or is_correct(period, "EVENT") or is_correct(period, "TIME")):  
        date_compared = check_similarity.get_best_period(period)   
        if date_compared == None:       
            period = ""
        else:
            context = replace(context,date_compared)
            period = date_compared
    return context,period





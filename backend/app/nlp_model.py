# nlp_model.py

from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, pipeline

def load_nlp_model():
    model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=2)
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    nlp_pipeline = pipeline("text-classification", model=model, tokenizer=tokenizer)
    return nlp_pipeline

def predict_nlp(nlp_pipeline, description):
    return nlp_pipeline(description)
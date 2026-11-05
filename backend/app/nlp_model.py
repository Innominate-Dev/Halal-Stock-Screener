from transformers import BertTokenizer, BertForSequenceClassification
import torch
import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # this goes up from app/ to backend/
PROJECT_ROOT = os.path.dirname(BASE_DIR)  # this goes up one more level to project root
model = os.getenv("MODEL")
model_path = os.path.join(PROJECT_ROOT, model)

# Loading my trained model and its tokenizer
model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(model_path)

def predict(description):
    
    #Make it into numerical tokens that BERT can understand
    inputs = tokenizer(description, return_tensors="pt", padding=True, truncation=True, max_length=512)

    #Give a prediction
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    predicted_class = torch.argmax(logits, dim=1).item()

    #Map back to the label names
    label_mapping = {0: 'halal', 1: 'non-halal', 2: 'doubtful'}

    return label_mapping[predicted_class]

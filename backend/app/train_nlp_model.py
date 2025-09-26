import pandas as pd
import os
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from datasets import Dataset
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments

load_dotenv()
model_path = os.getenv("MODEL_PATH")

# Sample data (replace with your actual dataset)
data = [
    {"description": "A major beverage company that manufactures soft drinks and juices.", "label": "non-halal"},
    {"description": "A company that provides health insurance services for individuals and families.", "label": "non-halal"},
    {"description": "A technology firm offering software development services for small businesses.", "label": "halal"},
    {"description": "A real estate investment trust managing commercial properties and malls.", "label": "non-halal"},
    {"description": "A food processing company specializing in halal-certified chicken products.", "label": "halal"},
    {"description": "A corporation focused on research and development in artificial intelligence and machine learning.", "label": "halal"},
    {"description": "A tobacco company producing and selling cigarettes and cigars.", "label": "non-halal"},
    {"description": "A company that provides banking services, offering loans and interest-based products.", "label": "non-halal"},
    {"description": "A large automobile company manufacturing luxury cars with a focus on electric vehicles.", "label": "halal"},
    {"description": "An online store selling consumer electronics, gadgets, and accessories.", "label": "halal"},
    {"description": "A major streaming platform offering movies, TV shows, and adult content.", "label": "non-halal"},
    {"description": "A multinational fast food chain serving halal meat options and vegetarian meals.", "label": "halal"},
    {"description": "A large chain of bars and nightclubs serving alcohol.", "label": "non-halal"},
    {"description": "A global cosmetics company using non-animal tested products, but its parent company owns a gambling operation.", "label": "non-halal"},
    {"description": "A company offering stock brokerage services for high-net-worth individuals.", "label": "non-halal"},
    {"description": "A tech company providing cloud storage and digital security services.", "label": "halal"},
    {"description": "An online auction platform for art, antiques, and collectibles.", "label": "halal"},
    {"description": "A retailer of alcoholic beverages and related accessories.", "label": "non-halal"},
    {"description": "A company producing dietary supplements and healthy foods with halal certification.", "label": "halal"},
    {"description": "A video game company with a focus on violent and explicit content.", "label": "non-halal"},
    {"description": "A logistics and transportation company specializing in non-perishable goods.", "label": "halal"},
    {"description": "A gambling company offering sports betting and casino games.", "label": "non-halal"},
    {"description": "A company providing investment services with a focus on socially responsible and Islamic finance.", "label": "halal"},
    {"description": "A multinational alcohol producer, with a portfolio of spirits and beers.", "label": "non-halal"},
    {"description": "A multinational coffee chain offering ethically sourced beans and a focus on social welfare.", "label": "halal"},
    {"description": "A company involved in the production of synthetic fibers for industrial use.", "label": "halal"},
    {"description": "A biotechnology company working on genetically modified crops for agricultural use.", "label": "halal"},
    {"description": "An adult entertainment company producing films and other explicit media.", "label": "non-halal"},
    {"description": "A transportation company offering environmentally-friendly electric vehicles.", "label": "halal"},
    {"description": "A multinational mining company extracting resources like gold and diamonds.", "label": "non-halal"},
    {"description": "A pharmaceutical company specializing in non-haram drugs and halal-certified medications.", "label": "halal"},
    {"description": "A construction company focused on building mosques and Islamic community centers.", "label": "halal"},
    {"description": "A defense contractor manufacturing military weapons and ammunition.", "label": "non-halal"},
    {"description": "A company manufacturing non-alcoholic beverages with a focus on healthy hydration options.", "label": "halal"},
    {"description": "A luxury goods brand selling high-end jewelry and fashion accessories.", "label": "halal"},
    {"description": "A multinational coffee chain specializing in instant coffee and tea products.", "label": "halal"},
    {"description": "An energy company involved in nuclear power and fossil fuel extraction.", "label": "non-halal"},
    {"description": "A software company providing solutions for the healthcare sector.", "label": "halal"},
    {"description": "An online gambling platform offering casino games and poker.", "label": "non-halal"},
    {"description": "A technology company offering blockchain-based financial services.", "label": "halal"},
    {"description": "A car manufacturer specializing in luxury cars and high-performance sports models.", "label": "halal"},
    {"description": "A fashion company that promotes clothing lines with eco-friendly and ethical production practices.", "label": "halal"},
    {"description": "A chain of hotels catering exclusively to alcohol-free tourists.", "label": "halal"},
    {"description": "A company offering halal meat slaughtering services for local markets.", "label": "halal"},
    {"description": "A pharmaceutical company manufacturing synthetic recreational drugs.", "label": "non-halal"},
    {"description": "A furniture company specializing in modern, eco-friendly designs for urban homes.", "label": "halal"},
    {"description": "A cosmetics brand offering cruelty-free, halal-certified beauty products.", "label": "halal"},
    {"description": "A company providing payday loan services with high-interest rates.", "label": "non-halal"},
    {"description": "A global provider of education services, offering online courses and certifications.", "label": "halal"},
    {"description": "A telecommunications company specializing in 5G networks and high-speed internet.", "label": "halal"},
    {"description": "A company providing payday loan services with high-interest rates and debt consolidation.", "label": "non-halal"},
    {"description": "A major company producing non-halal food products for global distribution.", "label": "non-halal"},
    {"description": "A company offering legal services to businesses, specializing in corporate law.", "label": "halal"},
    
    # Add synthetic long-form samples (halal, non-halal, doubtful) — you can extend or replace
    {"description": "HalalFresh Co. is a certified halal food manufacturer offering frozen ready-to-eat meals, meat products, and snacks for the Muslim market in North America and the Middle East.", "label": "halal"},
    {"description": "LiquorWorld Inc. owns and operates a chain of retail liquor stores and online alcohol delivery services across major U.S. cities.", "label": "non-halal"},
    {"description": "MegaMart Corp. is a global e-commerce and logistics provider selling a wide range of consumer goods, including electronics, groceries, and third-party products, some of which include alcohol and adult items.", "label": "doubtful"},
    {"description": "SafePay Ltd. is a fintech company that enables secure digital payments through QR codes, NFC, and peer-to-peer transfers, compliant with Islamic finance rules.", "label": "halal"},
    {"description": "VegasBet Ltd. is a digital entertainment company offering online casino games, sports betting, and poker tournaments in Europe and Asia.", "label": "non-halal"},
    {"description": "StreamBox Ltd. operates a global video streaming platform that offers movies, TV shows, and original content, including mature and explicit-rated programming.", "label": "doubtful"},
]



# Create DataFrame
df = pd.DataFrame(data)

# Split data into train and validation
train_df, val_df = train_test_split(df, test_size=0.2)

# Convert to Hugging Face Dataset format
train_dataset = Dataset.from_pandas(train_df)
val_dataset = Dataset.from_pandas(val_df)

# Map labels to integers
label_mapping = {'halal': 0, 'non-halal': 1, 'doubtful': 2}
train_dataset = train_dataset.map(lambda e: {'label': label_mapping[e['label']]}, remove_columns=['label'])
val_dataset = val_dataset.map(lambda e: {'label': label_mapping[e['label']]}, remove_columns=['label'])

# Tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Tokenize the data
def tokenize_function(examples):
    return tokenizer(examples["description"], padding="max_length", truncation=True, max_length=512)

train_dataset = train_dataset.map(tokenize_function, batched=True)
val_dataset = val_dataset.map(tokenize_function, batched=True)

# Load pre-trained BERT model
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=3)

# Set up TrainingArguments
training_args = TrainingArguments(
    output_dir="./results",          # output directory
    num_train_epochs=10,              # number of epochs
    per_device_train_batch_size=8,   # batch size for training
    per_device_eval_batch_size=8,    # batch size for evaluation
    weight_decay=0.01,               # strength of weight decay
    logging_dir="./logs",            # logging directory
    logging_steps=100,               # number of steps to log
    save_steps=500,                  # how often to save the model
    save_total_limit=2,              # number of saved models to keep
)

# Initialize the Trainer
trainer = Trainer(
    model=model,                         # the instantiated 🤗 Transformers model to be trained
    args=training_args,                  # training arguments, defined above
    train_dataset=train_dataset,         # training dataset
    eval_dataset=val_dataset             # evaluation dataset
)

eval_results = trainer.evaluate()
print(f"Evaluation results: {eval_results}")

# Train the model
trainer.train()

# Save the trained model and tokenizer
model.save_pretrained(model_path)
tokenizer.save_pretrained(model_path)

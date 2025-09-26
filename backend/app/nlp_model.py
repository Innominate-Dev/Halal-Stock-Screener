from transformers import BertTokenizer, BertForSequenceClassification
import torch
import os
from dotenv import load_dotenv

load_dotenv()
model_path = os.getenv("MODEL_PATH")

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

# Testing a clear 'not-halal' case
description = "JPMorgan Chase & Co. is a leading global financial services firm based in the United States with operations worldwide, specializing in areas such as investment banking, financial services for consumers and small businesses, commercial banking, financial transaction processing, and asset management. The company, operating under the J.P. Morgan and Chase brands, serves a wide range of clients globally."
result = predict(description)
print(f"Predicted Label: {result}")  # Should return 'not-halal'

# Testing a clear 'halal' case
description = "Apple Inc. designs, manufactures, and markets various products and services globally. Their product lines include the iPhone, Mac personal computers, and iPad tablets. They also offer wearables, home products, and accessories such as AirPods, Apple TV, Apple Watch, Beats products, and HomePod. The company provides AppleCare support, cloud services, and operates platforms like the App Store for discovering and downloading applications and digital content. Additionally, Apple offers subscription services including Apple Arcade, Apple Fitness+, Apple Music, Apple News+, Apple TV+, Apple Card, and Apple Pay. They serve consumers, small and mid-sized businesses, and the education, enterprise, and government markets. Products are distributed through retail and online stores, direct sales, and third-party carriers and resellers. Apple Inc. was founded in 1976 and is headquartered in Cupertino, California."
result = predict(description)
print(f"Predicted Label: {result}")  # Should return 'halal'

# Testing a clear 'halal' case
description = "A company offering legal services to businesses, specializing in corporate law."
result = predict(description)
print(f"Predicted Label: {result}")  # Should return 'halal'

# Testing a clear 'doubtful' case
description = "Amazon.com, Inc. engages in the retail sale of consumer products and subscriptions in North America and internationally. The company operates through three segments: North America, International, and Amazon Web Services (AWS). It sells merchandise and content through online and physical stores. The company also manufactures and sells electronic devices, including Kindle, Fire tablets, Fire TVs, Echo, Ring, and other devices, and develops and produces media content. In addition, it offers programs that enable sellers to sell their products on its websites, and programs that allow authors, musicians, filmmakers, Twitch streamers, and other content creators to publish and sell content. Further, the company provides compute, storage, database, analytics, machine learning, and other services to developers and enterprises through AWS. Amazon.com, Inc. was founded in 1994 and is headquartered in Seattle, Washington."
result = predict(description)
print(f"Predicted Label: {result}")  # Should return 'Doubtful'

# Testing a difficult 'doubtful or halal' case
description = "Gibo Holdings Ltd is a HK-based company operating in Interactive Media & Services industry. Gibo Holdings Ltd is an investment holding company mainly engaged in the artificial intelligence (AI) technology business. The firm operates its businesses through its subsidiary Hong Kong Daily Group Supply Chain Ltd. The firm primarily engaged in developing AI technology to generate user content into AI scripts, images, voices and animation for its global users."
result = predict(description)
print(f"Predicted Label: {result}")  # Should return 'Doubtful'

# Testing a difficult 'halal' case
description = "Oracle Corp. engages in the provision of products and services that address aspects of corporate information technology environments, including applications and infrastructure technologies. The company is headquartered in Austin, Texas and currently employs 159,000 full-time employees. The firm's segments include cloud and license, hardware, and services. The cloud and license segment markets, sells and delivers a broad spectrum of enterprise applications and infrastructure technologies through its cloud and license offerings. The hardware segment provides a broad selection of enterprise hardware products and hardware-related software products including Oracle Engineered Systems, servers, storage, operating systems, virtualization, management and other hardware-related software and related hardware support. The services segment helps customers and partners maximize the performance of their investments in Oracle applications and infrastructure technologies. Its products and services are delivered worldwide through a variety of flexible and interoperable IT deployment models. These models include on-premise, cloud-based and hybrid deployments."
result = predict(description)
print(f"Predicted Label: {result}")  # Should return 'halal'
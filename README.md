# 🕋 Halal Stock Screener

An AI-powered web application that classifies stocks based on Shariah-compliant principles. By leveraging a fine-tuned **BERT** model, this tool analyzes company business descriptions to determine if they are **Halal**, **Non-Halal**, or **Doubtful**.

> [!WARNING]  
> **DISCLAIMER: NOT AAOIFI CERTIFIED**  
> This application is an educational and analytical tool powered by Machine Learning. It has **not** been audited or certified by the **Accounting and Auditing Organization for Islamic Financial Institutions (AAOIFI)** or any official Shariah Board. Users should not rely solely on this tool for investment decisions and are encouraged to perform their own due diligence or consult a qualified Shariah scholar.

---

## 🚀 Overview
Traditional stock screening often relies on manual keyword matching. This project uses **Natural Language Processing (NLP)** to understand the context of a company's operations, providing a more nuanced classification of their business activities.

- **Backend:** Python and FastAPI
- **Frontend:** React.js
- **AI Model:** Fine-tuned `bert-base-uncased` (Transformers)

---

## ⚙️ Setup & Installation

### 1. Model Training & Environment
Ensure you have a `.env` file in your root or backend folder:
```env
MODEL_PATH="./your-trained-model-path"
```

### 2. Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Frontend (React)
```bash
cd frontend
npm install
npm start
```

---

## 🧠 Machine Learning Approach
The core of this application is a **Sequence Classification** model. 
1. **Data:** Trained on a dataset of company descriptions with Shariah labels.
2. **Tokenizer:** BERT Tokenizer handles specialized financial and religious terminology.
3. **Fine-tuning:** Adjusts the pre-trained BERT weights to focus on "Halal" vs "Non-Halal" business nuances.

---


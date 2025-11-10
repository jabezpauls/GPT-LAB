# E-commerce Chatbot

**Experiment No. 1** | URK22CS1007 | 13-08-25

## Quick Setup

1. **Install Ollama and pull model:**
   ```bash
   ollama pull qwen2.5:0.5b
   ```

2. **Install dependencies:**
   ```bash
   cd ex1
   pip install -r requirements.txt
   ```

3. **Run the chatbot:**
   ```bash
   python chatbot.py
   ```

## Project Structure

```
ex1/
├── chatbot.py           # Main chatbot application
├── products.csv         # Product dataset (20 products)
├── ecommerce_faq.csv   # FAQ dataset (15 FAQs)
├── reviews.csv         # Product reviews (47 reviews)
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## How It Works

The chatbot processes user queries in this order:

1. **FAQ Matching** - Uses SentenceTransformer embeddings + cosine similarity (threshold: 0.65)
2. **Product Recommendations** - Detects keywords (recommend/suggest) → TF-IDF similarity
3. **Sentiment Analysis** - Detects keywords (review/feedback) → DistilBERT sentiment pipeline
4. **Product Q&A** - Falls back to Qwen LLM via Ollama with product context

## Features

- **FAQ Matching** using sentence embeddings
- **Product Q&A** using Qwen LLM via Ollama
- **Product Recommendations** using TF-IDF similarity
- **Sentiment Analysis** of reviews using DistilBERT

## Example Queries

```
"What is your return policy?"             → FAQ Match
"What is the price of wireless headphones?" → Product Q&A (LLM)
"Can you recommend a good laptop backpack?" → Recommendations
"What do customers say about fitness watch?" → Sentiment Analysis
```

## Tech Stack

- **LLM:** Qwen 2.5 (0.5b) via Ollama
- **Embeddings:** SentenceTransformer (all-MiniLM-L6-v2)
- **Recommendations:** TF-IDF (sklearn)
- **Sentiment:** DistilBERT (SST-2)

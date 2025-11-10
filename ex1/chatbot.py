import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
import ollama

# ---------------- CONFIG ----------------
FAQ_CSV = "ecommerce_faq.csv"
PRODUCTS_CSV = "products.csv"
REVIEWS_CSV = "reviews.csv"
OLLAMA_MODEL = "qwen2.5:0.5b"
FAQ_THRESHOLD = 0.65
# System role for Ollama
system_prompt = {
    "role": "system",
    "content": "You are an e-commerce assistant. Be concise, helpful, and answer only from given context."}

# ---------------- LOAD MODELS ----------------
print("Loading models...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  # For FAQ embeddings
sentiment_pipeline = pipeline("sentiment-analysis")        # For sentiment analysis

# ---------------- LOAD DATA ----------------
faq_df = pd.read_csv(FAQ_CSV)
products_df = pd.read_csv(PRODUCTS_CSV)
reviews_df = pd.read_csv(REVIEWS_CSV)
# Prepare FAQ embeddings
faq_df["embedding"] = faq_df["prompt"].apply(lambda q: embedding_model.encode(q))
# Prepare TF-IDF for products
products_df["text"] = products_df["name"] + " " + products_df["brand"] + " " + products_df["description"]
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(products_df["text"])

# ---------------- FUNCTIONS ----------------
def find_best_faq_match(user_question):
    """Find best FAQ match based on embeddings."""
    user_embedding = embedding_model.encode(user_question)
    similarities = [cosine_similarity([user_embedding], [emb])[0][0] for emb in faq_df["embedding"]]
    best_index = similarities.index(max(similarities))
    return faq_df.iloc[best_index]["prompt"], faq_df.iloc[best_index]["response"], similarities[best_index]
def get_top_product(query, top_k=1):
    """Return top-k product rows based on TF-IDF similarity."""
    query_vec = tfidf.transform([query])
    similarity = cosine_similarity(query_vec, tfidf_matrix)[0]
    top_idx = similarity.argsort()[-top_k:][::-1]
    return products_df.iloc[top_idx], similarity[top_idx]
def product_qa_llm(user_query):
    """Answer using Ollama and top product details."""
    top_product = get_top_product(user_query, top_k=1)[0].iloc[0]
    product_details = (
        f"Product ID: {top_product['product_id']}\n"
        f"Name: {top_product['name']}\n"
        f"Category: {top_product['category']}\n"
        f"Brand: {top_product['brand']}\n"
        f"Price: {top_product['price']}\n"
        f"Description: {top_product['description']}\n"  )
    prompt = f"""
    Answer the user's question using ONLY the product details below.
    If the answer is not available, say: 'I don't have that information.'
    {product_details}
    User Query: {user_query} """
    response = ollama.chat(model=OLLAMA_MODEL, messages=[
        system_prompt,
        {"role": "user", "content": prompt} ])
    return response["message"]["content"]
def recommend_products(user_query, top_k=3):
    """Return top-k recommended products."""
    query_vec = tfidf.transform([user_query])
    similarity = cosine_similarity(query_vec, tfidf_matrix)[0]
    top_indices = similarity.argsort()[-top_k:][::-1]
    recommendations = products_df.iloc[top_indices][['product_id', 'name', 'price', 'brand']]
    return recommendations
def get_product_reviews_sentiment(user_query):
    """Analyze sentiment for all reviews of products matching threshold > 0.7."""
    # Get top products (you can increase top_k if needed)
    matched_product_df, similarity_scores = get_top_product(user_query, top_k=10)
    # Filter products where similarity > 0.77
    filtered_products = matched_product_df[similarity_scores > 0.7]
    if filtered_products.empty:
        return "No matching product found for sentiment analysis."
    response_lines = []
    for _, product in filtered_products.iterrows():
        product_id = product["product_id"]
        product_name = product["name"]
        # Get reviews for this product
        product_reviews = reviews_df[reviews_df["product_id"] == product_id]
        if product_reviews.empty:
            continue
        response_lines.append(f"\nSentiment Analysis for {product_name}:\n")

        # Analyze each review
        for review in product_reviews["review"]:
            result = sentiment_pipeline(review)[0]
            sentiment = result["label"]
            score = round(result["score"], 2)
            response_lines.append(f"{sentiment} (score: {score})\nReview: {review}\n")
    if not response_lines:
        return "No reviews available for matched products."
    return "\n".join(response_lines)

# ---------------- CHATBOT LOGIC ----------------
def chatbot_response(user_input):
    user_input = user_input.strip()
    if not user_input:
        return "Please enter a valid query."
    # 1. Try FAQ match
    matched_q, matched_a, score = find_best_faq_match(user_input)
    if score >= FAQ_THRESHOLD:
        return f"[FAQ Match] {matched_a}"
    # 2. If query asks for recommendations
    if any(word in user_input.lower() for word in ["recommend", "suggest", "similar", "alternatives"]):
        recs = recommend_products(user_input)
        result = "Recommended Products:\n"
        for _, row in recs.iterrows():
            result += f"- {row['name']} ({row['brand']}) - ₹{row['price']}\n"
        return result
    # 3. If query asks about reviews or sentiment
    if any(word in user_input.lower() for word in ["review", "feedback", "opinion", "customer say"]):
        return get_product_reviews_sentiment(user_input)
    # 4. Default → Product Q&A via LLM
    return product_qa_llm(user_input)

# ---------------- RUN LOOP ----------------
if __name__ == "__main__":
    print("Welcome to E-Commerce Chatbot (type 'exit' to quit)\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = chatbot_response(user_input)
        print("Bot:", response, "\n")

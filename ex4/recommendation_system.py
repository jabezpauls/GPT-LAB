import ollama

# -----------------------------
# Sample User Data
# -----------------------------
user_profiles = [
    {"user": "Alice", "likes": ["Inception", "Interstellar", "The Matrix"]},
    {"user": "Bob", "likes": ["Pride and Prejudice", "Little Women", "Emma"]},
    {"user": "Charlie", "likes": ["Avengers", "Iron Man", "Spider-Man"]}
]

# -----------------------------
# Prompt Builder
# -----------------------------
def build_prompt(user):
    likes = ", ".join(user["likes"])
    return (
        f"The user named {user['user']} likes the following titles: {likes}. "
        "Suggest 5 **new** similar titles that the user hasn't seen yet. "
        "Do not repeat any of the liked titles. Return only a numbered list, no quotes, no explanations."
    )

# -----------------------------
# Generate Recommendations
# -----------------------------
def get_recommendations(user, model_name="qwen2.5:0.5b"):
    prompt = build_prompt(user)
    response = ollama.chat(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": "You are a recommendation engine. Always respond with a concise numbered list of 5 recommendations only."
            },
            {"role": "user", "content": prompt}
        ]
    )
    return response["message"]["content"]

# -----------------------------
# Display Results
# -----------------------------
def display_recommendations():
    for user in user_profiles:
        print("=" * 60)
        print(f"User: {user['user']}")
        print("Liked:", ", ".join(user["likes"]))
        print("Recommended:")
        print(get_recommendations(user))
        print("=" * 60, "\n")

# -----------------------------
# Freeform Query
# -----------------------------
def test_new_user_query(query, model_name="qwen2.5:0.5b"):
    refined_prompt = (
        f"The user says: '{query}'. "
        "Based on this, suggest 5 movies that are similar but not the same as any commonly known titles mentioned. "
        "Only respond with a clean numbered list of titles, no paragraphs or explanations."
    )
    response = ollama.chat(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": "You are a recommendation system. Output only a concise numbered list of 5 movies based on the user's taste."
            },
            {"role": "user", "content": refined_prompt}
        ]
    )
    print("Query:", query)
    print("Recommendations:")
    print(response["message"]["content"])

# -----------------------------
# Main Execution
# -----------------------------
if __name__ == "__main__":
    print("===== Personalized Recommendation System using Ollama =====\n")

    # Show results for predefined users
    display_recommendations()

    # Test with new query
    print("\nTesting with new user query...\n")
    test_new_user_query("I like fantasy movies with magic and dragons.")

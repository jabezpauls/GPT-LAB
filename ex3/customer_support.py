import ollama

# Step 1: Past customer-agent interactions
past_examples = [
    {
        "customer": "My order #84721 arrived with a cracked mug. What should I do?",
        "agent": "I'm sorry about the damaged mug. I can arrange a free replacement or a refund. "
                 "Please confirm your preference and share a photo so I can process it right away."
    },
    {
        "customer": "I was charged twice for my subscription this month.",
        "agent": "Thanks for reaching out. I see two charges on your account. "
                 "I've initiated a refund for the duplicate payment; it should reflect in 3–5 business days."
    },
    {
        "customer": "The tracking shows delivered but I didn't receive my package.",
        "agent": "I'm sorry you haven't received it yet. I can contact the carrier to open a trace. "
                 "Meanwhile, please check with neighbors. If not located in 48 hours, I'll send a replacement or refund."
    }
]

# Step 2: Prompt builder
def build_prompt(new_query: str) -> str:
    examples_text = "\n\n".join(
        f"Customer: {ex['customer']}\nAgent: {ex['agent']}"
        for ex in past_examples
    )
    prompt = f"""
You are a polite and professional customer support assistant.

Here are some past conversations:
{examples_text}

Now, draft a helpful reply to the NEW customer message based on past interactions.:

Customer: {new_query}

Reply:
"""
    return prompt.strip()


# Step 3: Suggest reply function
def suggest_reply(new_query: str) -> str:
    prompt = build_prompt(new_query)
    response = ollama.chat(
        model="qwen2.5:0.5b",  # make sure you pulled llama3 with: ollama pull llama3
        messages=[
            {"role": "system", "content": "You are a helpful customer support assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["message"]["content"].strip()

# Step 4: Test run
if __name__ == "__main__":
    new_customer_query = "Hi, I ordered headphones last week but tracking says delivered and I can't find them."
    reply = suggest_reply(new_customer_query)

    print("\nCustomer:", new_customer_query)
    print("\nSuggested Reply:\n", reply)

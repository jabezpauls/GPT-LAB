import requests

# Ollama API setup
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:0.5b"

# Step 1: Knowledge Base
knowledge_base = {
    "cold": {
        "keywords": ["sneeze", "runny nose", "congestion", "cough"],
        "advice": "It may be a common cold. Rest, drink warm fluids, and consider over-the-counter cold remedies.",
        "severity": "Mild"
        },
    "flu": {
        "keywords": ["fever", "body ache", "chills", "fatigue"],
        "advice": "It may be the flu. Stay hydrated, rest, and monitor your temperature.",
        "severity": "Moderate"
        },
    "migraine": {
        "keywords": ["headache", "nausea", "sensitivity to light", "sensitivity to sound"],
        "advice": "It may be a migraine. Rest in a quiet, dark room and consider over-the-counter pain relief.",
        "severity": "Mild"
        },
    "indigestion": {
        "keywords": ["stomach pain", "nausea", "bloating", "heartburn"],
        "advice": "It may be indigestion. Avoid spicy food, drink water, and try small light meals.",
        "severity": "Moderate"
        },
    "chest pain": {
        "keywords": ["chest pain", "shortness of breath", "pressure"],
        "advice": "Potentially serious. Seek immediate medical attention.",
        "severity": "Severe"
    }
}

conversation_memory = []

# Step 2: Knowledge Base Match
def check_knowledge_base(symptoms):
    for condition, data in knowledge_base.items():
        if any(word in symptoms.lower() for word in data["keywords"]):
            return f"Condition: {condition.title()}\nSeverity: {data['severity']}\nAdvice: {data['advice']}"
    return None

# Step 3: Ask Ollama Qwen
def ollama_response(symptoms):
    prompt = f"""
You are a helpful medical assistant AI.
Analyze the following symptoms and provide:
1. Possible causes
2. Home care advice
3. When to see a doctor
Always end with: "Disclaimer: I am not a doctor."
Symptoms: {symptoms}
"""
    payload = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
    response = requests.post(OLLAMA_URL, json=payload)
    if response.status_code == 200:
        return response.json().get("response", "").strip()
    else:
        return f"Error: {response.text}"

# Step 4: Combine KB + Model
def medical_assistant(symptoms):
    kb_result = check_knowledge_base(symptoms)
    if kb_result:
        result = kb_result
    else:
        result = ollama_response(symptoms)

    # Emergency alert
    if any(word in symptoms.lower() for word in ["chest pain", "shortness of breath", "breathe"]):
        result = "⚠️ EMERGENCY ALERT: Seek immediate medical help!\n" + result

    disclaimer = "\nDisclaimer: This information is for general awareness and not a substitute for professional medical advice."
    if "Disclaimer" not in result:
        result += disclaimer

    conversation_memory.append({"user": symptoms, "assistant": result})
    return result

# Step 5: Export Health Report
def export_report():
    with open("health_report.txt", "w") as f:
        for turn in conversation_memory:
            f.write(f"User: {turn['user']}\nAssistant: {turn['assistant']}\n\n")
    print("Health report saved as health_report.txt")

# Step 6: Interactive Loop
if __name__ == "__main__":
    print("AI Medical Assistant (Demo)")
    print("Type 'exit' to quit or 'report' to export.\n")

    while True:
        user_input = input("Enter your symptoms: ")
        if user_input.lower() == "exit":
            export_report()
            print("Goodbye! Stay healthy.")
            break
        elif user_input.lower() == "report":
            export_report()
        else:
            print("\nAssistant Response:\n", medical_assistant(user_input), "\n")

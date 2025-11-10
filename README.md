# Ollama AI Projects

Collection of AI-powered applications using Ollama's Qwen 2.5 model for various practical use cases.

## Prerequisites

Before running any of these projects, ensure you have:

1. **Ollama installed and running**
   ```bash
   # Install Ollama from https://ollama.ai
   # Start Ollama service
   ollama serve
   ```

2. **Qwen model pulled**
   ```bash
   ollama pull qwen2.5:0.5b
   ```

3. **Python dependencies installed**
   ```bash
   # Install required packages
   venv/bin/pip install ollama requests
   ```

---

## Projects Overview

### ex3 - Customer Support Assistant

**What it does:**
- Uses few-shot learning to generate customer support responses
- Learns from past customer-agent conversation examples
- Suggests professional and helpful replies to new customer queries

**How to run:**
```bash
cd ex3
../venv/bin/python customer_support.py
```

**Example output:**
Takes a customer query like "I ordered headphones but tracking says delivered and I can't find them" and generates a helpful support response based on past examples.

---

### ex4 - Personalized Recommendation System

**What it does:**
- Recommends movies/books based on user preferences
- Analyzes past liked titles to suggest similar content
- Supports both predefined user profiles and custom queries
- Provides 5 recommendations per request

**How to run:**
```bash
cd ex4
../venv/bin/python recommendation_system.py
```

**Features:**
- Predefined profiles for Alice (sci-fi), Bob (classics), Charlie (superhero)
- Custom query support (e.g., "I like fantasy movies with magic and dragons")

---

### ex6 - AI Medical Assistant

**What it does:**
- Analyzes user-reported symptoms
- Suggests possible conditions with severity levels (Mild, Moderate, Severe)
- Provides home care remedies and advice
- Triggers emergency alerts for critical symptoms
- Maintains conversation history
- Exports health reports

**How to run:**
```bash
cd ex6
../venv/bin/python medical_assistant.py
```

**Interactive commands:**
- Enter symptoms when prompted
- Type `report` to export conversation to `health_report.txt`
- Type `exit` to quit and save final report

**Knowledge base includes:**
- Cold (runny nose, cough, congestion)
- Flu (fever, body ache, chills)
- Migraine (headache, light sensitivity)
- Indigestion (stomach pain, bloating)
- Emergency conditions (chest pain, breathing issues)

**⚠️ Important:** This is a demo application for educational purposes only. Not a substitute for professional medical advice.

---

## Technical Details

- **Model**: Qwen 2.5 (0.5B parameters)
- **Framework**: Ollama for local LLM inference
- **Python version**: 3.x
- **API approach**:
  - ex3 & ex4: Use `ollama.chat()` (ollama Python library)
  - ex6: Uses direct HTTP requests to Ollama API

## Troubleshooting

**Issue**: "Connection refused" or API errors
- **Solution**: Make sure Ollama is running (`ollama serve`)

**Issue**: "Model not found"
- **Solution**: Pull the model first (`ollama pull qwen2.5:0.5b`)

**Issue**: "ModuleNotFoundError"
- **Solution**: Install dependencies (`venv/bin/pip install ollama requests`)

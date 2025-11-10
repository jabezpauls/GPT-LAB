# AI Blog Post Generator

**Experiment No. 2** - Blog Generation using Local LLM

## Quick Setup

1. **Install Ollama and pull model:**
   ```bash
   ollama pull qwen2.5:0.5b
   ```

2. **Install dependencies:**
   ```bash
   cd ex2
   ~/Workspace/pranov/venv/bin/pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   ~/Workspace/pranov/venv/bin/python blog_generator.py
   ```

4. **Open browser:**
   - Navigate to `http://127.0.0.1:7860`

## Project Structure

```
ex2/
├── blog_generator.py    # Main Gradio application
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Features

- **Clean Modern UI** - Slate gray theme, minimal design, elegant layout
- **Model Load Status** - Real-time progress tracking with visual feedback
- **Generation Statistics** - Time taken and word count displayed
- **Structured Input** - Topic, tone, length, and outline configuration
- **Smooth Interactions** - Hover effects and subtle animations
- **Error Handling** - Clear troubleshooting messages

## How It Works

1. User enters blog topic and configuration
2. System constructs structured prompt
3. Progress tracker shows model loading status
4. Qwen 2.5 generates blog content via Ollama
5. Statistics displayed (generation time, word count)
6. Blog content shown in clean output box

## UI Features

- **Slate Gray Theme** - Clean, professional slate/gray color palette
- **Modern Minimalist** - No harsh colors, elegant spacing
- **Dropdown Menus** - Pre-configured tone and length options
- **Progress Tracking** - Real-time visual feedback during generation
- **Statistics Display** - Generation time and word count
- **Smooth Animations** - Subtle hover effects and transitions
- **Error Messages** - Helpful troubleshooting information

## Tech Stack

- **LLM:** Qwen 2.5 (0.5b) via Ollama
- **UI Framework:** Gradio 4.0+
- **Language:** Python 3.8+

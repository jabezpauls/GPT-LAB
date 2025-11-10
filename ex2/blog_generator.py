import gradio as gr
import ollama
from typing import List
import json
import re
import time

def clean_text(text: str) -> str:
    """
    Clean user input text by removing excessive whitespace and unwanted characters.
    """
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text

def generate_blog(topic: str, tone: str, length: str, outline: str, progress=gr.Progress()):
    """
    Generate a blog post using local LLM via Ollama based on user inputs.
    """
    if not topic.strip():
        return "Error: Please enter a blog topic.", "N/A", "N/A", ""

    # Clean inputs
    topic_clean = clean_text(topic)
    tone_clean = clean_text(tone) if tone.strip() else "informative"
    length_clean = clean_text(length) if length.strip() else "500 words"
    outline_clean = clean_text(outline) if outline.strip() else "Introduction\nMain content\nConclusion"

    # Show loading progress
    progress(0.1, desc="Preparing prompt...")
    time.sleep(0.3)

    # Construct structured prompt
    prompt = f"""
Write a blog post about "{topic_clean}" in a {tone_clean} tone, approximately {length_clean} words.

Use the following outline:
{outline_clean}

Make it well-structured, engaging, and plagiarism-free. Include a catchy title at the beginning.
"""

    try:
        progress(0.3, desc="Loading model...")
        time.sleep(0.3)

        progress(0.5, desc="Generating blog content...")

        # Call local LLM via Ollama
        start_time = time.time()
        response = ollama.chat(
            model="qwen2.5:0.5b",
            messages=[{
                "role": "system",
                "content": "You are a professional blog writer. Create high-quality, engaging content."
            }, {
                "role": "user",
                "content": prompt
            }]
        )
        end_time = time.time()

        progress(0.9, desc="Finalizing...")
        time.sleep(0.2)

        blog_content = response['message']['content']
        generation_time = f"{end_time - start_time:.2f}s"
        word_count = len(blog_content.split())

        # Create metadata string
        metadata = f"Generation Time: {generation_time} | Word Count: {word_count} | Model: qwen2.5:0.5b"

        progress(1.0, desc="Complete!")

        return blog_content, generation_time, str(word_count), metadata

    except Exception as e:
        error_message = f"Error generating blog: {str(e)}\n\nTroubleshooting:\n1. Ensure Ollama is running\n2. Verify qwen2.5:0.5b model is installed\n3. Run: ollama pull qwen2.5:0.5b"
        return error_message, "N/A", "N/A", ""

# Custom CSS for clean, modern design
custom_css = """
.gradio-container {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    max-width: 1200px;
    margin: auto;
}

.header {
    text-align: center;
    padding: 2.5rem 0;
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    color: white;
    border-radius: 12px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.stats-box {
    background: #f8fafc;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    border: 1px solid #e2e8f0;
}

.generate-btn {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 0.75rem 2rem !important;
    border-radius: 8px !important;
    border: none !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
}

.generate-btn:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15) !important;
}

.output-box {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    border: 1px solid #e2e8f0;
}

.info-text {
    color: #64748b;
    font-size: 0.9rem;
    font-style: italic;
}
"""

# Build Gradio Interface
with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:

    # Header
    gr.HTML("""
        <div class="header">
            <h1 style="margin:0; font-size: 2.5rem;">✍️ AI Blog Post Generator</h1>
            <p style="margin:0.5rem 0 0 0; opacity: 0.9;">Powered by Qwen 2.5 via Ollama</p>
        </div>
    """)

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📝 Blog Configuration")

            topic_input = gr.Textbox(
                label="Blog Topic",
                placeholder="e.g., The Future of AI in Healthcare",
                lines=2,
                info="Enter the main subject of your blog post"
            )

            with gr.Row():
                tone_input = gr.Dropdown(
                    label="Writing Tone",
                    choices=["Informative", "Conversational", "Professional", "Casual", "Academic", "Persuasive"],
                    value="Informative",
                    info="Select the desired tone"
                )

                length_input = gr.Dropdown(
                    label="Desired Length",
                    choices=["300 words", "500 words", "800 words", "1000 words", "1500 words"],
                    value="500 words",
                    info="Approximate word count"
                )

            outline_input = gr.Textbox(
                label="Blog Outline",
                placeholder="Introduction\nKey Applications\nBenefits and Challenges\nFuture Trends\nConclusion",
                lines=6,
                info="Structure your blog with key points (one per line)"
            )

            generate_button = gr.Button("✨ Generate Blog Post", elem_classes=["generate-btn"], size="lg")

            gr.Markdown("---")

            # Statistics
            gr.Markdown("### 📊 Generation Statistics")
            with gr.Row():
                time_output = gr.Textbox(label="⏱️ Time", interactive=False, scale=1)
                words_output = gr.Textbox(label="📄 Words", interactive=False, scale=1)

        with gr.Column(scale=1):
            gr.Markdown("### 📄 Generated Blog Post")

            metadata_output = gr.Textbox(
                label="Metadata",
                interactive=False,
                show_label=False,
                elem_classes=["info-text"]
            )

            output_box = gr.Textbox(
                label="",
                lines=25,
                show_label=False,
                placeholder="Your generated blog post will appear here...",
                elem_classes=["output-box"]
            )

    # Footer
    gr.Markdown("""
    ---
    <div style="text-align: center; color: #6c757d; font-size: 0.9rem;">
        <p>💡 <strong>Tips:</strong> Be specific with your topic | Choose an appropriate tone | Provide a clear outline</p>
        <p>Made with ❤️ using Gradio + Ollama</p>
    </div>
    """)

    # Connect button to function
    generate_button.click(
        fn=generate_blog,
        inputs=[topic_input, tone_input, length_input, outline_input],
        outputs=[output_box, time_output, words_output, metadata_output]
    )


if __name__ == "__main__":
    print("Starting Blog Generator UI...")
    print("Model: qwen2.5:0.5b")
    print("Ensure Ollama is running with: ollama pull qwen2.5:0.5b")
    demo.launch(share=False, show_error=True)

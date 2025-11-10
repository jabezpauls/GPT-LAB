# AI Document Analyzer

**Experiment No. 5** - Automated Document Analysis using Local LLM

## Quick Setup

1. **Install Ollama and pull model:**
   ```bash
   ollama pull qwen2.5:0.5b
   ```

2. **Install dependencies:**
   ```bash
   cd ex5
   ~/Workspace/pranov/venv/bin/pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   ~/Workspace/pranov/venv/bin/python document_analyzer.py
   ```

4. **Open browser:**
   - Navigate to `http://127.0.0.1:7860`

## Project Structure

```
ex5/
├── document_analyzer.py # Main Gradio application
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Objective

The Automated Document Analyzer assists users in quickly understanding the content of legal documents, contracts, or literary texts through AI-powered summarization and analysis.

## Features

### Core Capabilities
- **Multi-level Summaries** - Short (1-2 sentences), Medium (paragraph), Detailed (section-wise)
- **Smart Key Extraction** - Highlights key clauses for legal docs or themes for literary texts
- **Interactive Q&A** - Ask questions about uploaded document content
- **Drag & Drop Upload** - Convenient file upload interface
- **Tabbed Interface** - Organized results in Summary, Q&A, Keywords, Export tabs
- **Multiple Export Formats** - Export to PDF, DOCX, or TXT

### Document Types
- **Legal Documents** - Analyzes: Parties, Payment Terms, Liabilities, Confidentiality, Risks, Termination
- **Literary Texts** - Analyzes: Characters, Plot Events, Themes, Moral Lessons

### Supported File Formats
- PDF (.pdf)
- Word Documents (.docx)
- Text Files (.txt)

## How It Works

1. **Upload Document** - Drag & drop or select PDF/DOCX/TXT file
2. **Configure Analysis** - Select document type, summary level, export format
3. **Ask Questions** (Optional) - Query specific information from the document
4. **Analyze** - System extracts text and generates comprehensive analysis
5. **Review Results** - View summary, Q&A, keywords in tabbed interface
6. **Export** - Download analysis report in preferred format

## UI Features

- **Slate Gray Theme** - Clean, professional design
- **Progress Tracking** - Real-time analysis status updates
- **Document Statistics** - Word count and processing time
- **Organized Layout** - Configuration panel and results side-by-side
- **Tabbed Results** - Easy navigation between different analysis types
- **Export Status** - Clear feedback on file generation

## Usage Examples

### Legal Document Analysis
1. Upload contract PDF
2. Select "Legal" document type
3. Choose "Detailed" summary level
4. Ask: "What are the payment terms?"
5. Get section-wise analysis with key clauses highlighted

### Literary Text Analysis
1. Upload novel/story DOCX
2. Select "Literary" document type
3. Choose "Medium" summary level
4. Ask: "Who are the main characters?"
5. Get plot summary with character analysis and themes

## Export Options

- **TXT** - Plain text report (lightweight)
- **DOCX** - Formatted Word document (editable)
- **PDF** - Professional PDF report (shareable)

## Technical Details

- **LLM:** Qwen 2.5 (0.5b) via Ollama
- **UI Framework:** Gradio 4.0+
- **Text Extraction:** PyPDF2 (PDF), python-docx (DOCX)
- **PDF Generation:** ReportLab
- **API:** Ollama REST API with streaming

## Troubleshooting

### Issue: "Error connecting to Ollama API"
**Solution:** Ensure Ollama is running: `ollama serve`

### Issue: "Unable to extract text"
**Solution:**
- Verify file is not corrupted
- Ensure PDF is text-based (not scanned images)
- Try converting to TXT format

### Issue: "No response content"
**Solution:**
- Check if model is loaded: `ollama list`
- Pull model again: `ollama pull qwen2.5:0.5b`
- Restart Ollama service

## Performance Tips

- Use text-based PDFs for best results
- Shorter documents (< 5000 words) process faster
- "Short" summary level is fastest
- Close other Ollama sessions to free resources

## Future Enhancements

- Multi-document comparison
- Batch processing
- Custom extraction templates
- Advanced sentiment analysis
- Table and chart extraction
- OCR support for scanned documents

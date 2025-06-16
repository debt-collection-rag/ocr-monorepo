# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

This is an OCR (Optical Character Recognition) pipeline monorepo that processes PDF documents using multiple OCR engines and a custom table detection classifier.

### Core Components

1. **runner.py** - Main entry point that orchestrates the PDF processing pipeline
   - Accepts PDF files via command line (supports glob/regex patterns)
   - Converts PDFs to images using pdf2image
   - Runs table detection classifier on all pages
   - TODO: Implement actual OCR text extraction

2. **classifier.py** - Table detection using EfficientNet
   - Uses a pretrained EfficientNet-B0 model fine-tuned for table detection
   - Model weights stored in `efficientnet_model_epoch_10.pt`
   - Returns boolean indicators for table presence on each page

3. **azure.py** - Azure Document Intelligence integration
   - Requires AZURE_API_ENDPOINT and AZURE_API_KEY environment variables
   - Supports markdown output format for tables

4. **paddle.py** - PaddleOCR integration (implementation incomplete)

### Commands

```bash
# Install system dependencies (required)
# Install poppler-utils at system level (e.g., brew install poppler on macOS)

# Setup Python environment
conda create -n monorepo python=3.11
conda activate monorepo
pip install -r requirements.txt

# Run the OCR pipeline
python runner.py document.pdf
python runner.py "*.pdf"
python runner.py "doc_[0-9]+\.pdf"

# View help
python runner.py --help
```

### Dependencies

- **System**: poppler-utils (for pdf2image)
- **OCR Engines**: Azure Document Intelligence, PaddleOCR
- **ML**: PyTorch, timm (for EfficientNet classifier)
- **PDF Processing**: pdf2image

### Environment Variables

- `AZURE_API_ENDPOINT` - Azure Document Intelligence endpoint
- `AZURE_API_KEY` - Azure Document Intelligence API key

### Current TODOs

1. Add support for glob/regex patterns through command line ✓
2. Batch classifier calls
3. Complete pages-to-text conversion in pdf_to_text()
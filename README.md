# ocr-monorepo
our completed OCR pipeline 

### requirements
- make sure `poppler-utils` is installed @ the system level (rather than using pip)
- run `pip install -r requirements.txt`

### helpers
- `azure.py` calls Azure Document Intelligence
- `classifier.py` calls our table detection classifier
- `paddle.py` calls [PaddleOCR](https://paddlepaddle.github.io/PaddleOCR/main/en/index.html)
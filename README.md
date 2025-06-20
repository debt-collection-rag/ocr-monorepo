# ocr-monorepo
our completed OCR pipeline 

### Interface (`runner.py`)
- INPUT: paths to PDF files for a given case
- OUTPUT:
    - list per doc of
    - list per page of
    - text representation of page

### dotenv
We use a `.env` file to manage environment variables for Azure. To make your own, you'll have to set up an azure document intelligence instance - see `azure_ocr.py` or [Microsoft's documentation](https://learn.microsoft.com/azure/ai-services/document-intelligence/quickstarts/get-started-sdks-rest-api?pivots=programming-language-python) for details.

### requirements
- make sure `poppler-utils` is installed @ the system level (rather than using pip)
- (optional) create a python env with `conda create -n monorepo python=3.11` and activate it with `conda activate monorepo`
- run `pip install -r requirements.txt`

### helpers
- `azure.py` calls Azure Document Intelligence
- `classifier.py` calls our table detection classifier
- `paddle.py` calls [PaddleOCR](https://paddlepaddle.github.io/PaddleOCR/main/en/index.html)
"""
This code sample shows Prebuilt Layout operations with the Azure AI Document Intelligence client library.
The async versions of the samples require Python 3.8 or later.

To learn more, please visit the documentation - Quickstart: Document Intelligence (formerly Form Recognizer) SDKs
https://learn.microsoft.com/azure/ai-services/document-intelligence/quickstarts/get-started-sdks-rest-api?pivots=programming-language-python
"""

# notebook: https://colab.research.google.com/drive/1OCl0EoYK6jGyfVlnEWYDDrrVULP-0Tz8

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from dotenv import load_dotenv
import os

load_dotenv()

endpoint = os.getenv("AZURE_API_ENDPOINT")
key = os.getenv("AZURE_API_KEY")

document_intelligence_client = DocumentIntelligenceClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

def ocr(docs: list):
    for doc in docs:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout", 
            doc,
            output_content_format = DocumentContentFormat.MARKDOWN
        )
        yield poller.result()

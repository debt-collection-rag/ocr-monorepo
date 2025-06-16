"""
This code sample shows Prebuilt Layout operations with the Azure AI Document Intelligence client library.
The async versions of the samples require Python 3.8 or later.

To learn more, please visit the documentation - Quickstart: Document Intelligence (formerly Form Recognizer) SDKs
https://learn.microsoft.com/azure/ai-services/document-intelligence/quickstarts/get-started-sdks-rest-api?pivots=programming-language-python
"""

# notebook: https://colab.research.google.com/drive/1OCl0EoYK6jGyfVlnEWYDDrrVULP-0Tz8

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence.aio import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import DocumentContentFormat
from azure.core.exceptions import HttpResponseError

from image_util import image_to_bytes

from dotenv import load_dotenv
import os
import asyncio
import time

load_dotenv()

endpoint = os.getenv("AZURE_API_ENDPOINT")
key = os.getenv("AZURE_API_KEY")

async def process_single_document(client, doc, index, max_retries=3):
    """Process a single document with retry logic for rate limiting"""
    for attempt in range(max_retries):
        try:
            print(f'Processing page {index}')
            poller = await client.begin_analyze_document(
                "prebuilt-layout", 
                image_to_bytes(doc),
                output_content_format = DocumentContentFormat.MARKDOWN
            )
            result = await poller.result()
            return result.content
        except HttpResponseError as e:
            if e.status_code == 429 and attempt < max_retries - 1:
                print(f'Rate limit hit for page {index}, waiting 1 second before retry {attempt + 1}/{max_retries}')
                await asyncio.sleep(1)
            else:
                raise

async def ocr_async(docs: list):
    """Process multiple documents concurrently using async"""
    async with DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    ) as client:
        tasks = [
            process_single_document(client, doc, i) 
            for i, doc in enumerate(docs)
        ]
        return await asyncio.gather(*tasks)

def ocr(docs: list):
    """Synchronous wrapper for the async OCR function"""
    return asyncio.run(ocr_async(docs))
# for cmd line arguments
import argparse
from glob_util import expand_patterns

# for doc processing
from pdf2image import convert_from_path
# import numpy as np

# my helpers
from classifier import classify
from flattening_util import *
from stitching_util import *
from azure_ocr import ocr as _azure_ocr
from paddle_ocr import ocr as _paddle_ocr

"""
docs: paths to (multi-page) pdf docs to process
returns
- list per doc of
- list per page of
- text representation of page
"""
def pdf_to_text(*docs) -> list[list[str]]:
    # maps to pages
    docs_pages = [convert_from_path(doc) for doc in docs]

    # flattens
    flat_pages, lengths = flatten(docs_pages)

    page_classes = classify(flat_pages)

    pages_with_tables, pages_without_tables = unstitch(flat_pages, page_classes)

    texts_with_tables = _azure_ocr(pages_with_tables)
    texts_without_tables = _paddle_ocr(pages_without_tables)

    flat_texts = stitch(texts_with_tables, texts_without_tables, page_classes)

    # unflattens
    unflattened = unflatten(flat_texts, lengths)
    return unflattened

"""
runs pdf_to_text on pdf path supplied as arguments

example (bash) command:
  python runner.py example-docs/23CHLC18998_94523059.pdf
  python runner.py example-docs/23CHLC18998_94523059.pdf example-docs/23CHLC18998_98768329.pdf
  python runner.py example-docs/23CHLC18998_*.pdf
  python runner.py example-docs/*.pdf
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert PDF documents to text with support for glob/regex patterns',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python runner.py example-docs/23CHLC18998_94523059.pdf
  python runner.py example-docs/23CHLC18998_94523059.pdf example-docs/23CHLC18998_98768329.pdf
  python runner.py example-docs/23CHLC18998_*.pdf
  python runner.py example-docs/*.pdf
'''
    )
    parser.add_argument('patterns', nargs='+', 
                        help='Path(s) to PDF file(s) or glob/regex patterns to match PDF files')
    args = parser.parse_args()
    
    # Expand patterns to actual file paths
    pdf_files = expand_patterns(args.patterns)
    
    if not pdf_files:
        print("No PDF files found matching the specified patterns")
        parser.print_help()
        exit(1)
    
    print(f"Processing {len(pdf_files)} PDF file(s):")
    for pdf in pdf_files:
        print(f"  - {pdf}")
    
    result = pdf_to_text(*pdf_files)
    print(result)

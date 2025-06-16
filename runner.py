import argparse
from pdf2image import convert_from_path
from classifier import classify

"""
docs: paths to (multi-page) pdf docs to process
returns
- list per doc of
- list per page of
- text representation of page

Notes:
- Azure parses tables as markdown and checkbox as :selected: and :unselected:

"""
def pdf_to_text(*docs) -> list[list[str]]:
    # maps to pages
    docs_pages = [convert_from_path(doc) for doc in docs]

    # runs classifier on all pages
    table_inds = [classify(doc_pages) for doc_pages in docs_pages]

    # TODO: pages to text

"""
runs pdf_to_text on pdf path supplied as arguments

example (bash) command:
> python runner.py document1.pdf document2.pdf document3.pdf
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert PDF documents to text')
    parser.add_argument('pdfs', nargs='+', help='Path(s) to PDF file(s) to process')
    args = parser.parse_args()
    
    result = pdf_to_text(*args.pdfs)

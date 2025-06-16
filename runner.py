import argparse
import glob
import re
import os
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
    print(table_inds)

    # TODO: pages to text

def expand_patterns(patterns):
    """Expand glob and regex patterns to actual file paths"""
    files = []
    for pattern in patterns:
        # First try glob pattern
        glob_matches = glob.glob(pattern)
        if glob_matches:
            files.extend(glob_matches)
        else:
            # Try regex pattern on all PDF files in current directory
            try:
                regex = re.compile(pattern)
                for root, dirs, filenames in os.walk('.'):
                    for filename in filenames:
                        if filename.endswith('.pdf') and regex.match(filename):
                            files.append(os.path.join(root, filename))
            except re.error:
                # If not a valid regex, treat as literal filename
                if os.path.exists(pattern):
                    files.append(pattern)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_files = []
    for f in files:
        if f not in seen:
            seen.add(f)
            unique_files.append(f)
    
    return unique_files

"""
runs pdf_to_text on pdf path supplied as arguments

example (bash) command:
> python runner.py document1.pdf document2.pdf document3.pdf
> python runner.py "*.pdf"
> python runner.py "doc_[0-9]+\.pdf"
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert PDF documents to text with support for glob/regex patterns',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python runner.py document.pdf
  python runner.py doc1.pdf doc2.pdf doc3.pdf
  python runner.py "*.pdf"
  python runner.py "reports/*.pdf"
  python runner.py "doc_[0-9]+\.pdf"
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

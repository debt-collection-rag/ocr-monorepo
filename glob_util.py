import glob
import re
import os

# expands glob patterns per cmd line args
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
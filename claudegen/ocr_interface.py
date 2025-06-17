"""OCR interface definitions using Protocol (type hints) and simple decorators."""

from typing import Protocol, List, Callable
from PIL import Image
import functools

# Option 1: Using Protocol for type checking (Python 3.8+)
class OCRFunction(Protocol):
    """Protocol defining the OCR function interface."""
    def __call__(self, pages: List[Image.Image]) -> List[str]:
        ...

# Option 2: Type alias for the function signature
OCRFunc = Callable[[List[Image.Image]], List[str]]

# Option 3: Simple decorator for documentation/validation
def ocr_method(func: OCRFunc) -> OCRFunc:
    """Decorator that documents and validates OCR method signature."""
    @functools.wraps(func)
    def wrapper(pages: List[Image.Image]) -> List[str]:
        # Optional: Add validation
        if not isinstance(pages, list):
            raise TypeError(f"Expected list of images, got {type(pages)}")
        
        result = func(pages)
        
        if not isinstance(result, list):
            raise TypeError(f"OCR function must return list of strings, got {type(result)}")
        
        return result
    
    # Mark the function as an OCR method
    wrapper.is_ocr_method = True
    return wrapper

# Option 4: Simple registry pattern
_ocr_methods = {}

def register_ocr(name: str):
    """Register a function as an OCR method."""
    def decorator(func: OCRFunc) -> OCRFunc:
        _ocr_methods[name] = func
        return func
    return decorator

def get_ocr_method(name: str) -> OCRFunc:
    """Get a registered OCR method by name."""
    return _ocr_methods.get(name)

def list_ocr_methods() -> List[str]:
    """List all registered OCR methods."""
    return list(_ocr_methods.keys())

# Example usage:
if __name__ == "__main__":
    # Example with decorator
    @ocr_method
    def dummy_ocr(pages: List[Image.Image]) -> List[str]:
        return ["dummy text"] * len(pages)
    
    # Example with registry
    @register_ocr("dummy")
    def dummy_ocr_registered(pages: List[Image.Image]) -> List[str]:
        return ["dummy text"] * len(pages)
    
    # Type checking works with Protocol
    def process_with_ocr(ocr_func: OCRFunction, pages: List[Image.Image]) -> List[str]:
        return ocr_func(pages)
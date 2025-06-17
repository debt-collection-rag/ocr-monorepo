# Parallel PaddleOCR implementation options

from paddleocr import PaddleOCR
import numpy as np
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import Pool, cpu_count
import threading

# Option 1: Thread-based parallelization (good for I/O bound operations)
def ocr_threaded(pages: list, max_workers: int = 4):
    """Process pages in parallel using threads."""
    paddle_ocr_engine = PaddleOCR(use_angle_cls=True)
    
    def process_page(page):
        page_array = np.array(page)
        result = paddle_ocr_engine.ocr(page_array, cls=True)
        return '\n'.join([line[1][0] for line in result[0]]) if result[0] else ''
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_page, pages))
    
    return results


# Option 2: Process-based parallelization (better for CPU-bound operations)
def _process_page_worker(args):
    """Worker function for multiprocessing."""
    page_array, use_angle_cls = args
    # Each process needs its own PaddleOCR instance
    paddle_ocr = PaddleOCR(use_angle_cls=use_angle_cls)
    result = paddle_ocr.ocr(page_array, cls=True)
    return '\n'.join([line[1][0] for line in result[0]]) if result[0] else ''

def ocr_multiprocess(pages: list, max_workers: int = None):
    """Process pages in parallel using separate processes."""
    if max_workers is None:
        max_workers = min(cpu_count(), len(pages))
    
    # Convert PIL images to numpy arrays
    page_arrays = [(np.array(page), True) for page in pages]
    
    with Pool(processes=max_workers) as pool:
        results = pool.map(_process_page_worker, page_arrays)
    
    return results


# Option 3: Batch processing with single PaddleOCR instance
def ocr_batched(pages: list, batch_size: int = 4):
    """Process pages in batches to reduce overhead."""
    paddle_ocr_engine = PaddleOCR(use_angle_cls=True)
    result_texts = []
    
    for i in range(0, len(pages), batch_size):
        batch = pages[i:i + batch_size]
        for page in batch:
            page_array = np.array(page)
            result = paddle_ocr_engine.ocr(page_array, cls=True)
            result_texts.append('\n'.join([line[1][0] for line in result[0]]) if result[0] else '')
    
    return result_texts


# Option 4: Thread-local PaddleOCR instances for better performance
class ThreadLocalPaddleOCR:
    """Thread-local storage for PaddleOCR instances."""
    def __init__(self):
        self._local = threading.local()
    
    def get_ocr(self):
        if not hasattr(self._local, 'ocr'):
            self._local.ocr = PaddleOCR(use_angle_cls=True)
        return self._local.ocr

thread_local_ocr = ThreadLocalPaddleOCR()

def ocr_thread_local(pages: list, max_workers: int = 4):
    """Process pages with thread-local PaddleOCR instances."""
    def process_page(page):
        ocr_engine = thread_local_ocr.get_ocr()
        page_array = np.array(page)
        result = ocr_engine.ocr(page_array, cls=True)
        return '\n'.join([line[1][0] for line in result[0]]) if result[0] else ''
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_page, pages))
    
    return results


# Option 5: Async processing (if you want to integrate with async code)
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def ocr_async(pages: list, max_workers: int = 4):
    """Async wrapper for parallel OCR processing."""
    loop = asyncio.get_event_loop()
    
    # Use thread pool for CPU-bound operations in async context
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        tasks = []
        for page in pages:
            task = loop.run_in_executor(executor, _process_single_page, page)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
    
    return results

def _process_single_page(page):
    """Helper function for async processing."""
    paddle_ocr = PaddleOCR(use_angle_cls=True)
    page_array = np.array(page)
    result = paddle_ocr.ocr(page_array, cls=True)
    return '\n'.join([line[1][0] for line in result[0]]) if result[0] else ''


# Recommended approach: Hybrid with fallback
def ocr(pages: list, parallel: bool = True, max_workers: int = None):
    """
    Main OCR function with parallel processing support.
    
    Args:
        pages: List of PIL images
        parallel: Whether to use parallel processing
        max_workers: Maximum number of parallel workers
    
    Returns:
        List of extracted text strings
    """
    if not parallel or len(pages) <= 2:
        # Use original sequential processing for small batches
        paddle_ocr_engine = PaddleOCR(use_angle_cls=True)
        result_texts = []
        for page in pages:
            page_array = np.array(page)
            result = paddle_ocr_engine.ocr(page_array, cls=True)
            result_texts.append('\n'.join([line[1][0] for line in result[0]]) if result[0] else '')
        return result_texts
    
    # Use thread-based parallelization for larger batches
    # Threads are preferred over processes for PaddleOCR due to model loading overhead
    return ocr_threaded(pages, max_workers=max_workers or min(4, len(pages)))
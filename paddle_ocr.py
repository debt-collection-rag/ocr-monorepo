# notebook: https://colab.research.google.com/drive/1-obW-2th3xQlAZZuHhcz-B1XTnOLkcAq#scrollTo=Ldo7HuOA5O4M

from paddleocr import PaddleOCR
import numpy as np

def result_to_text(result):
    if result is not None and result[0] is not None:
        return ''.join([line[1][0] for line in result[0]])
    else:
        return ''

paddle_ocr_engine = PaddleOCR(use_angle_cls=True)

def ocr(pages: list):
    result_texts = []
    for i, page in enumerate(pages):
        # print('processing page', i)
        # Convert PIL image to numpy array for PaddleOCR
        page_array = np.array(page)
        result = paddle_ocr_engine.ocr(page_array, cls=True)
        result_texts.append(result_to_text(result))
    return result_texts

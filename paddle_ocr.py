# notebook: https://colab.research.google.com/drive/1-obW-2th3xQlAZZuHhcz-B1XTnOLkcAq#scrollTo=Ldo7HuOA5O4M

from paddleocr import PaddleOCR

def result_to_text(result):
    return '\n'.join([line[1][0] for line in result])

ocr = PaddleOCR(use_angle_cls=True)
def ocr(docs: list):
    result_texts = []
    for i, doc in enumerate(docs):
        print('processing page', i)
        result_texts.append(result_to_text(ocr.ocr(doc, cls=True)))
    return result_texts

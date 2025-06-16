from io import BytesIO

def image_to_bytes(doc):
    # cursor gen
    img_bytes = BytesIO()
    doc.save(img_bytes, format='PNG')  # or 'JPEG' if you prefer
    img_bytes.seek(0)

    return img_bytes
from io import BytesIO

def image_to_bytes(page):
    # cursor gen
    img_bytes = BytesIO()
    page.save(img_bytes, format='PNG')  # or 'JPEG' if you prefer
    img_bytes.seek(0)

    return img_bytes
import pytesseract
from PIL import Image

def solve_captcha(path_img):
    img = Image.open(path_img)

    # Limpieza básica
    img = img.convert("L")
    img = img.point(lambda x: 0 if x < 140 else 255, '1')

    text = pytesseract.image_to_string(img, config="--psm 6 digits")
    text = text.strip().replace(" ", "")

    return text

import pytesseract
from PIL import Image

image = Image.open('../getimage.jpg')
text = pytesseract.image_to_string(image)
print(text)
import pytesseract
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import cv2


filename = "/home/daitama/Desktop/hello/Go5-Project/text_recognition/pytesseract/tests/data/test.png"
image = cv2.imread(filename)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, threshold = cv2.threshold(gray,55, 255, cv2.THRESH_BINARY)
print(pytesseract.image_to_string(threshold))
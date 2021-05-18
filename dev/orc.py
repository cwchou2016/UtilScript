from pdf2image import convert_from_path
from pyzbar.pyzbar import decode
import cv2
import numpy as np

file="demo3.jpg"

img =cv2.imread(file)

for barcode in decode(img):
    print(barcode.data)
    pts = np.array(barcode.polygon, np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.polylines(img, [pts], True,(255,0,255), 5)

cv2.imwrite("out.jpg",img)
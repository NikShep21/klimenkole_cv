import numpy as np
from skimage.measure import regionprops
import cv2
from skimage.morphology import label

def count_pencils(image):
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
 
    lower = np.array([0,  80,  60], dtype=np.uint8)   
    upper = np.array([120,255,200], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower, upper)

    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((10,10)), iterations=2)
    labeled = label(mask)
    regions = regionprops(labeled)

    count = 0
    for region in regions:
       
        if region.area < 130000 or region.eccentricity < 0.995:
            continue
        count += 1

    return count, mask


total = 0
for i in range(1,13):
    img = cv2.imread(f'./images/img ({i}).jpg')
    c, mask = count_pencils(img)
    print(f'Image {i}: {c} pencils')
    total += c
   
   
print("Total pencils:", total)


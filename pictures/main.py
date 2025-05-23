import cv2
import numpy as np

def is_circle(contour, min_circularity=0.7):
    perimeter = cv2.arcLength(contour, True)
    area = cv2.contourArea(contour)
    if perimeter == 0:
        return False
    circularity = 4 * np.pi * (area / (perimeter * perimeter))
    return circularity > min_circularity

def is_my_image(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if hierarchy is None:
        return False

    hierarchy = hierarchy[0]

    for _ , (contour, hier) in enumerate(zip(contours, hierarchy)):
        child = hier[2]
        if child != -1:
            if is_circle(contour) and is_circle(contours[child]):
                return True

    return False

   
cap = cv2.VideoCapture("output.avi")

match_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    if is_my_image(frame):
        match_count += 1


cap.release()
print(f"Количество изображений: {match_count}")


import cv2
import numpy as np
import json
import os
import random

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_EXPOSURE, 1)
capture.set(cv2.CAP_PROP_EXPOSURE, -5)

cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)

def get_color(image):
    x, y, w, h = cv2.selectROI("Color selection", image)
    x, y, w, h = int(x), int(y), int(w), int(h)
    roi = image[y:y+h, x:x+w]
    color = (
        np.median(roi[:, :, 0]),
        np.median(roi[:, :, 1]),
        np.median(roi[:, :, 2]),
    )
    cv2.destroyWindow("Color selection")
    return color

def get_ball(image, color):
    n_lower = (max(color[0] - 8, 0), color[1] * 0.75, color[2] * 0.75)
    n_upper = (min(color[0] + 8, 179), 255, 255)
    mask = cv2.inRange(image, np.array(n_lower, dtype=np.uint8), np.array(n_upper, dtype=np.uint8))
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        contour = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(contour)
        return True, (int(x), int(y), radius, mask)
    return False, (-1, -1, -1, np.array([]))


path = "settings.json"
if os.path.exists(path):
    base_colors = json.load(open(path, "r"))
else:
    base_colors = {}

game_started = False
guess_colors = []

while capture.isOpened():
    ret, frame = capture.read()
    if not ret:
        break

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    key_code = cv2.waitKey(1) & 0xFF
    key = chr(key_code) if key_code != 255 else ""

    if key == "q":
        break

    if key in ["1", "2", "3"]:
        color = get_color(hsv)
        base_colors[key] = color
       

    if key == "r":
        if len(base_colors) == 3:
            random.shuffle(guess_colors)
            print("new:", guess_colors)
            

    
    if len(base_colors) == 3 and not game_started:
        guess_colors = list(base_colors.keys())
        random.shuffle(guess_colors)
        print("guess_colors:", guess_colors)
        game_started = True

    balls = []
    for key_id in base_colors:
        retr, (x, y, radius, mask) = get_ball(hsv, base_colors[key_id])
        if retr:
            cv2.imshow("Mask", mask)
            cv2.circle(frame, (x, y), int(radius), (255, 0, 255), 2)
            balls.append((x, key_id))

    if len(balls) == 3:
        balls.sort()
        detected_order = [key_id for x, key_id in balls]
        if detected_order == guess_colors:
            cv2.putText(frame, "yes", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 4)
        else:
            cv2.putText(frame, "no", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)

    cv2.putText(frame, f"Game started = {game_started}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    cv2.imshow("Camera", frame)


capture.release()
cv2.destroyAllWindows()
json.dump(base_colors, open(path, "w"))
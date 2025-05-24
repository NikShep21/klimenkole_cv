import cv2


cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_EXPOSURE, -4)

glasses = cv2.imread('deal-with-it.png', cv2.IMREAD_UNCHANGED)


eye_cascade = cv2.CascadeClassifier("haarcascade-eye.xml")

while capture.isOpened():
    ret, frame = capture.read()
    if not ret:
        break

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=7)

    if len(eyes) == 2:
        eyes = sorted(eyes, key=lambda e: e[0])
        x1, y1, w1, h1 = eyes[0]
        x2, y2, w2, h2 = eyes[1]

        x = x1
        y = min(y1, y2)
        w = (x2 + w2) - x1
        h = max(y1 + h1, y2 + h2) - y

        resized_glasses = cv2.resize(glasses, (w, h))

        bgr = resized_glasses[:, :, :3]

        gray_glasses = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray_glasses, 100, 255, cv2.THRESH_BINARY_INV)
        mask_inv = cv2.bitwise_not(mask)

        fg = cv2.bitwise_and(bgr, bgr, mask=mask)
        roi = frame[y:y+h, x:x+w]
        bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

        combined = cv2.add(bg, fg)
        frame[y:y+h, x:x+w] = combined

    key = chr(cv2.waitKey(1) & 0xFF)
    if key == 'q':
        break

    cv2.imshow("Camera", frame)

capture.release()
cv2.destroyAllWindows()

import mss
import cv2
import numpy as np
import time
import pyautogui



SCAN_TOP = 33.7
SCAN_WIDTH = 600
SCAN_LEFTR = 330
SCAN_HEIGHT = 40

x_history = []
t_history = []

last_good_speed = None  

def merge_close_rects(rects, gap):
    if not rects:
        return []

    rects = sorted(rects, key=lambda r: r[0])
    merged = []
    cur = rects[0]

    for next_rect in rects[1:]:
        x, y, w, h = next_rect
        if x <= cur[0] + cur[2] + gap:
            new_x = cur[0]
            new_w = max(cur[0] + cur[2], x + w) - new_x
            new_y = min(cur[1], y)
            new_h = max(cur[1] + cur[3], y + h) - new_y
            cur = (new_x, new_y, new_w, new_h)
        else:
            merged.append(cur)
            cur = next_rect
    merged.append(cur)
    return merged

with mss.mss() as sct:
    monitor = sct.monitors[1]
    scan_center_x = monitor["left"] + monitor["width"] // 2
    left = scan_center_x - SCAN_LEFTR
    
    top = monitor["top"] + monitor["height"] * SCAN_TOP // 100
    bbox = {"left": int(left), "top": int(top), "width": SCAN_WIDTH, "height": SCAN_HEIGHT}

    while True:
        frame_time = time.time()
        im = sct.grab(bbox)
        img = np.array(im)
        gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        raw_rects = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 5 and h > 10:
                raw_rects.append((x, y, w, h))

        merged_rects = merge_close_rects(raw_rects, 20)

        if merged_rects:
            merged_rects.sort(key=lambda r: r[0])
            x, y, w, h = merged_rects[0]

            if x_history and abs(x - x_history[-1]) > 50:
                x_history.clear()
                t_history.clear()

            x_history.append(x)
            t_history.append(frame_time)

       
            if len(x_history) > 5:
                x_history.pop(0)
                t_history.pop(0)

            if len(x_history) >= 2:
                dx_total = x_history[0] - x_history[-1]
                dt_total = t_history[-1] - t_history[0]

                if dt_total > 0 and dx_total > 0:
                    raw_speed = dx_total / dt_total

                    
                    if last_good_speed is not None and raw_speed < last_good_speed * 0.3:
            
                        continue

                    speed = raw_speed
                    last_good_speed = speed

                    time_to_hit = x / (speed * 0.85)

                    if time_to_hit < 0.15:
                        pyautogui.keyDown('space')
                        
                        pyautogui.keyUp('space')

                        duck_delay = ((w ** 2.0) * (h ** 0.4)) / (speed ** 3.0) * 400

                      
                        

                        time.sleep(duck_delay)
                        pyautogui.keyDown('down')
                        
                        pyautogui.keyUp('down')

        if cv2.waitKey(1) == 27:
            break

cv2.destroyAllWindows()

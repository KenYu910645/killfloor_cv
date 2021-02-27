'''
Name: get_video_pixel.py
Description: Take a snapshot of a video and get the RGB value
    of any pixel in the snapshot.
Author: Najam Syed (github.com/nrsyed)
Created: 2018-Feb-12
'''

import numpy as np
import cv2
import time

COLOR_ROWS = 160
COLOR_COLS = 500

# capture = cv2.VideoCapture(0)
capture = cv2.VideoCapture('../overcooked_play.mp4')
if not capture.isOpened():
    raise RuntimeError('Error opening VideoCapture.')

(grabbed, frame) = capture.read()
snapshot = np.zeros(frame.shape, dtype=np.uint8)
cv2.imshow('Snapshot', snapshot)

colorArray = np.zeros((COLOR_ROWS, COLOR_COLS, 3), dtype=np.uint8)
cv2.imshow('Color', colorArray)

def on_mouse_click(event, x, y, flags, userParams):
    if event == cv2.EVENT_LBUTTONDOWN:
        colorArray[:] = snapshot[y, x, :]
        rgb = snapshot[y, x, [2,1,0]]

        # HSV convert
        snapshot_hsv = cv2.cvtColor(snapshot, cv2.COLOR_BGR2HSV)
        hsv = snapshot_hsv[y, x, [0,1,2]]

        # From stackoverflow/com/questions/1855884/determine-font-color-based-on-background-color
        # Get text Color 
        luminance = 1 - (0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]) / 255
        if luminance < 0.5:
            textColor = [0,0,0]
        else:
            textColor = [255,255,255]
        
        cv2.putText(colorArray, "(x,y): " + str((x,y)), (20, COLOR_ROWS - 100),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=textColor)
        cv2.putText(colorArray, "RGB:" + str(rgb), (20, COLOR_ROWS - 60),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=textColor)
        cv2.putText(colorArray, "HSV:" + str(hsv), (20, COLOR_ROWS - 20),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=textColor)

        cv2.imshow('Color', colorArray)

cv2.setMouseCallback('Snapshot', on_mouse_click)

while True:
    (grabbed, frame) = capture.read()
    cv2.imshow('Video', frame)

    if not grabbed:
       break

    keyVal = cv2.waitKey(1) & 0xFF
    if keyVal == ord('q'):
        break
    elif keyVal == ord('t'):
        snapshot = frame.copy()
        cv2.imshow('Snapshot', snapshot)
    time.sleep(0.2)

capture.release()
cv2.destroyAllWindows()
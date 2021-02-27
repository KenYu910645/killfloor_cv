import pyautogui
import time 
import math
#目前滑鼠坐標
print (pyautogui.position())
#目前螢幕解析度
print( pyautogui.size() )
#(x,y)是否在螢幕上
x, y = 122, 244
#print (pyautogui.onScreen(x, y))
SCREEN_PATH = [(892, 132), (335, 577), (912, 815), (1609, 530)]

num_seconds = 1.2
pyautogui.moveTo(x, y, duration=num_seconds)

# if __name__ == "__main__":
#     while(True):
#         for path in SCREEN_PATH:
#             pyautogui.moveTo(path[0], path[1], duration=num_seconds)
#             time.sleep(1)
#         # print( pyautogui.position() )
        
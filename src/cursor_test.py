import win32api
from PIL import ImageGrab
import win32con
import win32gui
import numpy as np
import cv2
import time

# def click(x,y): # Mouse control
#     win32api.SetCursorPos((x,y))
#     win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
#     win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
# click(10,10)

def enum_cb(hwnd, results):
    global winlist
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    
def get_screens(screen_name):
    # wait for the program to start initially.
    win32gui.EnumWindows(enum_cb, winlist)
    # string = winlist.__str__()
    # for hwnd, title in winlist:
    #     print(title.lower())
    # idx = string.find("cook")
    # print (string[idx-10:idx+30])
    screens = [(hwnd, title) for hwnd, title in winlist if screen_name in title.lower()]
    while len(screens) == 0:
        screens = [(hwnd, title) for hwnd, title in winlist if screen_name in title.lower()]
        # print (screens)
        win32gui.EnumWindows(enum_cb, winlist)

    return screens

if __name__ == '__main__':
    winlist = []
    screen = 'overcooked2'
    screens = get_screens(screen)

    last_time = time.time()
    cont = True
    while cont:
        if len(get_screens(screen)) <= 0:   # check if closed
            cont = False
            print("[ERROR] Overcooked2 screen closed")
            continue
        # print (screens)
        window = screens[0][0]
        print (window) # 786600
        try:
            print_screen = np.array(ImageGrab.grab(bbox=win32gui.GetWindowRect(window)))
            print (win32gui.GetWindowRect(window))
            print("loop took {} seconds".format(time.time() - last_time))
            last_time = time.time()
            cv2.imshow('window',cv2.cvtColor(print_screen, cv2.COLOR_BGR2RGB))
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
        except Exception as e:
            print("error", e)
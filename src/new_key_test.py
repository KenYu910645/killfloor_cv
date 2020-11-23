import ctypes
import time

SendInput = ctypes.windll.user32.SendInput


class player1():
    def __init__(self):
        self.up_key = 0x11 # W
        self.down_key = 0x1F # S
        self.right_key = 0x20 # A 
        self.left_key = 0x1E # D 
        self.chop_key = 0x10 # Q
        self.pick_key = 0x12 # E
        self.dash_key = 0x13 # R

class player2():
    def __init__(self):
        self.up_key = 0x17 # I 
        self.down_key = 0x25 # K
        self.right_key = 0x26 # LWI
        self.left_key = 0x24 # J
        self.chop_key = 0x16 # U
        self.pick_key = 0x18 # O
        self.dash_key = 0x19 # P

PLAY1 = player1()
PLAY2 = player2()

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008,0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def impluse_key(hexcode, width = 0.0):
    PressKey(hexcode)
    if width != 0.0:
        time.sleep(width)
    ReleaseKey(hexcode)

def test():
    impluse_key(PLAY1.chop_key)
    impluse_key(PLAY2.chop_key)
    time.sleep(0.4)

    # impluse_key(PLAY1.pick_key)
    # impluse_key(PLAY2.pick_key)
    # time.sleep(0.4)

    # impluse_key(PLAY1.dash_key, width = 0.05)
    # impluse_key(PLAY2.dash_key, width = 0.05)
    # time.sleep(0.4)

    # PressKey(PLAY1.up_key)
    # PressKey(PLAY2.up_key)
    # time.sleep(0.5)
    # ReleaseKey(PLAY1.up_key)
    # ReleaseKey(PLAY2.up_key)

    # PressKey(PLAY1.down_key)
    # PressKey(PLAY2.down_key)
    # time.sleep(0.5)
    # ReleaseKey(PLAY1.down_key)
    # ReleaseKey(PLAY2.down_key)

    # PressKey(PLAY1.right_key)
    # PressKey(PLAY2.right_key)
    # time.sleep(0.5)
    # ReleaseKey(PLAY1.right_key)
    # ReleaseKey(PLAY2.right_key)    

    # PressKey(PLAY1.left_key)
    # PressKey(PLAY2.left_key)
    # time.sleep(0.5)
    # ReleaseKey(PLAY1.left_key)
    # ReleaseKey(PLAY2.left_key)

# directx scan codes http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
while (True):
    test()
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
        self.right_key = 0x26 # L
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
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008,10000 , ctypes.pointer(extra) )
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
        t = time.time()
        time.sleep(width)
        ReleaseKey(hexcode)
        return time.time() - t
    ReleaseKey(hexcode)

# directx scan codes http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
summon = 0.0


if __name__ == '__main__':
    while(True):
        ''' summon time sleep test
        dt = impluse_key(PLAY1.up_key, width = 0.17) # 0.15 for 180 degree
        summon += dt
        time.sleep(0.5) # take a rest
        dt = impluse_key(PLAY1.down_key, width = 0.17) # 0.15 for 180 degree
        summon -= dt
        print ("summon: " + str(summon) )
        time.sleep(0.5)
        '''
        '''
        time.sleep(2)
        offset = 0.20 # 0.2 sec to go a single block
        for i in range(5):
            impluse_key(PLAY1.down_key, width = offset) # 0.15 for 180 degree
            time.sleep(0.5)
        for i in range(10):
            impluse_key(PLAY1.right_key, width = offset) # 0.15 for 180 degree
            time.sleep(0.5)
        for i in range(5):
            impluse_key(PLAY1.up_key, width = offset) # 0.15 for 180 degree
            time.sleep(0.5)
        for i in range(10):
            impluse_key(PLAY1.left_key, width = offset) # 0.15 for 180 degree
            time.sleep(0.5)
        '''
        #offset = 0.20
        #impluse_key(PLAY1.up_key, width = offset) # 0.15 for 180 degree
        #impluse_key(PLAY1.right_key, width = offset) # 0.15 for 180 degree
        #impluse_key(PLAY1.down_key, width = offset) # 0.15 for 180 degree
        #impluse_key(PLAY1.left_key, width = offset) # 0.15 for 180 degree
        impluse_key(PLAY1.left_key, width = 0.1) #
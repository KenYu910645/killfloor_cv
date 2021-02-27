import numpy as np
import cv2
import time
import math
from new_key_test import player1, player2, impluse_key, PressKey



# Global variable
# x-axis ->, y-axis |
#                   v
p1_loc = [4.0, 3.0] 
p2_loc = [8.0, 3.0]

PLAY1 = player1()
PLAY2 = player2()

LATTICE_TIME = 0.2 # sec, need 0.2 sec to traval to another lattice
HIP_RADIUS = 0.25 # lattice size, can't go closer to obstacle, 0.2 = 20%

# Player1 aurora
lower_blue = np.array([100, 230, 235]) # HSV
upper_blue = np.array([110, 245, 255]) # HSV
# Player2 aurora
lower_red = np.array([170, 230, 220]) # HSV
upper_red = np.array([180, 250, 255]) # HSV

# create BFMatcher object
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Initiate STAR detector
orb = cv2.ORB_create(nfeatures=50, scoreType=cv2.ORB_FAST_SCORE)
img_fish = cv2.imread("fish.jpg")
# find the keypoints with ORB
kps_fish = orb.detect(img_fish,None)
kps_fish, des_fish = orb.compute(img_fish, kps_fish)
img_fish = cv2.drawKeypoints(img_fish, kps_fish, None, color=(255,255,0), flags=0)
# cv2.imshow("img_fish", img_fish)
cap = cv2.VideoCapture('../overcooked_play.mp4')

orb_frame = cv2.ORB_create(nfeatures=2000, scoreType=cv2.ORB_FAST_SCORE)

# Init map
img_map = cv2.imread("map.png")
map_scale = 50 # N times bigger than original
img_map_enlarge = cv2.resize(img_map, (img_map.shape[1]*map_scale, img_map.shape[0]*map_scale), interpolation = cv2.INTER_AREA) 

def get_centroid(img):
    '''
    '''
    # calculate moments of binary image
    M = cv2.moments(img)

    # calculate x,y coordinate of center
    try:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    except ZeroDivisionError:
        return None
    else:
        return (cX, cY)

def get_marker_point(loc, shape, size):
    '''
    loc - (x,y) location of marker points
    shape - (x,y) shape of the image
    size - int, size of the marker
    '''
    ans = []
    for row in range(loc[1] - math.floor(size/2.0), loc[1] + math.floor(size/2.0)): # row
        for col in range(loc[0] - math.floor(size/2.0), loc[0] + math.floor(size/2.0)): # col
            ans.append((col, row))
    return ans

def check_legal_loc(loc, hip_radius):
    '''
    need img_map
    '''
    left  = (math.floor(loc[0] - hip_radius), math.floor(loc[1]))
    right = (math.floor(loc[0] + hip_radius), math.floor(loc[1]))
    up    = (math.floor(loc[0]), math.floor(loc[1] - hip_radius))
    down  = (math.floor(loc[0]), math.floor(loc[1] + hip_radius))

    if tuple(img_map[left[1]][left[0]]) != (255,255,255): # Left
        print ("Touch Left margin" + str(img_map[left[1]][left[0]]))
        return [loc[0] + hip_radius, loc[1]]
    if tuple(img_map[right[1]][right[0]]) != (255,255,255): # Right
        print ("Touch Right margin")
        return [loc[0] - hip_radius, loc[1]]
    if tuple(img_map[up[1]][up[0]]) != (255,255,255): # Up
        print ("Touch Up margin")
        return [loc[0], loc[1] + hip_radius]
    if tuple(img_map[down[1]][down[0]]) != (255,255,255): # Down
        print ("Touch Down margin" + str(img_map[down[1]][down[0]]))
        return [loc[0], loc[1] - hip_radius]
    return loc


proc_img = np.ones((720,1280,3),np.uint8)*255
last_t = time.time()

while(cap.isOpened()):
    ret, frame = cap.read()  # [row][column][RGB]
    time_start = time.time()

    # Get HSV image
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blue_mask = cv2.inRange(frame_hsv, lower_blue, upper_blue)
    red_mask  = cv2.inRange(frame_hsv, lower_red,  upper_red)
    
    # Get centroid of play1
    centroid = get_centroid(blue_mask)
    try:
        cv2.circle(blue_mask, centroid, 5, (255, 255, 255), -1)
        cv2.putText(blue_mask, "play1", (centroid[0] - 25, centroid[1] - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    except TypeError:
        pass
    
    # Get centroid of play2
    centroid = get_centroid(red_mask)
    try:
        cv2.circle(red_mask, centroid, 5, (255, 255, 255), -1)
        cv2.putText(red_mask, "play2", (centroid[0] - 25, centroid[1] - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    except TypeError:
        pass
    
    # OR operation on maskes
    mask = cv2.bitwise_or(blue_mask, red_mask)

    # Get orders
    order_img = frame[0:100, 0:90]
    print (p1_loc)
    # update players location on map
    left  = (p1_loc[0] - HIP_RADIUS, p1_loc[1])
    right = (p1_loc[0] + HIP_RADIUS, p1_loc[1])
    up    = (p1_loc[0], p1_loc[1] - HIP_RADIUS)
    down  = (p1_loc[0], p1_loc[1] + HIP_RADIUS)

    markers = get_marker_point((int(p1_loc[0] * map_scale), int(p1_loc[1] * map_scale)),
                                img_map_enlarge.shape[:2], 9)
    markers.extend(get_marker_point((int(left[0] * map_scale), int(left[1] * map_scale)), img_map_enlarge.shape[:2], 9))
    markers.extend(get_marker_point((int(right[0] * map_scale), int(right[1] * map_scale)), img_map_enlarge.shape[:2], 9))
    markers.extend(get_marker_point((int(up[0] * map_scale), int(up[1] * map_scale)), img_map_enlarge.shape[:2], 9))
    markers.extend(get_marker_point((int(down[0] * map_scale), int(down[1] * map_scale)), img_map_enlarge.shape[:2], 9))
    
    img_map_loc = img_map_enlarge.copy()
    for i in markers:
        img_map_loc[i[1]][i[0]] = (255,0,0)
    
    # find the keypoints with ORB
    '''
    kps = orb_frame.detect(frame,None)
    kps, des = orb.compute(frame, kps)
    matches = bf.match(des_fish, des)
    print (len(kps))
    print ("matches = " + str(len(matches)))
    
    kps_matched = []
    for i in matches:
       kps_matched.append(kps[i.queryIdx])

    frame = cv2.drawKeypoints(frame, kps_matched, None, color=(255,255,0), flags=0)
    '''

    PressKey(PLAY1.up_key)
    p1_loc[1] -= (time.time() - last_t) / LATTICE_TIME
    # PressKey(PLAY1.down_key)
    # p1_loc[1] += (time.time() - last_t) / LATTICE_TIME
    # PressKey(PLAY1.left_key)
    # p1_loc[0] -= (time.time() - last_t) / LATTICE_TIME
    # PressKey(PLAY1.right_key)
    # p1_loc[0] += (time.time() - last_t) / LATTICE_TIME
    
    last_t = time.time()
    p1_loc = check_legal_loc(p1_loc, HIP_RADIUS)

    time_elasped = time.time() - time_start
    print ("time_elasped : " + str(time_elasped))
    cv2.imshow('mask', mask)
    cv2.imshow('overcooked_gameplay', frame)
    cv2.imshow("img_map_loc", img_map_loc)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
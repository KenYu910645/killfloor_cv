import numpy as np
import cv2
# from cv2 import FeatureDetector_create
import time

# PLAYER1_BULE_BGR = [248, 149, 18] # HSV = [206 degree, 92.7%, 97.3%] -> [145, 236.4, 248.1]
# PLAYER2_RED_BGR = [47, 16, 236]   # HSV = [352 degree, 93.2%, 92.5%]
#threhold = 10

# lower_blue = np.array([140, 230, 240])
# upper_blue = np.array([150, 240, 255])
lower_blue = np.array([100, 230, 235]) # HSV
upper_blue = np.array([110, 245, 255]) # HSV
lower_red = np.array([170, 230, 220]) # HSV
upper_red = np.array([180, 250, 255]) # HSV


# Initiate STAR detector
# orb = cv2.ORB_create(nfeatures=2000, scoreType=cv2.ORB_FAST_SCORE)

# Matcher
# matcher = cv2.DescriptorMatcher_create("BruteForce")
# create BFMatcher object
# bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

cap = cv2.VideoCapture('../overcooked_play.mp4')

# out = cv2.VideoWriter('output.avi', -1, 20.0, (640,480))

kps_last = None
des_last = None
img_last = None
init = False

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

proc_img = np.ones((720,1280,3),np.uint8)*255



while(cap.isOpened()):
    ret, frame = cap.read()  # [row][column][RGB]
    print (frame.shape) # (720, 1280, 3)
    count_p1 = 0
    count_p2 = 0
    time_start = time.time()
 
    time_elasped = time.time() - time_start
    print("count_p1 : " + str(count_p1))
    print("count_p2 : " + str(count_p2))
    print ("time_elasped : " + str(time_elasped))

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
    
    mask = cv2.bitwise_or(blue_mask, red_mask)
    cv2.imshow('mask', mask)
    cv2.imshow('frame_hsv', frame_hsv)
    cv2.imshow('overcooked_gameplay', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    init = True

out.release()
# cap.release()
cv2.destroyAllWindows()
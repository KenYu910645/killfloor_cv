import numpy as np
import cv2
# from cv2 import FeatureDetector_create
import time

# Initiate STAR detector
orb = cv2.ORB_create(nfeatures=2000, scoreType=cv2.ORB_FAST_SCORE)

# Matcher
# matcher = cv2.DescriptorMatcher_create("BruteForce")
# create BFMatcher object
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

cap = cv2.VideoCapture('../kf_gameplay.flv')

out = cv2.VideoWriter('output.avi', -1, 20.0, (640,480))

kps_last = None
des_last = None
img_last = None
init = False
while(cap.isOpened()):
    ret, frame = cap.read()
    

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # find the keypoints with ORB
    kps = orb.detect(gray,None)
    
    filter_kps = []
    for kp in kps:
        (x,y) = (kp.pt[0], kp.pt[1])
        if x < 215 and y < 165:
            continue
        elif x < 202 and y > 606:
            continue
        elif x > 1075 and y > 556:
            continue
        else:
            filter_kps.append(kp)

    # compute the descriptors with ORB
    kps, des = orb.compute(gray, filter_kps)
    print ("raw_kps_num  = " + str(len(kps)))
    # des is a 32 dimension vector
    # print (len(des[0]))
    '''
    rawMatches = matcher.knnMatch(des, des_last, 2)

    matches = []
    for m in rawMatches:
        # print (“#1:{} , #2:{}".format(m[0].distance, m[1].distance))
        if len(m) == 2 and m[0].distance < m[1].distance * 0.8:
            matches.append((m[0].trainIdx, m[0].queryIdx))

    print (matches)
    '''

    if init :
        # Match descriptors.
        matches = bf.match(des,des_last) # des_last is train data
        # Sort them in the order of their distance.
        # matches = sorted(matches, key = lambda x:x.distance)
        # print (len(matches))
        # print (matches[0].queryIdx)
        # Draw first 10 matches.
        kps_correspondance_last = []
        kps_correspondance_new = []
        for i in matches:
            kps_correspondance_new.append(kps[i.queryIdx])
            kps_correspondance_last.append(kps_last[i.trainIdx])
        print ("kps_correspondance_num = " + str(len(kps_correspondance_new)))
        
        kps_moving = []
        for i in range(len(kps_correspondance_new)):
            dx = kps_correspondance_new[i].pt[0] - kps_correspondance_last[i].pt[0]
            dy = kps_correspondance_new[i].pt[1] - kps_correspondance_last[i].pt[1]
            if abs(dx) + abs(dy) > 3:
                kps_moving.append(kps_correspondance_new[i])
                

        # matched_img = cv2.drawMatches(gray,kps,img_last,kps_last,matches[500:],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        matched_img = cv2.drawKeypoints(frame, kps_moving, None, color=(255,0,0), flags=0)
        
    # print (kps[0].angle)

    output_img = cv2.drawKeypoints(frame, kps, None, color=(0,255,0), flags=0)

    cv2.imshow('kf_gameplay',output_img)
    if init:
        cv2.imshow('kf_gameplay_matched',matched_img)
        out.write(matched_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # Flags
    kps_last = kps
    des_last = des
    img_last = gray
    init = True

out.release()
cap.release()
cv2.destroyAllWindows()
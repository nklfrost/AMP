# Standard imports
import time
import cv2
import numpy as np;


import io
import picamera
from picamera.array import PiRGBArray



#setup detector:
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 50
#params.maxThreshold = 255


# Filter by Area.
params.filterByArea = True
params.minArea = 200
params.maxArea = 9000000000

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.6
params.maxCircularity = 1

# Filter by Convexity
params.filterByConvexity = False
params.minConvexity = 0.87

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.5
params.maxInertiaRatio = 1

detector = cv2.SimpleBlobDetector_create(params)


def getPoint():
# grab an image from the camera
    camera = picamera.PiCamera()
    fraction = 0.3
    xres = int(2592*fraction)
    yres = int(1952*fraction)

    camera.resolution = (xres,yres)
    time.sleep(0.1)
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture, 'bgr')
    image = rawCapture.array

    center = image.shape
    x = center[1]/1-xres/1
    y = center[0]/2
    margin= 600*fraction
    #im = image[int(y-margin):int(y+margin), int(x):int(x+xres)]
    im = image

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    #ret,im = cv2.threshold(gray,20,255,0)

    # Detect blobs.
    keypoints = detector.detect(im)
    
    if(len(keypoints)==1):
        pointX = keypoints[0].pt[0]
        pointY = keypoints[0].pt[1]
        #print(f"size is: {keypoints[0].size}")
        #print(f"X: {pointX} Y: {pointY}")
        fromCenter = pointX-(center[1]/2)
        #print(f"{fromCenter} px from center")
        camera.close()
        return [int(fromCenter/fraction),int(keypoints[0].size/fraction)]
    camera.close()
    return [0,0]
print(getPoint())


def runTest():
    print("running test")
    camera = picamera.PiCamera()
    fraction = 0.25
    xres = int(2592*fraction)
    yres = int(1952*fraction)

    camera.resolution = (xres,yres)
    time.sleep(0.1)
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture, 'bgr')
    image = rawCapture.array

    center = image.shape
    x = center[1]/1-xres/1
    y = center[0]/2
    margin= 600*fraction
    im = image[int(y-margin):int(y+margin), int(x):int(x+xres)]

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret,im = cv2.threshold(gray,5,255,0)

    #im = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
     
    # Read image
    #im = cv2.imread("image-small.jpg", 0)
    
    # Detect blobs.
    keypoints = detector.detect(im)
    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imwrite("image-small-cv.jpg", im_with_keypoints)
    print(f"I found {len(keypoints)} blob(s)")
    if(len(keypoints)>0):
        pointX = keypoints[0].pt[0]
        pointY = keypoints[0].pt[1]
        print(f"size is: {keypoints[0].size}")
        print(f"X: {pointX} Y: {pointY}")
        fromCenter = pointX-(center[1]/2)
        print(f"{fromCenter} px from center")
    camera.close()
#runTest()
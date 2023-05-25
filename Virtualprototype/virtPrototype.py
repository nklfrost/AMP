# Standard imports
import cv2
import numpy as np;


#a function that takes an image and returns a quantized image
def quantize(im):
    n = 2    # Number of levels of quantization
    indices = np.arange(0,256)   # List of all colors 
    divider = np.linspace(0,15,n+1)[1] # we get a divider
    quantiz = np.int0(np.linspace(0,255,n)) # we get quantization colors
    color_levels = np.clip(np.int0(indices/divider),0,n-1) # color levels 0,1,2..
    palette = quantiz[color_levels] # Creating the palette
    im2 = palette[im]  # Applying palette on image
    im2 = cv2.convertScaleAbs(im2) # Converting image back to uint8
    #cv2.imshow('im2',im2)
    #cv2.waitKey(0)
    return im2
 

params = cv2.SimpleBlobDetector_Params()
 
# Change thresholds
params.minThreshold = 50
#150 for light
params.maxThreshold = 10000
 
# Filter by Area.
params.filterByArea = True
params.maxArea = 990000
params.minArea = 2000
 
# Filter by Circularity
params.filterByCircularity = True
params.maxCircularity = 0.99
params.minCircularity = 0.72
 
# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.93
 
# Filter by Inertia
params.filterByInertia = False
params.minInertiaRatio = 0.01 


# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create(params)

for i in range(0,20):
    dir = "animation"
    print(dir+"/000" + str(i) + ".jpg")
    # Read image
    if i < 10:
        im = cv2.imread(dir+"/000" + str(i) + ".jpg", cv2.IMREAD_GRAYSCALE)
    else:
        im = cv2.imread(dir+"/00" + str(i) + ".jpg", cv2.IMREAD_GRAYSCALE)
    im = quantize(im)
    # Detect blobs.
    keypoints = detector.detect(im)
    print(len(keypoints))
    for y in range(0, len(keypoints)):
        print(keypoints[y].size)
        size = keypoints[y].size
        fromCenter = keypoints[y].pt[0] - 1920/2
        print(fromCenter)
        org = (int(keypoints[y].pt[0]), int(keypoints[y].pt[1]))
    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
     # font
    font = cv2.FONT_HERSHEY_SIMPLEX
    # org
    # fontScale
    fontScale = 1
    # Blue color in BGR
    color = (255, 0, 0)
    # Line thickness of 2 px
    thickness = 2
    #fromCenter = str(int(size))+" big"
    fromCenter = str(int(fromCenter))+" px from center"
    # Using cv2.putText() method
    image = cv2.putText(im_with_keypoints, fromCenter, org, font, 
                       fontScale, color, thickness, cv2.LINE_AA)
    #save image
    if i < 10:
        cv2.imwrite("animation/result/qu/000" + str(i) + ".jpg", image)
    else:
        cv2.imwrite("animation/result/qu/00" + str(i) + ".jpg", image)

# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)



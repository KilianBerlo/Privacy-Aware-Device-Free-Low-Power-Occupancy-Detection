import cv2
import numpy as np

class person_detection:
    def __init__(self, figure):
        self.figure = figure

    def contour_detection(self, waitkey): 
        imagedef = cv2.imread(self.figure)
        hsv_frame = cv2.cvtColor(imagedef, cv2.COLOR_BGR2HSV)

        low = np.array([0, 0, 220])
        high = np.array([175, 255, 255])
        hsv_mask = cv2.inRange(hsv_frame, low, high)
        
        ## takes all extreme outer contours only, so no contours inside other contours
        contours, hierarchy = cv2.findContours(hsv_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        print("The Total Number of People in the Image = ")
        ##command len used to calculate the number of contours/people in the image
        print (str(len(contours)))
        cv2.drawContours(imagedef, contours, -1,(0,0,0),3)

        cv2.imshow('Image', imagedef)
        cv2.waitKey(waitkey)
        
        if waitkey == 0:
            cv2.destroyAllWindows()

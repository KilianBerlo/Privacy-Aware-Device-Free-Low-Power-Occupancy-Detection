import cv2
import numpy as np

class person_detection:
    """
    Class that detects people in a Heatmap frame
    """
    def __init__(self, figure):
        """
        Constructor for the class detecting people in a Heatmap frame
        
        Parameters:
            figure (string): Indicates the location of the figure that has to be analysed
        """        
        self.figure = figure

    def contour_detection(self, waitkey): 
        """
        Function that aids in the detection of deviating and broken pixels

        Parameters:
            waitkey (int): Indicates when the image window showing the edited figure has to be destroyed
        
        Returns:
            peopleCount (int): Indicates how many people are detected within the figure
        """  
        imagedef = cv2.imread(self.figure)
        hsv_frame = cv2.cvtColor(imagedef, cv2.COLOR_BGR2HSV)

        ## Thresholds for making a distinction between the background and the people present
        low = np.array([0, 0, 220])
        high = np.array([175, 255, 255])
        hsv_mask = cv2.inRange(hsv_frame, low, high)
        
        ## Takes all extreme outer contours only, so no contours inside other contours
        contours, hierarchy = cv2.findContours(hsv_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        print("The Total Number of People in the Image = ")
        ## Command len used to calculate the number of contours/people in the image
        print (str(len(contours)))
        cv2.drawContours(imagedef, contours, -1,(0,0,0),3)

        cv2.imshow('Image', imagedef)
        cv2.waitKey(waitkey)
        
        if waitkey == 0:
            cv2.destroyAllWindows()
        
        return len(contours)

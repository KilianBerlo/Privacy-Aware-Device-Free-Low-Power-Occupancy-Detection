import cv2

class person_detection:
    def __init__(self, figure):
        self.figure = figure

    def contour_detection(self):    
        image = cv2.imread(self.figure, cv2.IMREAD_GRAYSCALE)
        
        ## BLACK AND WHITE
        (ret, thresh) = cv2.threshold(image, 200, 255, 0)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        print("The Total Number of People in the Image = ")
        ##command len used to calculate the number of contours/people in the image
        print (str(len(contours)))
        cv2.drawContours(image, contours, -1,(0,0,0),3)

        cv2.imshow('Image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
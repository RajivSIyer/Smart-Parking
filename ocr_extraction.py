# Import Libraries
import cv2 as cv
import imutils
import numpy as np
import pytesseract
import string

whitelist = string.digits + 'abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ'
text_string = ''

# This Function Extracts Characters from a static imagem
def static_image_ocr(frame,show_process,cropped_lp,cont):
    """ 
    Parameters
    ----------
    frame : Numpy Array
        Image as a numpy py array passed from the main code
    show_process : Boolean
        To display the whole process, if false display only original image and Output image with 
        Detected License Plate number

    Returns
    -------
    text_string : String
        A string which contains the characters recognised from the OCR, in this case the license plate number

    """ 
    image = frame.copy()
    cv.imshow('Original Image',image)

    image = cv.resize(image, (1200,720),interpolation = cv.INTER_AREA )
    
    if cont == True:
        
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY) #convert to gray scale
        gray = cv.bilateralFilter(gray, 11, 17, 17) #Blur to reduce noise 
        edge = cv.Canny(gray, 30, 200) #Perform Edge detection
        
        # Retaining only the contour with number plate
        contours = cv.findContours(edge.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key = cv.contourArea, reverse = True)[:10]
        count = None
        
        # loop over our contours
        for c in contours:
         # approximate the contour
         peri = cv.arcLength(c, True)
         approx = cv.approxPolyDP(c, 0.018 * peri, True)
         
         # if our approximated contour has four points, then
         # we can assume that we have found our screen
         if len(approx) == 4:
          count = approx
          break
        
        if count is None:
         detected = 0
         print("No contour detected")
        else:
         detected = 1
        
        if detected == 1:
         cv.drawContours(image, [count], -1, (0, 255, 0), 3)
        
        # Masking the part other than the number plate
        mask = np.zeros(gray.shape,np.uint8)
        new_image = cv.drawContours(mask,[count],0,255,-1,)
        new_image = cv.bitwise_and(image,image,mask=mask)
        
        # Now crop
        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx+1, topy:bottomy+1]
        # cv.imshow('image',image)
        
        # resize image
        scale_percent = 300 # percent of original size
        width = int(Cropped.shape[1] * scale_percent / 100)
        height = int(Cropped.shape[0] * scale_percent / 100)
        dim = (width, height)
        invert = cv.resize(Cropped, dim, interpolation = cv.INTER_NEAREST)
        
        # To display the whole process
        if show_process == True :
            cv.imshow('Grayscale Image',gray)
            cv.imshow('Bilateral Filter',gray)
            # cv.imshow('Contours', Countured)
            cv.imshow('Canny Edge Detection',edge)
            cv.imshow('Mask',new_image)
            cv.imshow('Cropped',Cropped)
            cv.imshow('Resize', invert)
    
    #invert = cropped_lp
    
    
    
    # Perform OCR on the cropped frame
    text = pytesseract.image_to_string(invert, config='--psm 11')
    
    
    whitelist = string.digits + 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    text_string = ''
    for char in text:
        if char in whitelist:
            text_string += char
        else:
            text_string += ''      
    print("Detected Number is:",text_string)
    # print(text_string)
    
    out = cv.putText(image, text_string, (1000,600), cv.FONT_HERSHEY_SIMPLEX,0.75, (255,255,255), 2, cv.LINE_AA)
    cv.imshow('Output', out)
    cv.waitKey(0)
    cv.destroyAllWindows()
    return text_string
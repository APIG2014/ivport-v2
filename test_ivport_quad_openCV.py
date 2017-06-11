#!/usr/bin/env python

import os
import ivport
import time
import cv2
import IIC
import io
import numpy as np
import imutils # installed using pip
from picamera.array import PiRGBArray

camera_v2=False
board_type=ivport.TYPE_QUAD



def capture_one_image(iv):
    using_file=False
    

    if using_file is False:
        stream = io.BytesIO()
        iv.picam.capture(stream, format='jpeg', use_video_port=True)
            
        # Construct a numpy array from the stream
        data = np.fromstring(stream.getvalue(), dtype=np.uint8)
        # "Decode" the image from the array, preserving colour
        image = cv2.imdecode(data, 1)

        image_new = imutils.resize(image, width=400)
    
    else:
        iv.picam.capture("/tmp/testFile.jpg", use_video_port=True)
        image  = cv2.imread('/tmp/testFile.jpg')
        image_new = imutils.resize(image, width=400)
        image_new = image
    return image_new





def picam_capture_into_files():
    iv = ivport.IVPort(board_type, iv_jumper='A')
    iv.camera_open(camera_v2=camera_v2)
    iv.camera_change(1)
    iv.camera_capture("picam", use_video_port=False)

    iv.camera_change(2)
    iv.camera_capture("picam", use_video_port=False)
    iv.camera_change(3)
    iv.camera_capture("picam", use_video_port=False)
    iv.camera_change(4)
    iv.camera_capture("picam", use_video_port=False)


    img = cv2.imread('picam_CAM1.jpg')
    cv2.imshow( "desparateWindows1" , img)
    img = cv2.imread('picam_CAM2.jpg')
    cv2.imshow( "desparateWindows2" , img)

    print "press any key to exit"
    cv2.waitKey(0)
    print "just read my file"
    time.sleep(0.5)
    cv2.destroyAllWindows()
    iv.close()



def get_one_image_by_cameraId(iv, camera_id):
    
    time.sleep(0.002)
    iv.camera_change(camera_id)
    time.sleep(0.002)

    return capture_one_image(iv)



def windows_name_by_id(id):
    return "picam_%s" % str(id)


# main capture examples
# all of them are functional
def main():
    print "beginning of main"
    if camera_v2 is True:
        iviic = IIC.IIC(addr=(0x70), bus_enable =(0x01))
    print "right after iviic = IIC.IIC...."
    camera_list =  range(1,  5)
    print camera_list
    #picam_capture_into_files()
    #exit()

    iv = ivport.IVPort(board_type, iv_jumper='A')
    print "right after iv = ivport.IVPort(...."
    iv.camera_open(camera_v2=camera_v2)
    print "right after iv.camear_open"
    time.sleep(2.0)
    print "stop to sleep"

    #for i in range(1, 2):
    #   cv2.namedWindow( windows_name_by_id(i) )
    

    while True:
        images={}
        print "right after images = {}"
        
        # first take all the images and store them
        for i in camera_list:
            image_new = get_one_image_by_cameraId(iv, i)
            #cv2.imshow( windows_name_by_id(i) , image_new)
            images[windows_name_by_id(i)] = image_new
            #print "taking new image port %u windows_name:%s" % (i,  windows_name_by_id(i)) 
        
        print "got the images"
        # print all the images
        for i in camera_list:
            image_new = images[windows_name_by_id(i)] 
            cv2.imshow( windows_name_by_id(i) , image_new)
            #images[windows_name_by_id(i)] = image_new

            #print "taking new image port %u windows_name:%s" % (i,  windows_name_by_id(i)) 

        key = cv2.waitKey(1)
        if key == ord("q"): # if the `q` key was pressed, break from the loop 
            break


    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

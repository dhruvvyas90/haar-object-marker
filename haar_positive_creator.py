#!/usr/bin/env python
#################################################################
# Name              : haar_positive_file_creator.py
# Version           : 1.0a
# Date created on   : 11/08/2015
# Date modified on  : 11/08/2015
# Description       : A small python tool to create a postive
#                   : file for haar training
#################################################################

# module imports

import cv2
import sys
import glob

# global variables

debug = 1
obj_list = []
obj_count = 0
click_count = 0
x1 = 0
y1 = 0
h = 0
w = 0
key = None
frame = None

# mouse callback

def obj_marker(event,x,y,flags,param):
    global click_count
    global debug
    global obj_list
    global obj_count
    global x1
    global y1
    global w
    global h
    global frame
    if event == cv2.EVENT_LBUTTONDOWN:
        click_count += 1
        if click_count % 2 == 1:
            x1 = x
            y1 = y
        else:
            w = abs(x1 - x)
            h = abs(y1 - y)
            obj_count += 1
            if x1 > x:
                x1 = x
            if y1 > y:
                y1 = y
            obj_list.append('%d %d %d %d ' % (x1,y1,w,h))
            if debug > 0:
                print obj_list
            cv2.rectangle(frame,(x1,y1),(x1+w,y1+h),(255,0,0),5)
            cv2.imshow('frame',frame)


if len(sys.argv) != 3:
    print 'Usage : python haar_positive_creator.py /path/to/location output_filename.txt'
else:
    if debug > 0:
        print 'Arguments are ok'
        print 'Path is : %s' % sys.argv[1]
        print 'Output file is : %s' % sys.argv[2]
        print 'Click on edges you want to mark as an object'
        print 'Press q to quit'
        print 'Press c to cancel markings'
        print 'Press n to load next image'
    #getting list of jpgs files from
    list = glob.glob('%s/*.jpg' % sys.argv[1])
    if debug > 0:
        print list
    #creating window for frame and setting mouse callback
    cv2.namedWindow('frame',cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback('frame',obj_marker)
    #creating a file handle
    file_name = open(sys.argv[2],"w")
    #loop to traverse through all the files in given path
    for i in list:
        frame = cv2.imread(i)                                                   # reading file
        cv2.imshow('frame',frame)                                               # showing it in frame
        obj_count = 0                                                           #initializing obj_count
        key = cv2.waitKey(0)                                                    # waiting for user key
        while((key & 0xFF != ord('q')) and (key & 0xFF != ord('n'))):           # wait till key pressed is q or n
            key = cv2.waitKey(0)                                                # if not, wait for another key press
            if(key & 0xFF == ord('c')):                                         # if key press is c, cancel previous markings
                obj_count = 0                                                   # initializing obj_count and list
                obj_list = []
                frame = cv2.imread(i)                                           # read original file
                cv2.imshow('frame',frame)                                       # refresh the frame
        if(key & 0xFF == ord('q')):                                             # if q is pressed
            break                                                               # exit
        elif(key & 0xFF == ord('n')):                                           # if n is pressed
            if(obj_count > 0):                                                  # and obj_count > 0
                str1 = '%s %d ' % (i,obj_count)                                 # write obj info in file
                file_name.write(str1)
                for j in obj_list:
                    file_name.write(j)
                file_name.write('\n')
                obj_count = 0
                obj_list = []
    file_name.close()                                                           # end of the program; close the file
cv2.destroyAllWindows()

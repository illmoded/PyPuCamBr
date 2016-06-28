#!/usr/bin/env python

# cap = cv2.VideoCapture('http://<user>:<pass>@<addr>:<port>/videostream.cgi?.mjpg'
# http://92.110.149.150:7777/cam_x.cgi # dużo
# http://71.85.193.254:8888/cam_x.cgi # niewiem
# http://admin:admin@59.177.49.12:8080/cam_%d.cgi # obóz pracy

import cv2
import os
from cam_class import *


camera = Webcam7("92.110.149.150", "7777")

for s in range(1, 24):
    name = "92.110.149.150" + '_' + str(s) + '.png'
    frame = camera.GrabFrame(s)
    if frame is not None:
        cv2.imwrite('capture/' + name, frame)
        FaceDetect(frame, name)
        print("Zrobione %s" % str(s))
    else:
        print("Błąd: Pusty obraz %s" % str(s))

print("END")

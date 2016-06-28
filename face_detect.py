#!/usr/bin/env python

import cv2
import sys
from cam_class import *

cas_profile = cv2.CascadeClassifier(
    '/usr/share/opencv/haarcascades/haarcascade_profileface.xml')
cas_face = cv2.CascadeClassifier(
    '/usr/share/opencv/haarcascades/haarcascade_frontalface_alt2.xml')
cas_eyes = cv2.CascadeClassifier(
    '/usr/share/opencv/haarcascades/haarcascade_eye.xml')


def FaceDetect(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    lProfile = cas_profile.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in lProfile:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    fFace = cas_face.detectMultiScale(
        gray, scaleFactor=1.3, minNeighbors=5, minSize=(20, 20))
    for (x, y, w, h) in fFace:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    lEyes = cas_eyes.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in lEyes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    if len(lProfile) is not 0 or len(fFace) is not 0 or len(lEyes) is not 0:
        cv2.imwrite('detect.png', frame)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        camera = WbudowanyWebcam()
        frame = camera.GrabFrame()

        cv2.imwrite('source.png', frame)
        FaceDetect(frame)
    else:
        frame = cv2.imread(sys.argv[1])
        FaceDetect(frame)

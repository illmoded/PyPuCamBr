import base64
import time
import urllib.request
import urllib.error
import urllib.parse
import requests
from timeout import *
import cv2


cas_profile = cv2.CascadeClassifier(
    '/usr/share/opencv/haarcascades/haarcascade_profileface.xml')
cas_face = cv2.CascadeClassifier(
    '/usr/share/opencv/haarcascades/haarcascade_frontalface_alt2.xml')
cas_eyes = cv2.CascadeClassifier(
    '/usr/share/opencv/haarcascades/haarcascade_eye.xml')


@timeout(60)
def Connect(link):
    return cv2.VideoCapture(link)


def FaceDetect(frame, name):
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
        cv2.imwrite('busted/' + name, frame)
        print('Złapany!')
    else:
        print('Nikogo nie ma... ;(')


class Camera(object):

    def __init__(*arg):
        pass


class ipCamera(Camera):

    def __init__(self, url, user, password):
        self.url = url
        auth_encoded = base64.encodestring('%s:%s' % (user, password))[:-1]

        self.req = urllib.Request(self.url)
        self.req.add_header('Authorization', 'Basic %s' % auth_encoded)

    def __str__(self):
        return str(self.url)
        pass

    def GrabFrame(self):
        response = urllib.urlopen(self.req)
        img_array = np.asarray(bytearray(response.read()), dtype=np.uint8)
        frame = cv2.imdecode(img_array, 1)
        return frame


class WbudowanyWebcam(Camera):

    def __init__(self, camera=0):
        self.cam = cv2.VideoCapture(camera)

        if not self.cam:
            raise Exception("brak dostepu")

        self.shape = self.GrabFrame().shape

    def __str__(self):
        return 'to jest wbudowana kamera...'
        pass

    def GrabFrame(self):
        retval, im = self.cam.read()
        return im


class Webcam7(Camera):
    """Webcam7"""

    def __init__(self, ip, port, user='', password=''):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password

    def GrabFrame(self, src):
        print("Łączę z %s..." % str(src))
        if self.user is '' and self.password is '':
            address = 'http://' + self.ip + ':' + \
                self.port + '/cam_' + str(src) + '.cgi'
        else:
            address = 'http://' + self.user + ':' + self.password + '@' + \
                self.ip + ':' + self.port + '/cam_' + str(src) + '.cgi'

        try:
            cap = Connect(address)
        except:
            print("Błąd: Timeout")
        else:
            print("Otwieranie %s..." % str(src))
            if cap.isOpened():
                ret, frame = cap.read()
                cap.release()
                return frame
            else:
                cap.release()
                print("Błąd: Nie można połączyć się z %s" % str(src))


if __name__ == "__main__":

    kamera = ipCamera()
    obraz = kamera.GrabFrame()

    file = "test.png"
    cv2.imwrite(file, obraz)

    print(kamera)
    del(kamera)
    pass

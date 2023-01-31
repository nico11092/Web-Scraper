import urllib3
from bs4 import BeautifulSoup
import re

import Class.DataClass.Results_Google as Results_Goo

class Google_Scraper():
    def __init__(self, _Param_G):
        self.Param_G = _Param_G
        self.liste_link = []

    def scrap(self):
        http = urllib3.PoolManager()
        r = http.request('GET', self.Param_G.Url)
        soup = BeautifulSoup(r.data, 'html.parser')

        reviews_selector = soup.find_all('div', class_='Gx5Zad fP1Qef xpd EtOod pkphOe')
        for review_selector in reviews_selector:
            review_url = review_selector.find('a', href=True)['href']
            review_url = re.split(r'=|&', review_url)
            url = review_url[1]

            review_titre = review_selector.find('div', class_='BNeawe vvjwJb AP7Wnd').text
            
            review_descr = review_selector.find('div', class_='BNeawe s3v9rd AP7Wnd').text

            review_descr = review_descr.replace("ŕ", "à")
            review_descr = review_descr.replace("č", "è")
            review_descr = review_descr.replace(" ", " ")
            
            if url is not None and review_titre is not None and review_descr is not None :
                result = Results_Goo.Results_G(url, review_titre, review_descr)
                self.liste_link.append(result)

        self.check_language()
        self.check_domaine()

        return self.liste_link

    def check_language(self):
        liste = []
        if self.Param_G.Language != "":

            for i in range(len(self.liste_link)):
                http = urllib3.PoolManager()
                url = self.liste_link[i].Url
                r = http.request('GET', url)
                soup = BeautifulSoup(r.data, 'html.parser')

                lang = soup.find('html')

                if lang['lang'] is not None:
                    if self.Param_G.Language == lang['lang']:
                        liste.append(self.liste_link[i])
            self.liste_link = liste
            

    def check_domaine(self):
        liste = []
        if self.Param_G.Domain != "":
            for i in range(len(self.liste_link)): 
                if self.Param_G.Domain in self.liste_link[i].Url:
                    liste.append(self.liste_link[i])
            self.liste_link = liste

            
                

 
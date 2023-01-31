import urllib3
from bs4 import BeautifulSoup
import re

class Contact_Scraper():
    def __init__(self, _Param_C):
        self.Param_C = _Param_C

        self.link_page = []
        self.info_page = []

        self.info_contact = []

    def scrap(self):
        self.get_link_page()

        self.sort_link_page()

        self.get_info_contact()

        self.sort_info_contact()

        return self.info_contact, self.link_page

    def get_link_page(self):
        http = urllib3.PoolManager()
        r = http.request('GET', self.Param_C.Url)
        soup = BeautifulSoup(r.data, 'html.parser')

        reviews_selector = soup.find_all('a', href=True)
        for review_selector in reviews_selector:
            self.link_page.append(review_selector['href'])

    def sort_link_page(self):
        link = []

        for i in range(len(self.link_page)):
            if "contact" in self.link_page[i]:
                link.append(self.link_page[i])

        self.link_page = (list(set(link)))

    def get_info_contact(self):
        info = []
        for i in range(len(self.link_page)):
            http = urllib3.PoolManager()
            r = http.request('GET', self.link_page[i])
            soup = BeautifulSoup(r.data, 'html.parser')

            reviews_selector = soup.find_all('p')
            for review_selector in reviews_selector:
                info.append(review_selector.text)

            self.info_page.append(info)
            info = []

    def sort_info_contact(self):
        info = []
        for i in range(len(self.info_page)):
            for j in range(len(self.info_page[i])):
                compt = 0
                valeur_max = 0
                for a in range(len(self.info_page[i][j])):
                    if self.info_page[i][j][a].isdigit() or self.info_page[i][j][a] == " ":
                        compt= compt + 1
                        if valeur_max < compt:
                            valeur_max = compt
                    else:
                        if valeur_max < compt:
                            valeur_max = compt
                        compt = 0

                if valeur_max >= 5:
                    info.append(self.info_page[i][j])

            self.info_contact.append(info)
            info = []

        




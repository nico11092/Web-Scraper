from typing import Optional

import Class.ScraperClass.Scraper_google as Google_scraper
import Class.ScraperClass.Scraper_contact as Contact_scraper

class Windows_Scraper():
    def __init__(self, _Param_G : Optional[list] = None, _Param_C : Optional[list] = None) -> None:
        self.Param_G = _Param_G
        self.Param_C = _Param_C

    def search(self):
        myGoogleScraper = Google_scraper.Google_Scraper(self.Param_G)
        return myGoogleScraper.scrap()

    def search_contact(self):
        myContactScraper = Contact_scraper.Contact_Scraper(self.Param_C)
        return myContactScraper.scrap()

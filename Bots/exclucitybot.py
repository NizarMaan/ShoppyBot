"""Shopping bot for ExclucityLife Shopify e-store"""
import webbrowser
import requests
import bs4
from Bots.bot import Bot
from Models.items import Shoes
from settings import Settings

class ExclucityBot(Bot):
    """The class that defines the ExclucityBot's mechanics"""
    def __init__(self, checkout_profiles):
        super().__init__(checkout_profiles)
        settings = Settings()   
        self.baseURL = settings.shopify_store_urls[0]

    def purchase_item(self, item):
        """Parses the Exlucity online store HTML to navigate to the item and purchase it"""
        RawHTML = requests.get(self.baseURL, headers=self.headers)
        print(RawHTML)
        
    #def check_stock(self, item):
        """Parses the store's html to check the stock for a given item"""
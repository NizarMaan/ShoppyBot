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

    #def purchase_item(self, item):
        
    #def check_stock(self, item):

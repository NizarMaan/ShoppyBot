"""Shopping bot for the Yeezy online store"""
import selenium
import time
from Bots.bot import Bot
from Models.items import Shoes
from settings import Settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class YeezyBot(Bot):
    """Initializes a Bot for the Yeezy online store"""
    def __init__(self, checkout_profiles):
        super().__init__(checkout_profiles)
        settings = Settings()
        self.baseURL = settings.other_store_urls[1]
    
    def purchase_item(self, item):
        """Parses the Exlucity online store HTML to navigate to the item and purchase it"""
        start_time = time.time()

        self.browser.get(self.baseURL)
        self.add_to_cart(item)
        self.checkout()

        elapsed_time = time.time() - start_time

        print("Checkout completed in: " + str(elapsed_time) + " seconds.")

    def check_stock(self, item):
        """Parses the given item's html page to check the stock for the desired size"""
        print("checking stock...")

    def add_to_cart(self, item):
        """Adds the given item to the bot's Selenium session cart"""
        print("adding to cart...")

    def checkout(self):
        """Goes through the checkout process for the bot's Selenium session"""
        print("checking out...")

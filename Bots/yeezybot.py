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

        # Yeezy items have a new line character before item names
        new_line_name = "\n" + item.item_name

        try:
            product_link = self.browser.find_element_by_xpath(
                "//a[@title=\"" + new_line_name + "\"]")

            product_link.click()

        except Exception as e:
            raise(ValueError("Item " + item.item_name + " was not found." + str(e)))

        try:
            self.browser.find_element_by_xpath(
                "//option[text()=\"" + str(item.size) + "\"]").click()
        except Exception as e:
            raise(ValueError("Item " + item.item_name +
                             " is not available in size " + str(item.size) + "\n" + str(e)))

    def add_to_cart(self, item):
        """Adds the given item to the bot's Selenium session cart"""
        self.check_stock(item)

        add_to_cart_btn = self.browser.find_element_by_class_name("K__button")

        for i in range(0, item.purchase_quantity):
            add_to_cart_btn.submit()
            time.sleep(0.3)

    def checkout(self):
        """Goes through the checkout process for the bot's Selenium session"""
        self.browser.find_element_by_name("checkout").click()

        limited_stock_btn_continue = None

        try:
            limited_stock_btn_continue = self.browser.find_element_by_name("commit")
            limited_stock = True
        except:
            limited_stock = False
        
        if limited_stock == True:
            print("Purchase quantity was modified as there is limited stock.")
            limited_stock_btn_continue.click()

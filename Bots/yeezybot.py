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
        self.baseURL = settings.other_store_urls[1] + "/collections/men"

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
            time.sleep(0.25)

    def checkout(self):
        """Goes through the checkout process for the bot's Selenium session"""
        checkout_profile = self.checkout_profiles[0]

        self.browser.find_element_by_name("checkout").click()

        limited_stock_btn_continue = None

        try:
            limited_stock_btn_continue = self.browser.find_element_by_name(
                "commit")
            limited_stock = True
        except:
            limited_stock = False

        if limited_stock == True:
            modified_quantity = self.browser.find_element_by_xpath(
                ".//span[@class='page-main__emphasis']").text
            print("Purchase quantity was modified to " +
                  modified_quantity + " as there is limited stock.")
            limited_stock_btn_continue.click()

        email_field = self.browser.find_element_by_name("checkout[email]")
        first_name_field = self.browser.find_element_by_name(
            "checkout[shipping_address][first_name]")
        last_name_field = self.browser.find_element_by_name(
            "checkout[shipping_address][last_name]")
        address_field = self.browser.find_element_by_name(
            "checkout[shipping_address][address1]")
        city_field = self.browser.find_element_by_name(
            "checkout[shipping_address][city]")
        country_dropdown = self.browser.find_element_by_xpath("//option[@data-code=\""
                                                              + checkout_profile.billing_address.country + "\"]")
        province_dropdown = self.browser.find_element_by_xpath("//option[@value=\""
                                                               + checkout_profile.shipping_address.province + "\"]")
        zip_field = self.browser.find_element_by_name(
            "checkout[shipping_address][zip]")
        phone_field = self.browser.find_element_by_name(
            "checkout[shipping_address][phone]")

        email_field.send_keys(checkout_profile.shipping_address.email)
        time.sleep(0.1)

        first_name_field.send_keys(
            checkout_profile.shipping_address.first_name)
        time.sleep(0.5)

        last_name_field.send_keys(checkout_profile.shipping_address.last_name)
        time.sleep(0.1)

        address_field.send_keys(checkout_profile.shipping_address.street)
        time.sleep(0.1)

        city_field.send_keys(checkout_profile.shipping_address.city)
        time.sleep(0.1)

        country_dropdown.click()
        time.sleep(0.1)

        # Province/state dropdown only appears in the DOM after a country is selected
        province_dropdown.click()
        time.sleep(0.1)

        zip_field.send_keys(checkout_profile.shipping_address.postal_code)
        time.sleep(0.1)

        phone_field.send_keys(checkout_profile.shipping_address.phone_number)
        time.sleep(0.1)

        self.browser.find_element_by_xpath(
            ".//input[@id='salesFinal']").click()

        time.sleep(0.1)

        submit_shipping_address = self.browser.find_element_by_class_name(
            "step__footer__continue-btn")
        submit_shipping_address.click()

        time.sleep(0.1)

        # Check whether payment method is available, if not, no shipping to given address
        to_payment_method = None

        to_payment_method = self.browser.find_element_by_class_name(
            "step__footer__continue-btn")
        disabled = to_payment_method.get_attribute("disabled")

        if disabled != None:
            raise ValueError("This item does not ship to your location.")

        to_payment_method.click()

        self.send_keys_to_element_in_iframe("//iframe[@title='Field container for: CARD NUMBER']",
                                            "//input[@data-current-field='number']",
                                            checkout_profile.credit_card.number)

        self.send_keys_to_element_in_iframe("//iframe[@title='Field container for: NAME ON CARD']",
                                            "//input[@data-current-field='name']",
                                            checkout_profile.billing_address.first_name + " " + checkout_profile.billing_address.last_name)

        self.send_keys_to_element_in_iframe("//iframe[@title='Field container for: Expiration date (MM / YY)']",
                                            "//input[@data-current-field='expiry']",
                                            checkout_profile.credit_card.expiration)

        self.send_keys_to_element_in_iframe("//iframe[@title='Field container for: Security code']",
                                            "//input[@data-current-field='verification_value']",
                                            checkout_profile.credit_card.cvv)

        submit_payment_button = self.browser.find_element_by_class_name(
            "step__footer__continue-btn")

        self.browser.find_element_by_xpath(
            ".//input[@data-backup='different_billing_address_false']").click()

        submit_payment_button.click()

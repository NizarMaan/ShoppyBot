"""Shopping bot for ExclucityLife Shopify e-store"""
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


class ExclucityBot(Bot):
    """The class that defines the ExclucityBot's mechanics"""

    def __init__(self, checkout_profiles):
        super().__init__(checkout_profiles)
        settings = Settings()
        self.baseURL = settings.shopify_store_urls[0]

    def purchase_item(self, item):
        """Parses the Exlucity online store HTML to navigate to the item and purchase it"""
        start_time = time.time()

        self.browser.get(self.baseURL + "/collections/men-footwear")
        self.add_to_cart(item)
        self.checkout()

        elapsed_time = time.time() - start_time

        print("Checkout completed in: " + str(elapsed_time) + " seconds.")

    def check_stock(self, item):
        """Parses the given item's html page to check the stock for the desired size"""
        in_stock = True
        size_option_element = None
        size_disabled = None

        try:
            size_option_element = self.browser.find_element_by_xpath(
                ".//option[text()=\"" + str(item.size) + "\"]")
        except:
            in_stock = False

        if size_option_element != None:
            size_disabled = size_option_element.get_attribute("disabled")
            if size_disabled == None:
                in_stock = True

        if in_stock == False:
            raise(ValueError("Item " + item.item_name + " of size " +
                             str(item.size) + " is not in stock or was not found."))

    def add_to_cart(self, item):
        """Adds the product to the bot's Selenium session cart"""
        product_anchor_path = ".//a[text()=\"" + item.item_name + "\"]"
        product_anchor = self.browser.find_element_by_xpath(
            product_anchor_path)
        product_url = product_anchor.get_attribute("href")

        self.browser.get(product_url)

        self.check_stock(item)

        size_option = self.browser.find_element_by_xpath(
            ".//option[@value=\"" + str(item.size) + "\"]")

        size_option.click()

        self.browser.find_element_by_class_name(
            "product__add-to-cart").submit()

    def checkout(self):
        """Goes through the checkout process for the bot's Selenium session"""
        checkout_profile = self.checkout_profiles[0]

        self.browser.find_element_by_class_name(
            "cart__checkout-button").click()

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

        submit_shipping_address = self.browser.find_element_by_class_name(
            "step__footer__continue-btn")
        submit_shipping_address.click()

        time.sleep(0.1)

        to_payment_method = None

        to_payment_method = self.browser.find_element_by_class_name(
            "step__footer__continue-btn")
        disabled = to_payment_method.get_attribute("disabled")

        if disabled != None:
            raise ValueError("This item does not ship to your location.")

        to_payment_method.click()

        self.send_keys_to_element_in_iframe("//iframe[@title='Field container for: Card number']",
                                            "//input[@data-current-field='number']",
                                            checkout_profile.credit_card.number)

        self.send_keys_to_element_in_iframe("//iframe[@title='Field container for: Cardholder name']",
                                            "//input[@data-current-field='name']",
                                            checkout_profile.billing_address.first_name + " " + checkout_profile.billing_address.last_name)

        self.send_keys_to_element_in_iframe("//iframe[@title='Field container for: MM / YY']",
                                            "//input[@data-current-field='expiry']",
                                            checkout_profile.credit_card.expiration)

        self.send_keys_to_element_in_iframe("//iframe[@title='Field container for: CVV']",
                                            "//input[@data-current-field='verification_value']",
                                            checkout_profile.credit_card.cvv)

        submit_payment_button = self.browser.find_element_by_class_name(
            "step__footer__continue-btn")
        submit_payment_button.click()

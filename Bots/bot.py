"""Defines a base class for shopping bots"""
import selenium
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Bot:
    """Parent class for shopping bots that defines common properties"""

    def __init__(self, checkout_profiles):
        self.checkout_profiles = checkout_profiles
        self.purchase_schedule = {}
        browser_options = Options()
        # browser_options.headless = True
        self.browser = selenium.webdriver.Chrome(
            "./Resources/chromedriver.exe", chrome_options=browser_options)
        # Wait 5 seconds for elements to load if an element is not found.
        self.browser.implicitly_wait(5)

    def schedule_purchase(self, run_date, item):
        """Adds a purchase to the schedule dictionary"""
        if self.purchase_schedule.get(run_date) == None:
            self.purchase_schedule[run_date] = [item]
        else:
            self.purchase_schedule[run_date].append(item)

    def add_checkout_profile(self, checkout_profile):
        """Adds a checkout profile to the list of profiles"""
        self.checkout_profiles.append(checkout_profile)

    def get_random_checkout_profile(self):
        """Returns a random checkout profile from the list of checkout profiles"""
        index = random.randint(0, len(self.checkout_profiles))
        return self.checkout_profiles[index]

    def send_keys_to_element_in_iframe(self, xpath_to_iframe, xpath_to_element, keys_to_send):
        """Finds an element within an iframe and sends it some keys then returns to the default page content"""

        WebDriverWait(self.browser, 5).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,
                                                                                        xpath_to_iframe)))
        WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH,
                                                                         xpath_to_element))).send_keys(keys_to_send)

        self.browser.switch_to.default_content()
        time.sleep(0.05)

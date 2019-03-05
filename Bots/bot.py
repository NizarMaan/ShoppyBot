"""Defines a base class for shopping bots"""
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Bot:
    """Parent class for shopping bots that defines common properties"""
    def __init__(self, checkout_profiles):
        self.checkout_profiles = checkout_profiles
        self.purchase_schedule = {}
        browser_options = Options()
        browser_options.headless = True
        self.browser = selenium.webdriver.Chrome("./Resources/chromedriver.exe", chrome_options=browser_options)
        self.browser.implicitly_wait(5) #Wait 5 seconds for elements to load if an element is not found.

    def schedule_purchase(self, run_date, item):
        """Adds a purchase to the schedule dictionary"""
        if self.purchase_schedule.get(run_date) == None:
            self.purchase_schedule[run_date] = [item]
        else:
            self.purchase_schedule[run_date].append(item)
    
    def add_checkout_profile(self, checkout_profile):
        """Adds a checkout profile to the list of profiles"""
        self.checkout_profiles.append(checkout_profile)
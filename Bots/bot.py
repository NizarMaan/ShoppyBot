"""Defines a base class for shopping bots"""
import requests

class Bot:
    """Parent class for shopping bots that defines common properties"""
    def __init__(self, checkout_profiles):
        self.checkout_profiles = checkout_profiles
        self.purchase_schedule = {}
        self.headers =  {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.session = requests.sessions.Session()

    def schedule_purchase(self, run_date, item):
        """Adds a purchase to the schedule dictionary"""
        if self.purchase_schedule.get(run_date) == None:
            self.purchase_schedule[run_date] = [item]
        else:
            self.purchase_schedule[run_date].append(item)
    
    def add_checkout_profile(self, checkout_profile):
        """Adds a checkout profile to the list of profiles"""
        self.checkout_profiles.append(checkout_profile)
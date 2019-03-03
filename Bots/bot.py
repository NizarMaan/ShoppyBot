"""Defines a base class for shopping bots"""
from Models.items import Shoes

class Bot:
    """Parent class for shopping bots that defines common properties"""
    def __init__(self, checkout_profiles):
        self.purchase_schedule = {}
        self.headers =  {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    def schedule_purchase(self, run_date, item):
        """Adds a purchase to the schedule dictionary"""
        if self.purchase_schedule.get(run_date) == None:
            self.purchase_schedule[run_date] = [item]
        else:
            self.purchase_schedule[run_date].append(item)
    
    def get_headers(self):
        return self.headers
    
    def get_purchase_schedule(self):
        return self.purchase_schedule
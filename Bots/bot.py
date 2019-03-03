"""Defines a base class for shopping bots"""
from Models.items import Shoes

class Bot:
    def __init__(self, checkout_profiles):
        self.purchase_schedule = {}
    
    def schedule_purchase(self, run_date, item):
        """Adds a purchase to the schedule dictionary"""
        if self.purchase_schedule.get(run_date) == None:
            self.purchase_schedule[run_date] = [item]
        else:
            self.purchase_schedule[run_date].append(item)
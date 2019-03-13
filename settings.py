"""This module helps handle environment settings"""
import os
import json
from dotenv import load_dotenv


class Settings:
    """A class to initialize and access environment settings."""

    def __init__(self):
        load_dotenv()
        self.max_shoe_size_us = os.environ['MAX_SHOE_SIZE_US']
        self.min_shoe_size_us = os.environ['MIN_SHOE_SIZE_US']
        self.max_shoe_size_eu = os.environ['MAX_SHOE_SIZE_EU']
        self.min_shoe_size_eu = os.environ['MIN_SHOE_SIZE_EU']
        self.max_purchase_quantity = os.environ['MAX_PURCHASE_QUANTITY']
        self.shopify_store_urls = json.loads(os.environ['SHOPIFY_STORE_URLS'])
        self.other_store_urls = json.loads(os.environ['OTHER_STORE_URLS'])
        self.country_size_codes = json.loads(os.environ['COUNTRY_SIZE_CODES'])

    def __str__(self):
        return str(self.__dict__)

"""This module helps handle environment settings"""
import os
import json
from dotenv import load_dotenv

class Settings:
    """A class to initialize and access environment settings."""
    def __init__(self):
        load_dotenv()
        self.max_shoe_size = os.environ['MAX_SHOE_SIZE']
        self.min_shoe_size = os.environ['MIN_SHOE_SIZE']
        self.shopify_store_urls = json.loads(os.environ['SHOPIFY_STORE_URLS'])
        self.other_store_urls = json.loads(os.environ['OTHER_STORE_URLS'])

    def __str__(self):
        return str(self.__dict__)

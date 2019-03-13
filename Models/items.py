"""Defines classes that represent an item to be purchased"""
from settings import Settings


class Item:
    """A base class for purchasable items"""

    def __init__(self, item_name, purchase_quantity):
        self.validate_quantity(purchase_quantity)
        self.item_name = item_name
        self.purchase_quantity = purchase_quantity

    def validate_quantity(self, purchase_quantity):
        settings = Settings()

        if purchase_quantity < 0:
            raise ValueError("Purchase quantity cannot be negative.")
        elif purchase_quantity > int(settings.max_purchase_quantity):
            raise ValueError(
                "Purchase quantity cannot be greater than ten (10).")


class Shoes(Item):
    """A class that represents a shoe to purchase"""

    def __init__(self, item_name, purchase_quantity, size, country_code):
        super().__init__(item_name, purchase_quantity)
        self.size = size
        self.country_code = country_code
        self.validate_size(size)

    def validate_size(self, size):
        settings = Settings()

        found = False
        for code in settings.country_size_codes:
            if code == self.country_code:
                found = True

        if found == False:
            raise ValueError(
                "Invalid country code for shoe size '" + self.country_code + "'")

        if self.country_code == "EU":
            if size > int(settings.max_shoe_size_eu):
                raise ValueError("Shoe size is too big.")
            elif size < int(settings.min_shoe_size_eu):
                raise ValueError("Shoe size is too small.")
        elif self.country_code == "US":
            if size > int(settings.max_shoe_size_us):
                raise ValueError("Shoe size is too big.")
            elif size < int(settings.min_shoe_size_us):
                raise ValueError("Shoe size is too small.")

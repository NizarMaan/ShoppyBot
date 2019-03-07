"""Defines classes required for payment at checkout"""

class CreditCard:
    """Represents a credit card for payment purposes"""
    def __init__(self, number, expiration, cvv):
        self.number = number
        self.expiration = expiration
        self.cvv = cvv

    def set_number(self, number):
        """Sets credit card number to the given number"""
        self.number = number

    def set_expiration(self, expiration):
        """Sets credit card expiration date to the given expiration string"""
        self.expiration = expiration

    def set_cvv(self, cvv):
        """Sets the credit card cvv to the given cvv"""
        self.cvv = cvv

    def __str__(self):
        return str(self.__dict__)

class Address:
    """Represents basic address properties"""
    def __init__(self, first_name, last_name, street,
                 city, province, country, postal_code, phone_number, email):
        self.first_name = first_name
        self.last_name = last_name
        self.street = street
        self.city = city
        self.province = province
        self.country = country
        self.postal_code = postal_code
        self.phone_number = phone_number
        self.email = email

    def __str__(self):
        return str(self.__dict__)

class PaymentOption:
    """Represents a credit card along with its billing address"""
    def __init__(self, billing_address, credit_card):
        self.billing_address = billing_address
        self.credit_card = credit_card

    def __str__(self):
        return str(self.__dict__)

class CheckoutProfile:
    """Represents a set of normally required checkout info"""
    def __init__(self, credit_card, shipping_address, billing_address, payment_option):
        self.credit_card = credit_card
        self.shipping_address = shipping_address
        self.billing_address = billing_address
        self.payment_option = payment_option

    def __str__(self):
        return str(self.__dict__)
    
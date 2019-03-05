"""Shopping bot for ExclucityLife Shopify e-store"""
import selenium
from Bots.bot import Bot
from Models.items import Shoes
from settings import Settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class ExclucityBot(Bot):
    """The class that defines the ExclucityBot's mechanics"""
    def __init__(self, checkout_profiles):
        super().__init__(checkout_profiles)
        settings = Settings()   
        self.baseURL = settings.shopify_store_urls[0]

    def purchase_item(self, item):
        """Parses the Exlucity online store HTML to navigate to the item and purchase it"""
        self.browser.get(self.baseURL + "/collections/men-footwear")
        self.add_to_cart(item)
        self.checkout()
        
    def check_stock(self, item):
        """Parses the given item's html page to check the stock for the desired size"""
        in_stock = True
        size_option_element = None
        size_disabled = None

        try:
            size_option_element = self.browser.find_element_by_xpath(".//option[text()=\"" + str(item.size) + "\"]")
        except:
            in_stock = False
        
        if size_option_element != None:            
            size_disabled = size_option_element.get_attribute("disabled")  
            if size_disabled == None:
                in_stock = True

        if in_stock == False:
            raise(ValueError("Item " + item.item_name + " of size " + str(item.size) + " is not in stock or was not found."))
        
    def add_to_cart(self, item):
        """Adds the product to the bot's Selenium session cart"""
        product_anchor_path = ".//a[text()=\"" + item.item_name + "\"]"
        product_anchor = self.browser.find_element_by_xpath(product_anchor_path)
        product_url = product_anchor.get_attribute("href")

        self.browser.get(product_url)

        self.check_stock(item)

        self.browser.find_element_by_class_name("product__add-to-cart").submit()

    def checkout(self):
        """Goes through the checkout process for the bot's Selenium session"""
        self.browser.find_element_by_class_name("cart__checkout-button").click()
        print(self.browser.find_element_by_name("checkout[email]").get_attribute("id"))

    #deprecated/unused methods
    """
    def get_product_variant_id(self, product_page):
        ""Finds the product's variant id from the given product's html page"
        product_variant_id_html = product_page.find_all("option", attrs={"selected": "selected"})
        product_variant_id = None

        if len(product_variant_id_html) > 0:
            for element in product_variant_id_html:
                if element.has_attr("data-sku"):
                    product_variant_id = element["value"]

        if product_variant_id == None:
            raise(ValueError("Unable to parse HTML to find item's variant id."))

        return product_variant_id

    def add_to_cart(self, product_variant_id, size):
        ""Adds the product to the bot's session's cart""
        cart_endpoint = "https://shop.exclucitylife.com/cart/add.js"

        payload = {
           "id": product_variant_id,
           "variant_title": size,
           "variant_options": [size]
        }

        response = self.session.post(cart_endpoint, payload)

        if response.status_code != 200:
            raise ValueError("Error adding product to cart:\n\t" + response.text)
    """
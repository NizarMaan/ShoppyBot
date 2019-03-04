"""Shopping bot for ExclucityLife Shopify e-store"""
import webbrowser
import requests
import selenium
import bs4
from Bots.bot import Bot
from Models.items import Shoes
from settings import Settings
from selenium import webdriver

class ExclucityBot(Bot):
    """The class that defines the ExclucityBot's mechanics"""
    def __init__(self, checkout_profiles):
        super().__init__(checkout_profiles)
        settings = Settings()   
        self.baseURL = settings.shopify_store_urls[0]

    def purchase_item(self, item):
        """Parses the Exlucity online store HTML to navigate to the item and purchase it"""
        rawHTML = self.session.get(self.baseURL + "/collections/men-footwear", headers=self.headers)
        page = bs4.BeautifulSoup(rawHTML.text, "lxml")
        product_titles = page.find_all("h4", attrs={"class":"product-item__title"})

        product_page = None

        for product_title in product_titles:
            product_name = product_title.find("a").contents[0]

            if product_name == item.item_name:
                product_url = product_title.find("a")["href"]
                product_page = bs4.BeautifulSoup(self.session.get(self.baseURL+product_url, headers=self.headers).text, "lxml")
                break

        if product_page == None:
            raise(ValueError("Item " + item.item_name + " was not found."))
        
        self.check_stock(product_page, item)

        product_variant_id = self.get_product_variant_id(product_page)

        self.add_to_cart(product_variant_id, item.size)

        self.session.close()

        browser = selenium.webdriver.Chrome("./Resources/chromedriver.exe")
        browser.get(self.baseURL + "/collections/men-footwear")

    def check_stock(self, product_page, item):
        """Parses the given item's html page to check the stock"""
        in_stock = True
        size_option_html = product_page.find_all("option", attrs={"value":item.size})
 
        if len(size_option_html) > 0:
            if size_option_html[0].has_attr("disabled"):
                in_stock = False
        else:
            in_stock = False

        if(in_stock == False):
            raise(ValueError("Item " + item.item_name + " of size " + str(item.size) + " is not in stock"))

        return in_stock
    
    def get_product_variant_id(self, product_page):
        """Finds the product's variant id from the given product's html page"""
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
        """Adds the product to the bot's session's cart"""
        cart_endpoint = "https://shop.exclucitylife.com/cart/add.js"

        payload = {
           "id": product_variant_id,
           "variant_title": size,
           "variant_options": [size]
        }

        response = requests.post(cart_endpoint, payload)

        if response.status_code != 200:
            raise ValueError("Error adding product to cart:\n\t" + response.text)

    def checkout(self):
        """Goes through the checkout process for the bot's session"""
"""Shopping bot for ExclucityLife Shopify e-store"""
import webbrowser
import requests
import bs4
from Bots.bot import Bot
from Models.items import Shoes
from settings import Settings

class ExclucityBot(Bot):
    """The class that defines the ExclucityBot's mechanics"""
    def __init__(self, checkout_profiles):
        super().__init__(checkout_profiles)
        settings = Settings()   
        self.baseURL = settings.shopify_store_urls[0]

    def purchase_item(self, item):
        """Parses the Exlucity online store HTML to navigate to the item and purchase it"""
        rawHTML = requests.get(self.baseURL + "/collections/men-footwear", headers=self.headers)
        page = bs4.BeautifulSoup(rawHTML.text, "lxml")
        product_titles = page.find_all("h4", attrs={"class":"product-item__title"})

        product_page = None

        for product_title in product_titles:
            product_name = product_title.find("a").contents[0]

            if product_name == item.item_name:
                product_url = product_title.find("a")["href"]
                product_page = bs4.BeautifulSoup(requests.get(self.baseURL+product_url, headers=self.headers).text, "lxml")
                break

        if product_page == None:
            raise(ValueError("Item " + item.item_name + " was not found."))
        
        self.check_stock(product_page, item)
    
    def check_stock(self, product_page, item):
        """Parses the product's html page to check the stock for a given item"""
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
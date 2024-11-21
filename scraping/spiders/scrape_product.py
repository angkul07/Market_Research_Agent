from collections.abc import Iterable
from urllib.parse import urljoin
import scrapy
import re

# product = input("enter the product name: ")

# product = re.sub(r'(?<=\d) (?=\d)', '-', product)
# product = product.replace(' ', '+')

# user_url = "https://www.amazon.in/s?k="+"product"
list = []

class SearchList(scrapy.Spider):
    name = "scrape_product"

    """This will not work because Scrapy crawl are not for runtime input()"""
    # def start_requests(self):
    #     urls = user_url
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def __init__(self, product_name=None, *args, **kwargs):
        super(SearchList, self).__init__(*args, **kwargs)
        self.product_name = product_name

    def start_requests(self):
        # Construct the URL using the input product name
        product = re.sub(r'(?<=\d) (?=\d)', '-', self.product_name)
        product = product.replace(' ', '+')
        url = f"https://www.amazon.in/s?k={product}"
        
        yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, respone):
        # review_elements = respone.css("h2.a-size-mini a")
        review_elements = respone.css("div")
        # for review_element in review_elements:
        #     if review_element.css("div.attrib[data-asin]") != '':
        #         yield {
        #             "title": review_element
        #         }

        # for review_element in respone.css("div::attr(data-asin)").getall():
        #     if review_element.css("div::attr(data-asin)") != '':
        #         yield {
        #             "title": review_element
        #         }

        for review_element in review_elements:
            # Extract the 'data-asin' attribute value
            data_asin = review_element.css("div::attr(data-asin)").get()

            # Only process elements where 'data-asin' is not empty
            if data_asin:
                yield {
                    # "title": review_element.get(),
                    "asin": data_asin
                }

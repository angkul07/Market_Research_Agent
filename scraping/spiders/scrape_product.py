from collections.abc import Iterable
from urllib.parse import urljoin
import scrapy
import re


class SearchList(scrapy.Spider):
    name = "scrape_product"

    def __init__(self, product_name=None, *args, **kwargs):
        super(SearchList, self).__init__(*args, **kwargs)
        self.product_name = product_name

    def start_requests(self):
        product = re.sub(r'(?<=\d) (?=\d)', '-', self.product_name)
        product = product.replace(' ', '+')
        url = f"https://www.amazon.in/s?k={product}"

        for i in range(1, 5):
            url = f"https://www.amazon.in/s?k={product}&page={i}"
            yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, respone):
        review_elements = respone.css("div")

        for review_element in review_elements:
            data_asin = review_element.css("div::attr(data-asin)").get()
            if data_asin:
                yield {
                    data_asin
                }

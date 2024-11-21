import scrapy
from urllib.parse import urljoin
import re
import csv
from playwright.sync_api import sync_playwright

selectors = {
    "emailid": 'input[name=email]',
    "password": 'input[name=password]',
    "continue": 'input[id=continue]',
    "signin": 'input[id=signInSubmit]',
}

signin_url = "https://www.amazon.in/-/hi/ap/signin?openid.pape.max_auth_age=3600&openid.return_to=https%3A%2F%2Fwww.amazon.in%2Fspr%2Freturns%2Fgift&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=amzn_psr_desktop_in&openid.mode=checkid_setup&language=en_IN&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"  # Replace with the actual sign-in URL

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Set headless=True for no UI
    page = browser.new_page()

    # Navigate to the sign-in URL
    page.goto(signin_url)

    # Wait for the email input field to appear and type the email
    page.wait_for_selector(selectors["emailid"])
    page.type(selectors["emailid"], "angkulatheist07@gmail.com", delay=100)

    # Click the "Continue" button
    page.click(selectors["continue"])

    # Wait for the password field to appear and type the password
    page.wait_for_selector(selectors["password"])
    page.type(selectors["password"], "EA@&9qQYr$hEV62", delay=100)

    # Click the "Sign In" button
    page.click(selectors["signin"])

    # Wait for navigation after signing in
    page.wait_for_navigation()

    # Close the browser
    browser.close()

class AmazonReviews(scrapy.Spider):
    name = "scrape_review"

    def start_requests(self):
        with open('/home/angkul/my_data/coding/python/lightinig_ai/scraping/data.csv', mode='r') as file:
            csvfile = str(csv.reader(file))

            for data in csvfile:
                # url = f"https://www.amazon.in/product-reviews/{data}"
                url = f"https://www.amazon.in/dp/{data}"

                # for i in range(1, 6):
                #     url = f"https://www.amazon.in/product-reviews/{data}/ref=cm_cr_arp_d_paging_btm_next_{i}?pageNumber={i}"
                yield scrapy.Request(url=url, callback=self.parseReview)

    def parseReview(self, response):
        reviews = response.css('div[data-hook="review"]')  # Select each review block
        for review in reviews:
            # Extract the review text
            review_text = review.css('span[data-hook="review-body"] span::text').get()
            
            # Extract the review rating
            rating = review.css('i[data-hook="review-star-rating"] span::text').get()
            
            # Extract the review title (optional)
            title = review.css('a[data-hook="review-title"] span::text').get()
            
            # Extract the reviewer name (optional)
            reviewer_name = review.css('span.a-profile-name::text').get()

            yield {
                'review_text': review_text,
                'rating': rating,
                'title': title,
                'reviewer_name': reviewer_name,
            }



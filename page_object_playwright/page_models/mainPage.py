from page_object.page_object_playwright.page_models.basicPage import BasicPage
import time
import re


class MainPage(BasicPage):
    def __init__(self, page):
        super().__init__(page)

    locator_dictionary = {
      "sign_in_button": 'a.login',
      "search_input": '#search_query_top',
      "search_button": 'button.button-search',
      "products": 'ul.product_list li',
      "prices": 'ul.product_list li .product-price',
      "add_to_cart_button": "text='Add to cart'",
      "proceed_to_checkout_button": "text='Proceed to checkout'"
    }

    def click_sign_in(self):
        """
        A function that go to login page
        """
        self._page.locator(self.locator_dictionary["sign_in_button"]).click()
        return self._page

    def fill_search_input(self, text: str):
        """
        A function that fill the search input on the page with a text
        :param text: str
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string!")
        self._page.locator(self.locator_dictionary["search_input"]).fill(text)

    def click_search_button(self):
        """
        A function that clicks the search button
        """
        self._page.locator(self.locator_dictionary["search_button"]).click()

    def search_results_header(self, text) -> str:
        """
        A function that returns the header title of the search results
        :return: str, the header title
        """
        return self._page.locator(f"h1.page-heading:has-text('{text}')").inner_html()

    def find_cheapest_product(self) -> tuple:
        """
        A function that find the cheapest product from list of products and return it and its price
        """
        products = self._page.locator(self.locator_dictionary["products"])
        prices = self._page.locator(self.locator_dictionary["prices"])
        time.sleep(2)
        prices_list = []
        for price in prices.all_inner_texts():
            prices_list.append(re.sub('[^\d\.]', "", price))
        cheapest = products.locator(f".product-container:has-text('${(min(prices_list))}')")
        return cheapest, min(prices_list)

    def hover_product_and_add_to_cart(self, product):
        """
        A function that hover on the given product and add it to the cart
        :param product: A WebDriver element
        """
        product.hover()
        self._page.wait_for_timeout(3000)
        product.locator(self.locator_dictionary["add_to_cart_button"]).click()

    def click_proceed_to_checkout(self):
        """
        A function that clicks on the checkout button that leads to the order page
        """
        self._page.locator(self.locator_dictionary["proceed_to_checkout_button"]).click()
        return self._page

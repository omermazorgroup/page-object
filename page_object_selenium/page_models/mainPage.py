from page_object.page_object_selenium.page_models.basicPage import BasicPage
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import re


class MainPage(BasicPage):
    def __init__(self, driver):
        super().__init__(driver)

    locator_dictionary = {
      "sign_in_button": (By.CSS_SELECTOR, 'a.login'),
      "search_input": (By.ID, "search_query_top"),
      "search_button": (By.CSS_SELECTOR, 'button.button-search'),
      "search_results_header": (By.CSS_SELECTOR, "#center_column>h1"),
      "products": (By.CLASS_NAME, "product-container"),
      "prices": (By.CSS_SELECTOR, "span.product-price"),
      "right_block": (By.CLASS_NAME, "right-block"),
      "content_price": (By.CLASS_NAME, "content_price"),
      "price": (By.CLASS_NAME, "price"),
      "add_to_cart_button": (By.CSS_SELECTOR, 'a.ajax_add_to_cart_button'),
      "proceed_to_checkout_button": (By.CSS_SELECTOR,
          "#layer_cart > div.clearfix > div.layer_cart_cart > div.button-container > a")
    }

    def click_sign_in(self):
        """
        A function that go to login page
        """
        self._driver.find_element(*self.locator_dictionary["sign_in_button"]).click()
        return self._driver

    def fill_search_input(self, text: str):
        """
        A function that fill the search input on the page with a text
        :param text: str
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string!")
        self._driver.find_element(*self.locator_dictionary["search_input"]).send_keys(text)

    def click_search_button(self):
        """
        A function that clicks the search button
        """
        self._driver.find_element(*self.locator_dictionary["search_button"]).click()

    def search_results_header(self) -> str:
        """
        A function that returns the header title of the search results
        :return: str, the header title
        """
        return self._driver.find_element(*self.locator_dictionary["search_results_header"]).text

    def find_cheapest_product(self) -> tuple | None:
        """
        A function that find the cheapest product from list of products and return it and its price
        """
        products = self._driver.find_elements(*self.locator_dictionary["products"])
        prices = self._driver.find_elements(*self.locator_dictionary["prices"])
        time.sleep(1)
        prices_list = []
        for price in prices:
            prices_list.append(re.sub('[^\d\.]', "", price.text))
        prices_list = list(filter(None, prices_list))
        for product in products:
            right_block = product.find_element(*self.locator_dictionary["right_block"])
            content_price = right_block.find_element(*self.locator_dictionary["content_price"])
            price = content_price.find_element(*self.locator_dictionary["price"]).text
            price_num = str(price[1:len(price)])
            if min(prices_list) == price_num:
                return product, min(prices_list)
        return None

    def hover_product_and_add_to_cart(self, product):
        """
        A function that hover on the given product and add it to the cart
        :param product: A WebDriver element
        """
        actions = ActionChains(self._driver)
        actions.move_to_element(product).perform()
        product.find_element(*self.locator_dictionary["add_to_cart_button"]).click()

    def click_proceed_to_checkout(self):
        """
        A function that clicks on the checkout button that leads to the order page
        """
        self._driver.find_element(*self.locator_dictionary["proceed_to_checkout_button"]).click()
        return self._driver

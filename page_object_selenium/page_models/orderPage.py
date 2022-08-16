from selenium import webdriver
from selenium.webdriver.common.by import By
from page_object.page_object_selenium.page_models.basicPage import BasicPage


class OrderPage(BasicPage):
    def __init__(self, driver: webdriver):
        super().__init__(driver)

    locator_dictionary = {
        "summary_checkout_button": (By.CLASS_NAME, "standard-checkout"),
        "address_checkout_button": (By.CSS_SELECTOR, '[name=processAddress]'),
        "agree_to_terms_checkbox": (By.CSS_SELECTOR, 'input#cgv'),
        "shipping_checkout_button": (By.CSS_SELECTOR, '[name=processCarrier]'),
        "total_price": (By.ID, "total_product"),
        "pay_button": (By.CLASS_NAME, "bankwire"),
        "confirm_order_button": (By.CSS_SELECTOR, "#cart_navigation > button")
    }

    def perform_order_process(self):
        """
        A function that performs the ordering process
        """
        self._driver.find_element(*self.locator_dictionary["summary_checkout_button"]).click()
        self._driver.find_element(*self.locator_dictionary["address_checkout_button"]).click()
        self._driver.find_element(*self.locator_dictionary["agree_to_terms_checkbox"]).click()
        self._driver.find_element(*self.locator_dictionary["shipping_checkout_button"]).click()

    def total_price(self) -> str:
        """
        A function that returns the total price as shown on the page
        :return: str
        """
        return self._driver.find_element(*self.locator_dictionary["total_price"]).text

    def pay_and_complete_the_order(self):
        """
        A function that perform the payment and complete the order
        """
        self._driver.find_element(*self.locator_dictionary["pay_button"]).click()
        self._driver.find_element(*self.locator_dictionary["confirm_order_button"]).click()

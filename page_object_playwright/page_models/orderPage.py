from page_object.page_object_playwright.page_models.basicPage import BasicPage


class OrderPage(BasicPage):
    def __init__(self, page):
        super().__init__(page)

    locator_dictionary = {
        "summary_checkout_button": "#center_column >> text='Proceed to checkout'",
        "address_checkout_button": "button >> text='Proceed to checkout'",
        "agree_to_terms_checkbox": "input#cgv",
        "shipping_checkout_button": "button >> text='Proceed to checkout'",
        "total_price": "#total_product",
        "pay_button": "text='Pay by bank wire'",
        "confirm_order_button": "button >> text='I confirm my order'"
    }

    def perform_order_process(self):
        """
        A function that performs the ordering process
        """
        self._page.locator(self.locator_dictionary["summary_checkout_button"]).click()
        self._page.locator(self.locator_dictionary["address_checkout_button"]).click()
        self._page.locator(self.locator_dictionary["agree_to_terms_checkbox"]).click()
        self._page.locator(self.locator_dictionary["shipping_checkout_button"]).click()

    def total_price(self) -> str:
        """
        A function that returns the total price as shown on the page
        :return: str
        """
        return self._page.locator(self.locator_dictionary["total_price"]).inner_text()

    def pay_and_complete_the_order(self):
        """
        A function that perform the payment and complete the order
        """
        self._page.locator(self.locator_dictionary["pay_button"]).click()
        self._page.locator(self.locator_dictionary["confirm_order_button"]).click()

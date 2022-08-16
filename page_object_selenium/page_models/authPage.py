from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from page_object.page_object_selenium.page_models.basicPage import BasicPage


class AuthPage(BasicPage):
    def __init__(self, driver: webdriver):
        super().__init__(driver)

    locator_dictionary = {
      "email_input": (By.ID, "email"),
      "password_input": (By.ID, "passwd"),
      "submit_button": (By.ID, "SubmitLogin"),
      "forgot_password": (By.XPATH, '//a[text()="Forgot your password?"]')
    }

    def submit_form(self, email: str, password: str):
        """
        A function that fill email input and password input and then submit the form
        :param email: str
        :param password: str
        """
        if not isinstance(email, str):
            raise TypeError("email must be a string!")
        if not isinstance(password, str):
            raise TypeError("email must be a string!")
        self._driver.find_element(*self.locator_dictionary["email_input"]).send_keys(email)
        self._driver.find_element(*self.locator_dictionary["password_input"]).send_keys(password)
        self._driver.find_element(*self.locator_dictionary["submit_button"]).click()

    def click_forgot_password(self):
        self._driver.find_element(*self.locator_dictionary["forgot_password"]).click()


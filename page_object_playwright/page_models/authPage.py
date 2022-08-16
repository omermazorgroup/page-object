from page_object.page_object_playwright.page_models.basicPage import BasicPage


class AuthPage(BasicPage):
    def __init__(self, page):
        super().__init__(page)

    locator_dictionary = {
      "email_input": "input#email",
      "password_input": "input#passwd",
      "submit_button": "#SubmitLogin",
      "forgot_password": 'text=Forgot your password?'
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
        self._page.locator(self.locator_dictionary["email_input"]).fill(email)
        self._page.locator(self.locator_dictionary["password_input"]).fill(password)
        self._page.locator(self.locator_dictionary["submit_button"]).click()

    def click_forgot_password(self):
        self._page.locator(self.locator_dictionary["forgot_password"]).click()

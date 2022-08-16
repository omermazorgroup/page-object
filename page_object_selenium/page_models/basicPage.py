from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class BasicPage:
    def __init__(self, driver: webdriver):
        self._driver = driver

    locator_dictionary = {
      "body": (By.TAG_NAME, 'body')
    }

    @property
    def driver(self):
        """Gets the driver of this Model.
        :return: The driver of this Model.
        """
        return self._driver

    def text(self) -> str:
        """
        A function that return all the text inside the page
        :return: str
        """
        return self._driver.find_element(By.TAG_NAME, 'body').text

    def text_is_inside(self, text: str) -> bool:
        """
        A function that check if the text is inside the page or not
        :param text: str
        :return: True if the text is inside the page, False if not
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string!")
        return text in self.text()

    def url(self):
        """
        A function that return the url of the page
        :return:
        """
        return self._driver.current_url

    def close_page(self):
        """
        A function that close the page
        """
        self._driver.close()

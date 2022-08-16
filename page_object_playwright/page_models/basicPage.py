class BasicPage:
    def __init__(self, page):
        self._page = page

    @property
    def driver(self):
        """Gets the driver of this Model.
        :return: The driver of this Model.
        """
        return self._page

    def text(self) -> str:
        """
        A function that return all the text inside the page
        :return: str
        """
        return self._page.locator('body').inner_html()

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
        return self._page.url

    def close_page(self):
        """
        A function that close the page
        """
        self._page.close()

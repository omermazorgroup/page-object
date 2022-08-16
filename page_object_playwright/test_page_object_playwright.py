import time
import pytest
from page_models.mainPage import MainPage
from page_models.authPage import AuthPage
from page_models.orderPage import OrderPage
from playwright.sync_api import sync_playwright
import re
import logging
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
mylogger = logging.getLogger()


@pytest.fixture
def user():
    return {
      "email": "omermazor144@gmail.com",
      "password": "12345"
    }


def enter_main_page(playwright) -> MainPage:
    """
    A function that go to main page
    :param playwright:
    """
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://automationpractice.com/index.php")
    return MainPage(page)


def validate_input(email, password, text):
    with sync_playwright() as playwright:
        main_page = enter_main_page(playwright)
        time.sleep(2)
        auth_page = AuthPage(main_page.click_sign_in())
        time.sleep(2)
        auth_page.submit_form(email, password)
        time.sleep(2)
        return auth_page.text_is_inside(text)


def test_no_email(user):
    mylogger.info("test for empty email input")
    assert validate_input("", user["password"], "An email address required")
    mylogger.info("text succeeded!")


def test_fake_email(user):
    mylogger.info("test for invalid email input")
    assert validate_input("omermazor144@gmail", user["password"], "Invalid email address")
    mylogger.info("text succeeded!")


def test_no_password(user):
    mylogger.info("test for empty password input")
    assert validate_input(user["email"], "", "Password is required")
    mylogger.info("text succeeded!")


def test_invalid_password(user):
    mylogger.info("test for invalid password input")
    assert validate_input(user["email"], "1234", "Invalid password")
    mylogger.info("text succeeded!")


def test_fake_authentication():
    mylogger.info("test for unregistered input")
    assert validate_input("omermazor144@gmail.com", "123456", "Authentication failed")
    mylogger.info("text succeeded!")


def test_valid_authentication(user):
    mylogger.info("test for registered user")
    assert validate_input(user["email"], user["password"], "Welcome to your account")
    mylogger.info("text succeeded!")


def test_click_forgot_password():
    mylogger.info("test for click on forgot password button")
    with sync_playwright() as playwright:
        main_page = enter_main_page(playwright)
        auth_page = AuthPage(main_page.click_sign_in())
        time.sleep(2)
        auth_page.click_forgot_password()
        time.sleep(2)
        assert auth_page.url() == "http://automationpractice.com/index.php?controller=password"
        mylogger.info("text succeeded!")
        auth_page.close_page()


def test_buy_cheapest_summer_dress(user):
    mylogger.info("test for buying a cheapest summer dress process")
    with sync_playwright() as playwright:
        main_page = enter_main_page(playwright)
        auth_page = AuthPage(main_page.click_sign_in())
        time.sleep(2)
        auth_page.submit_form(user["email"], user["password"])
        time.sleep(2)
        mylogger.info("login to registered account")
        assert auth_page.text_is_inside("Welcome to your account")
        main_page.fill_search_input("summer")
        main_page.click_search_button()
        header = main_page.search_results_header('SUMMER')
        mylogger.info("search for summer dress")
        assert "summer" in header
        cheapest, price = main_page.find_cheapest_product()
        time.sleep(2)
        main_page.hover_product_and_add_to_cart(cheapest)
        order_page = OrderPage(main_page.click_proceed_to_checkout())
        time.sleep(2)
        order_page.perform_order_process()
        total_price = order_page.total_price()
        mylogger.info("check the price of the product")
        assert price == re.sub('[^\d\.]', "", total_price)
        order_page.pay_and_complete_the_order()
        time.sleep(5)
        assert order_page.text_is_inside("Your order on My Store is complete")
        mylogger.info("text succeeded!")
        order_page.close_page()

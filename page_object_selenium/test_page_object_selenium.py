import time

import pytest
from selenium import webdriver
# from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from page_models.mainPage import MainPage
from page_models.authPage import AuthPage
from page_models.orderPage import OrderPage
import re
import logging
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrom_driver_path = "C:/Users/omerm/AppData/Local/Temp/Temp1_chromedriver_win32.zip/chromedriver.exe"
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
mylogger = logging.getLogger()


@pytest.fixture
def user():
    return {
      "email": "omermazor144@gmail.com",
      "password": "12345"
    }


def enter_main_page() -> MainPage:
    """
    A function that go to main page
    """
    driver = webdriver.Chrome(chrom_driver_path, chrome_options=chrome_options)
    driver.maximize_window()
    driver.get('http://automationpractice.com/index.php')
    return MainPage(driver)


def validate_input(email, password, text):
    main_page = enter_main_page()
    time.sleep(2)
    auth_page = AuthPage(main_page.click_sign_in())
    time.sleep(2)
    auth_page.submit_form(email, password)
    time.sleep(2)
    try:
        return auth_page.text_is_inside(text)
    finally:
        auth_page.close_page()


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
    main_page = enter_main_page()
    auth_page = AuthPage(main_page.click_sign_in())
    time.sleep(2)
    auth_page.click_forgot_password()
    time.sleep(2)
    assert auth_page.url() == "http://automationpractice.com/index.php?controller=password"
    mylogger.info("text succeeded!")
    auth_page.close_page()


def test_buy_cheapest_summer_dress(user):
    mylogger.info("test for buying a cheapest summer dress process")
    main_page = enter_main_page()
    auth_page = AuthPage(main_page.click_sign_in())
    time.sleep(1)
    auth_page.submit_form(user["email"], user["password"])
    time.sleep(1)
    mylogger.info("login to registered account")
    assert auth_page.text_is_inside("Welcome to your account")
    main_page.fill_search_input("summer")
    main_page.click_search_button()
    header = main_page.search_results_header()
    mylogger.info("search for summer dress")
    assert "SUMMER" in header
    cheapest, price = main_page.find_cheapest_product()
    time.sleep(2)
    main_page.hover_product_and_add_to_cart(cheapest)
    time.sleep(10)
    order_page = OrderPage(main_page.click_proceed_to_checkout())
    time.sleep(1)
    order_page.perform_order_process()
    total_price = order_page.total_price()
    mylogger.info("check the price of the product")
    assert price == re.sub('[^\d\.]', "", total_price)
    order_page.pay_and_complete_the_order()
    time.sleep(2)
    assert order_page.text_is_inside("Your order on My Store is complete")
    mylogger.info("text succeeded!")
    order_page.close_page()

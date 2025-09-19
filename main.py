import pytest
import data
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages import OrderPage
from locators import OrderPageLocators



@pytest.fixture
def driver():
    """A fixture to set up and tear down the WebDriver instance for each test."""
    options = Options()
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def order_page(driver):
    """A fixture to initialize the Page Object and navigate to the base URL."""
    driver.get(data.BASE_URL)
    return OrderPage(driver)


class TestUrbanRoutes:
    """A collection of individually testable user flows for the Urban Routes website."""

    def test_1_set_address(self, order_page):
        """Tests setting the From and To addresses."""
        order_page.set_route(data.FROM_ADDRESS, data.TO_ADDRESS)
        assert data.FROM_ADDRESS in order_page.get_field_value(OrderPageLocators.FROM_FIELD)
        assert data.TO_ADDRESS in order_page.get_field_value(OrderPageLocators.TO_FIELD)
        time.sleep(2)

    def test_2_select_tariff(self, order_page):
        """Tests selecting the 'Supportive' tariff."""
        order_page.set_route(data.FROM_ADDRESS, data.TO_ADDRESS)
        order_page.click_order_button_initial()
        order_page.select_supportive_tariff()
        time.sleep(2)
        assert order_page.get_active_tariff_text() == "Supportive", "The 'Supportive' tariff was not selected."
        time.sleep(2)

    def test_3_add_phone_number(self, order_page):
        """Tests adding and confirming a phone number."""
        order_page.set_route(data.FROM_ADDRESS, data.TO_ADDRESS)
        order_page.click_order_button_initial()
        order_page.select_supportive_tariff()
        order_page.enter_phone_number_and_code(data.PHONE_NUMBER)
        time.sleep(2)
        assert data.PHONE_NUMBER in order_page.get_phone_number_value(), "Phone number was not entered correctly."

    def test_4_add_payment_card(self, order_page):
        """Tests adding a payment card."""
        order_page.set_route(data.FROM_ADDRESS, data.TO_ADDRESS)
        order_page.click_order_button_initial()
        order_page.add_payment_card(data.CARD_NUMBER, data.CARD_CODE)
        assert "Card" in order_page.get_payment_method_text(), "Payment method did not switch to 'Card'."

    def test_5_add_comment(self, order_page):
        """Tests adding a comment for the driver."""
        order_page.set_route(data.FROM_ADDRESS, data.TO_ADDRESS)
        order_page.click_order_button_initial()
        order_page.select_supportive_tariff()
        order_page.set_comment_for_driver(data.DRIVER_COMMENT)
        time.sleep(2)
        assert data.DRIVER_COMMENT in order_page.get_field_value(OrderPageLocators.COMMENT_FIELD)

    def test_6_order_extras(self, order_page):
        """Tests ordering a blanket and two ice creams."""
        order_page.set_route(data.FROM_ADDRESS, data.TO_ADDRESS)
        order_page.click_order_button_initial()
        order_page.select_supportive_tariff()
        order_page.request_blanket()
        assert order_page.is_blanket_selected(), "Blanket and handkerchiefs were not selected."
        order_page.add_ice_creams(2)
        time.sleep(2)
        assert order_page.get_ice_cream_count() == 2, "The ice cream count is not correct."

    def test_7_final_order(self, order_page):
        """Tests the final step of ordering the taxi."""
        order_page.set_route(data.FROM_ADDRESS, data.TO_ADDRESS)
        order_page.click_order_button_initial()
        time.sleep(2)
        order_page.select_supportive_tariff()
        order_page.enter_phone_number_and_code(data.PHONE_NUMBER)
        time.sleep(2)
        order_page.add_payment_card(data.CARD_NUMBER, data.CARD_CODE)
        time.sleep(2)
        order_page.set_comment_for_driver(data.DRIVER_COMMENT)
        order_page.click_order_button_final()
        assert order_page.wait_for_car_search_modal(), "The car search modal did not appear."
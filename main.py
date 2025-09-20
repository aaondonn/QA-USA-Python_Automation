import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages import OrderPage, OrderPageLocators
import data
import helpers

class TestUrbanRoutes:
    """A collection of individually testable user flows for the Urban Routes website."""

    driver = None

    @classmethod
    def setup_class(cls):
        """Sets up the WebDriver instance for the entire test class."""
        assert helpers.is_url_reachable(data.BASE_URL), "The URL is not reachable."
        options = Options()
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()

    @classmethod
    def teardown_class(cls):
        """Tears down the WebDriver instance after all tests."""
        if cls.driver:
            cls.driver.quit()

    @pytest.fixture(autouse=True)
    def order_page(self):
        """A fixture to initialize the Page Object and navigate to the base URL for each test."""
        self.driver.get(data.BASE_URL)
        return OrderPage(self.driver)

    def test_set_address(self, order_page):
        """Tests setting and verifying the From and To addresses."""
        order_page.set_route(data.FROM_ADDRESS, data.TO_ADDRESS)
        assert data.FROM_ADDRESS in order_page.get_field_value(OrderPageLocators.FROM_FIELD)
        assert data.TO_ADDRESS in order_page.get_field_value(OrderPageLocators.TO_FIELD)

    def test_select_tariff(self, order_page):
        """Tests selecting and verifying the 'Supportive' tariff."""
        order_page.set_route(data.FROM_ADDRESS, data.TO_ADDRESS)
        order_page.click_order_button_initial()
        order_page.select_supportive_tariff()
        assert order_page.get_active_tariff_text() == "Supportive"

    def test_add_phone_number(self, order_page):
        """Tests adding and verifying a phone number."""
        order_page.set_route(data.FROM_ADDRESS, data.TO_ADDRESS)
        order_page.click_order_button_initial()
        order_page.select_supportive_tariff()
        order_page.enter_phone_number_and_code(data.PHONE_NUMBER)
        assert data.PHONE_NUMBER in order_page.get_phone_number_value()

    def test_add_payment_card(self, order_page):
        """Tests adding and verifying a payment card."""
        order_page.set_route(data.FROM_ADDRESS, data.TO_ADDRESS)
        order_page.click_order_button_initial()
        order_page.select_supportive_tariff()
        order_page.enter_phone_number_and_code(data.PHONE_NUMBER)
        order_page.add_payment_card(data.CARD_NUMBER, data.CARD_CODE)
        assert "Card" in order_page.get_payment_method_text()

    def test_add_comment(self, order_page):
        """Tests adding a comment for the driver."""
        order_page.set_route(data.FROM_ADDRESS, data.TO_ADDRESS)
        order_page.click_order_button_initial()
        order_page.select_supportive_tariff()
        order_page.set_comment_for_driver(data.DRIVER_COMMENT)
        assert data.DRIVER_COMMENT in order_page.get_field_value(OrderPageLocators.COMMENT_FIELD)

    def test_order_blanket(self, order_page):
        """Tests ordering a blanket and handkerchiefs."""
        order_page.set_route(data.FROM_ADDRESS, data.TO_ADDRESS)
        order_page.click_order_button_initial()
        order_page.select_supportive_tariff()
        order_page.request_blanket()
        assert order_page.is_blanket_selected()

    def test_order_ice_creams(self, order_page):
        """Tests ordering two ice creams."""
        order_page.set_route(data.FROM_ADDRESS, data.TO_ADDRESS)
        order_page.click_order_button_initial()
        order_page.select_supportive_tariff()
        order_page.add_ice_creams(2)
        assert order_page.get_ice_cream_count() == 2

    def test_final_order(self, order_page):
        """Tests the final step of ordering the taxi and verifying the car search modal."""
        order_page.set_route(data.FROM_ADDRESS, data.TO_ADDRESS)
        order_page.click_order_button_initial()
        order_page.select_supportive_tariff()
        order_page.enter_phone_number_and_code(data.PHONE_NUMBER)
        order_page.add_payment_card(data.CARD_NUMBER, data.CARD_CODE)
        order_page.set_comment_for_driver(data.DRIVER_COMMENT)
        order_page.click_order_button_final()
        assert order_page.wait_for_car_search_modal()
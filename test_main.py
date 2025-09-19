import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages import OrderPage
from locators import OrderPageLocators

# Test Data
BASE_URL = "https://cnt-ae82fd4f-2464-46dc-9870-9ea0fab59644.containerhub.tripleten-services.com/"
FROM_ADDRESS = "East 2nd Street, 601"
TO_ADDRESS = "1300 1st St"
PHONE_NUMBER = "+1 123 123 1234"
CARD_NUMBER = "1234 5678 9101 1121"
CARD_CODE = "123"
DRIVER_COMMENT = "Please call upon arrival."


@pytest.fixture
def driver():
    """
    pytest fixture to set up and tear down the WebDriver instance for each test.
    """
    options = Options()
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def order_page(driver):
    """
    A fixture to initialize the Page Object and navigate to the base URL.
    """
    driver.get(BASE_URL)
    return OrderPage(driver)


class TestUrbanRoutes:
    """A collection of tests for the Urban Routes website, now independent."""

    def test_1_set_route(self, order_page):
        """Test Case 1: Set and verify the 'From' and 'To' addresses."""
        order_page.set_route(FROM_ADDRESS, TO_ADDRESS)
        assert FROM_ADDRESS in order_page.get_field_value(OrderPageLocators.FROM_FIELD)
        assert TO_ADDRESS in order_page.get_field_value(OrderPageLocators.TO_FIELD)

    def test_2_select_tariff(self, order_page):
        """Test Case 2: Select the 'Supportive' tariff."""
        order_page.set_route(FROM_ADDRESS, TO_ADDRESS)
        order_page.click_call_taxi_button()
        order_page.select_supportive_tariff()
        assert order_page.is_supportive_tariff_selected(), "The 'Supportive' tariff was not selected."

    def test_3_enter_phone_number(self, order_page):
        """Test Case 3: Enter and confirm phone number."""
        order_page.set_route(FROM_ADDRESS, TO_ADDRESS)
        order_page.click_call_taxi_button()
        order_page.select_supportive_tariff()
        order_page.enter_phone_number_and_code(PHONE_NUMBER)

    def test_4_add_payment_card(self, order_page):
        """Test Case 4: Add a credit card as a payment method."""
        order_page.set_route(FROM_ADDRESS, TO_ADDRESS)
        order_page.click_call_taxi_button()
        order_page.select_supportive_tariff()
        order_page.enter_phone_number_and_code(PHONE_NUMBER)
        order_page.add_payment_card(CARD_NUMBER, CARD_CODE)

    def test_5_add_extras(self, order_page):
        """Test Case 5: Add a driver comment and other extras."""
        order_page.set_route(FROM_ADDRESS, TO_ADDRESS)
        order_page.click_call_taxi_button()
        order_page.select_supportive_tariff()
        order_page.enter_phone_number_and_code(PHONE_NUMBER)
        order_page.add_payment_card(CARD_NUMBER, CARD_CODE)
        order_page.set_comment_for_driver(DRIVER_COMMENT)
        order_page.request_blanket()
        order_page.add_ice_creams(2)
        assert DRIVER_COMMENT in order_page.get_field_value(OrderPageLocators.COMMENT_FIELD)
        assert order_page.is_blanket_selected()
        assert order_page.get_ice_cream_count() == 2

    @pytest.mark.batch
    def test_full_order_flow_batch(self, order_page):
        """
        Batch Test: A complete end-to-end test case that runs all steps.
        """
        # 1. Set the route
        order_page.set_route(FROM_ADDRESS, TO_ADDRESS)
        # 2. Call a taxi
        order_page.click_call_taxi_button()
        # 3. Select tariff
        order_page.select_supportive_tariff()
        # 4. Enter phone number
        order_page.enter_phone_number_and_code(PHONE_NUMBER)
        # 5. Add payment method
        order_page.add_payment_card(CARD_NUMBER, CARD_CODE)
        # 6. Add extra details
        order_page.set_comment_for_driver(DRIVER_COMMENT)
        order_page.request_blanket()
        order_page.add_ice_creams(2)
        # 7. Place the order
        order_page.click_order_button()
        # 8. Verify the order was placed successfully
        modal_title = order_page.get_car_search_modal_title()
        assert "Looking for a driver" in modal_title, "The car search modal did not appear as expected."


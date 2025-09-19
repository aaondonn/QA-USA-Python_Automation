import pytest
from selenium import webdriver
from pages import OrderPage
# We must import the locators here so the test script can use them for assertions.
from locators import OrderPageLocators

# Test Data
BASE_URL = "https://cnt-8b57c933-1cd4-4e49-bf8a-e933e6047fc6.containerhub.tripleten-services.com/"
FROM_ADDRESS = "East 2nd Street, 601"
TO_ADDRESS = "1300 1st St"
PHONE_NUMBER = "+1 123 123 1234"
# The confirmation code is static in this test environment
CONFIRMATION_CODE = "1234"
CARD_NUMBER = "1234 5678 9101 1121"
CARD_CODE = "123"
DRIVER_COMMENT = "Please call upon arrival."


@pytest.fixture
def driver():
    """
    pytest fixture to set up and tear down the WebDriver instance for each test.
    """
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    # Teardown: close the browser after the test is finished
    driver.quit()


@pytest.fixture
def order_page(driver):
    """
    A fixture to initialize the Page Object and navigate to the base URL.
    This helps keep the test code DRY (Don't Repeat Yourself).
    """
    driver.get(BASE_URL)
    return OrderPage(driver)


class TestUrbanRoutes:
    """A collection of tests for the Urban Routes website, now independent."""

    def test_1_set_route(self, order_page):
        """Test Case 1: Set and verify the 'From' and 'To' addresses."""
        order_page.set_route(FROM_ADDRESS, TO_ADDRESS)
        # Verify that the values were entered correctly
        assert FROM_ADDRESS in order_page.get_field_value(OrderPageLocators.FROM_FIELD)
        assert TO_ADDRESS in order_page.get_field_value(OrderPageLocators.TO_FIELD)

    def test_2_select_tariff(self, order_page):
        """Test Case 2: Select the 'Comfort' tariff."""
        order_page.set_route(FROM_ADDRESS, TO_ADDRESS)
        order_page.click_call_taxi_button()
        order_page.select_comfort_tariff()
        # In a real scenario, we would add an assertion here to verify the tariff was selected.

    def test_3_enter_phone_number(self, order_page):
        """Test Case 3: Enter and confirm phone number."""
        order_page.set_route(FROM_ADDRESS, TO_ADDRESS)
        order_page.click_call_taxi_button()
        order_page.select_comfort_tariff()
        order_page.enter_phone_number_and_code(PHONE_NUMBER, CONFIRMATION_CODE)
        # Assertion to verify successful phone entry would go here.

    def test_4_add_payment_card(self, order_page):
        """Test Case 4: Add a credit card as a payment method."""
        order_page.set_route(FROM_ADDRESS, TO_ADDRESS)
        order_page.click_call_taxi_button()
        order_page.select_comfort_tariff()
        order_page.enter_phone_number_and_code(PHONE_NUMBER, CONFIRMATION_CODE)
        order_page.add_payment_card(CARD_NUMBER, CARD_CODE)
        # Assertion to verify the card was added would go here.

    def test_5_add_extras(self, order_page):
        """Test Case 5: Add a driver comment and other extras."""
        order_page.set_route(FROM_ADDRESS, TO_ADDRESS)
        order_page.click_call_taxi_button()
        order_page.select_comfort_tariff()
        order_page.enter_phone_number_and_code(PHONE_NUMBER, CONFIRMATION_CODE)
        order_page.add_payment_card(CARD_NUMBER, CARD_CODE)
        order_page.set_comment_for_driver(DRIVER_COMMENT)
        order_page.request_blanket()
        order_page.add_ice_creams(2)
        # Verification to check if the comment field has the correct text.
        assert DRIVER_COMMENT in order_page.get_field_value(OrderPageLocators.COMMENT_FIELD)

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
        order_page.select_comfort_tariff()
        # 4. Enter phone number
        order_page.enter_phone_number_and_code(PHONE_NUMBER, CONFIRMATION_CODE)
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


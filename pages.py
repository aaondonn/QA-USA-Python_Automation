import time
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from locators import OrderPageLocators
from helpers import retrieve_phone_code


class BasePage:
    """Base Page class containing common methods for all pages."""

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located(locator),
            message=f"Can't find element by locator {locator}"
        )

    def find_clickable_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(
            EC.element_to_be_clickable(locator),
            message=f"Element is not clickable by locator {locator}"
        )


class OrderPage(BasePage):
    """Methods for interacting with the main order page."""
    locators = OrderPageLocators

    def set_route(self, from_address, to_address):
        self.find_element(self.locators.FROM_FIELD).send_keys(from_address)
        self.find_element(self.locators.TO_FIELD).send_keys(to_address)

    def get_field_value(self, field_locator):
        return self.find_element(field_locator).get_attribute('value')

    def click_order_button_initial(self):
        self.find_clickable_element(self.locators.ORDER_BUTTON_INITIAL).click()
        time.sleep(2)

    def select_supportive_tariff(self):
        self.find_clickable_element(self.locators.SUPPORTIVE_TARIFF).click()
        self.find_element(self.locators.ACTIVE_TARIFF_TEXT)

    def get_active_tariff_text(self):
        """Retrieves the text of the currently active tariff plan."""
        return self.find_element(self.locators.ACTIVE_TARIFF_TEXT, time=2).text

    def enter_phone_number_and_code(self, phone):
        """Clicks the phone number button, enters the number, and confirms."""
        # Step 1: Click the button to open the phone number entry modal
        self.find_clickable_element(self.locators.PHONE_NUMBER_BUTTON).click()

        # Step 2: Now find the input field and type the number
        phone_input = self.find_clickable_element(self.locators.PHONE_FIELD)
        phone_input.send_keys(phone)

        # Step 3: Click 'Next'
        self.find_clickable_element(self.locators.PHONE_SUBMIT_BUTTON).click()
        time.sleep(2)

        # Step 4: Retrieve and enter the SMS code
        phone_code = retrieve_phone_code(self.driver)
        self.find_element(self.locators.CODE_FIELD).send_keys(phone_code)

        # Step 5: Click 'Confirm'
        self.find_clickable_element(self.locators.CONFIRM_CODE_BUTTON).click()
        time.sleep(2)

    def get_phone_number_value(self):
        """Retrieves the value from the phone number input field."""
        return self.get_field_value(self.locators.PHONE_FIELD)

    def add_payment_card(self, card_number, card_code):
        """Adds a credit card after the pop-up appears."""
        self.find_clickable_element(self.locators.PAYMENT_METHOD_BUTTON).click()
        time.sleep(2)
        self.find_clickable_element(self.locators.ADD_CARD_LINK).click()
        time.sleep(2)

        card_number_input = self.find_clickable_element(self.locators.CARD_NUMBER_FIELD)
        card_number_input.send_keys(card_number)
        time.sleep(2)

        card_code_field = self.find_element(self.locators.CARD_CODE_FIELD)
        card_code_field.send_keys(card_code)
        time.sleep(2)
        card_code_field.send_keys(Keys.TAB)

        self.find_clickable_element(self.locators.CARD_SUBMIT_BUTTON).click()
        time.sleep(2)
        self.find_clickable_element(self.locators.CLOSE_PAYMENT_MODAL_BUTTON).click()
        time.sleep(2)

    def get_payment_method_text(self):
        return self.find_element(self.locators.PAYMENT_METHOD_TEXT).text

    def set_comment_for_driver(self, comment):
        self.find_element(self.locators.COMMENT_FIELD).send_keys(comment)

    def request_blanket(self):
        self.find_clickable_element(self.locators.BLANKET_SWITCH).click()
        time.sleep(2)

    def is_blanket_selected(self):
        return self.find_element(self.locators.BLANKET_SWITCH_CHECKBOX).is_selected()

    def add_ice_creams(self, number_of_ice_creams):
        plus_button = self.find_clickable_element(self.locators.ICE_CREAM_PLUS_BUTTON)
        for _ in range(number_of_ice_creams):
            plus_button.click()
            time.sleep(2)

    def get_ice_cream_count(self):
        return int(self.find_element(self.locators.ICE_CREAM_COUNTER).text)

    def click_order_button_final(self):
        self.find_clickable_element(self.locators.ORDER_BUTTON_FINAL).click()
        time.sleep(2)

    def wait_for_car_search_modal(self):
        return self.find_element(self.locators.CAR_SEARCH_MODAL, time=15).is_displayed()
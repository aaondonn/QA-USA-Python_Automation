import time
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import OrderPageLocators
# We need our magical helper function!
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
        from_field = self.find_clickable_element(self.locators.FROM_FIELD)
        from_field.clear()
        from_field.send_keys(from_address)
        to_field = self.find_clickable_element(self.locators.TO_FIELD)
        to_field.clear()
        to_field.send_keys(to_address)

    def get_field_value(self, field_locator):
        return self.find_element(field_locator).get_attribute('value')

    def click_call_taxi_button(self):
        self.find_clickable_element(self.locators.CALL_TAXI_BUTTON).click()
        time.sleep(1) # A brief pause for the tariff modal to appear

    def select_supportive_tariff(self):
        """
        Selects the 'Supportive' plan only if it's not already selected.
        This single command now handles both checking and clicking.
        """
        try:
            # First, we check if the tariff is already active.
            self.find_element(self.locators.ACTIVE_SUPPORTIVE_TARIFF, time=2)
            # If the line above works, it means the tariff is already selected, so we do nothing!
        except TimeoutException:
            # If we get a TimeoutException, it means the tariff isn't active, so we click it.
            self.find_clickable_element(self.locators.SUPPORTIVE_TARIFF).click()

    def is_supportive_tariff_selected(self):
        """
        Checks if the 'Supportive' tariff plan is currently active.
        This is now mainly used for assertions in our tests.
        """
        try:
            self.find_element(self.locators.ACTIVE_SUPPORTIVE_TARIFF, time=2)
            return True
        except TimeoutException:
            return False

    def enter_phone_number_and_code(self, phone):
        self.find_element(self.locators.PHONE_FIELD).send_keys(phone)
        self.find_clickable_element(self.locators.PHONE_SUBMIT_BUTTON).click()
        phone_code = retrieve_phone_code(self.driver)
        code_field = self.find_element(self.locators.CODE_FIELD)
        code_field.send_keys(phone_code)
        self.find_clickable_element(self.locators.CONFIRM_CODE_BUTTON).click()

    def add_payment_card(self, card_number, card_code):
        self.find_clickable_element(self.locators.PAYMENT_METHOD_BUTTON).click()
        self.find_clickable_element(self.locators.ADD_CARD_LINK).click()
        self.find_element(self.locators.CARD_NUMBER_FIELD).send_keys(card_number)
        card_code_field = self.find_element(self.locators.CARD_CODE_FIELD)
        card_code_field.send_keys(card_code)
        self.find_clickable_element(self.locators.PAYMENT_MODAL).click()
        self.find_clickable_element(self.locators.CARD_SUBMIT_BUTTON).click()
        self.find_clickable_element(self.locators.CLOSE_PAYMENT_MODAL_BUTTON).click()

    def set_comment_for_driver(self, comment):
        self.find_element(self.locators.COMMENT_FIELD).send_keys(comment)

    def request_blanket(self):
        self.find_clickable_element(self.locators.BLANKET_SWITCH).click()

    def is_blanket_selected(self):
        checkbox = self.find_element(self.locators.BLANKET_SWITCH_CHECKBOX)
        return checkbox.is_selected()

    def add_ice_creams(self, number_of_ice_creams):
        plus_button = self.find_clickable_element(self.locators.ICE_CREAM_PLUS_BUTTON)
        for _ in range(number_of_ice_creams):
            plus_button.click()

    def get_ice_cream_count(self):
        return int(self.find_element(self.locators.ICE_CREAM_COUNTER).text)

    def click_order_button(self):
        self.find_clickable_element(self.locators.ORDER_BUTTON).click()

    def get_car_search_modal_title(self):
        modal_title_element = self.find_element(self.locators.CAR_SEARCH_MODAL_TITLE, time=15)
        return modal_title_element.text


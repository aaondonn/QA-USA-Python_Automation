import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# A separate class for locators makes them easy to manage
class OrderPageLocators:
    """Locators for the main order page of Urban Routes."""
    FROM_FIELD = (By.ID, "from")
    TO_FIELD = (By.ID, "to")
    ADDRESS_SUGGESTION = (By.XPATH, "(//div[contains(@class, 'address-item')])[1]")

    CALL_TAXI_BUTTON = (By.XPATH, "//button[text()='Call a taxi']")

    # Tariff Plan Locators
    COMFORT_PLAN_BUTTON = (By.XPATH, "//div[text()='Comfort']")

    # Phone Number Section
    PHONE_FIELD = (By.ID, "phone")
    PHONE_SUBMIT_BUTTON = (By.XPATH, "//button[text()='Next']")
    CODE_FIELD = (By.ID, "code")
    CONFIRM_CODE_BUTTON = (By.XPATH, "//button[text()='Confirm']")

    # Payment Method Section
    PAYMENT_METHOD_BUTTON = (By.CLASS_NAME, "pp-button")
    ADD_CARD_LINK = (By.CLASS_NAME, "pp-plus")
    CARD_NUMBER_FIELD = (By.ID, "number")
    CARD_CODE_FIELD = (By.XPATH, "//div[label[text()='Code:']]/input[@id='code']")
    CARD_SUBMIT_BUTTON = (By.XPATH, "//button[text()='Link']")
    CLOSE_PAYMENT_MODAL_BUTTON = (By.XPATH, "//div[@class='payment-picker open']//button[@class='close-button']")

    # Other Details
    COMMENT_FIELD = (By.ID, "comment")
    BLANKET_SWITCH = (By.XPATH, "//input[@type='checkbox' and @class='switch-input']")
    ICE_CREAM_PLUS_BUTTON = (By.XPATH, "//div[div[text()='Ice cream']]/div/div[@class='counter-plus']")

    # Final Order Button
    ORDER_BUTTON = (By.XPATH, "//button/span[text()='Order']/parent::button")

    # Verification Locator
    CAR_SEARCH_MODAL = (By.CLASS_NAME, "order-header-title")
    FROM_LOCATOR = (By.ID, 'from')
    TO_LOCATOR = (By.ID, 'to')
    CUSTOM_OPTION_LOCATOR = (By.XPATH, '//div[text()="Custom"]')
    DRIVE_ICON_LOCATOR = (By.XPATH, '(//img[@src="/static/media/car.8a2b1ff5.svg"])[2]')
    BOOK_BUTTON_LOCATOR = (By.XPATH, '//button[@class="button round"]')
    CAMPING_LOCATOR = (By.XPATH, '//div[contains(text(),"Camping")]')
    AUDI_TEXT_LOCATOR = (By.XPATH, '//div[contains(text(),"Audi A3 Sedan")]')
    ADD_DRIVER_LICENSE_LOCATOR = (By.XPATH, '(//div[contains(text(),"Add a driver")])[2]')
    FIRST_NAME_LOCATOR = (By.ID, 'firstName')
    LAST_NAME_LOCATOR = (By.ID, 'lastName')
    DATE_OF_BIRTH_LOCATOR = (By.ID, 'birthDate')
    NUMBER_LOCATOR = (By.ID, 'number')
    ADD_BUTTON_LOCATOR = (By.XPATH, '//button[@type="submit" and text()="Add"]')
    ADD_A_DRIVER_LICENCE_TITLE_LOCATOR = (By.XPATH, '//div[contains(text(),"Add a driver")]')
    VERIFICATION_TEXT_LOCATOR = (By.XPATH, '//div[@class="section active"]//div[@style="margin-bottom: 30px;"]')

class BasePage:
    """Base Page class containing common methods for all pages."""

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator, time=10):
        """Finds a single element with an explicit wait."""
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located(locator),
            message=f"Can't find element by locator {locator}"
        )

    def find_clickable_element(self, locator, time=10):
        """Finds a clickable element with an explicit wait."""
        return WebDriverWait(self.driver, time).until(
            EC.element_to_be_clickable(locator),
            message=f"Element is not clickable by locator {locator}"
        )


class OrderPage(BasePage):
    """Methods for interacting with the main order page."""

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = None

    def _enter_and_select_address(self, field_locator, address):
        field = self.driver.find_element(*field_locator)
        urban_routes_page = UrbanRoutesPage(driver)

        OrderPageLocators.enter_from_location('East 2nd Street, 601')
        urban_routes_page.enter_to_location('1300 1st St')
        # Use JavaScript to focus the element instead of clicking
        self.driver.execute_script("arguments[0].focus();", field)

        field.clear()
        field.send_keys(address)

        # Wait for dropdown and select first option
        first_option = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "select-option")))
        first_option.click()

    def set_route(self, from_address, to_address):
        """Fills the 'From' and 'To' fields and selects the first suggestion."""
        self._enter_and_select_address(OrderPageLocators.FROM_FIELD, from_address)
        self._enter_and_select_address(OrderPageLocators.TO_FIELD, to_address)

        # After setting the route, click the main "Call a taxi" button
        self.find_clickable_element(OrderPageLocators.CALL_TAXI_BUTTON).click()

    def select_comfort_plan(self):
        """Selects the 'Comfort' tariff plan."""
        self.find_clickable_element(OrderPageLocators.COMFORT_PLAN_BUTTON).click()

    def set_phone_number(self, phone):
        """Enters the phone number, submits, and enters the confirmation code."""
        self.find_element(OrderPageLocators.PHONE_FIELD).send_keys(phone)
        self.find_clickable_element(OrderPageLocators.PHONE_SUBMIT_BUTTON).click()

        # Wait for the code field to appear, then enter the code
        code_field = self.find_element(OrderPageLocators.CODE_FIELD)
        code_field.send_keys("1234")
        self.find_clickable_element(OrderPageLocators.CONFIRM_CODE_BUTTON).click()

    def set_payment_method_to_card(self, card_number, card_code):
        """Sets the payment method to Card and fills in the details."""
        self.find_clickable_element(OrderPageLocators.PAYMENT_METHOD_BUTTON).click()
        self.find_clickable_element(OrderPageLocators.ADD_CARD_LINK).click()
        self.find_element(OrderPageLocators.CARD_NUMBER_FIELD).send_keys(card_number)
        self.find_element(OrderPageLocators.CARD_CODE_FIELD).send_keys(card_code)
        self.find_clickable_element(OrderPageLocators.CARD_SUBMIT_BUTTON).click()
        self.find_clickable_element(OrderPageLocators.CLOSE_PAYMENT_MODAL_BUTTON).click()

    def set_comment_for_driver(self, comment):
        """Adds a comment for the driver."""
        self.find_element(OrderPageLocators.COMMENT_FIELD).send_keys(comment)

    def order_blanket_and_handkerchiefs(self):
        """Toggles the switch for a blanket and handkerchiefs."""
        self.find_clickable_element(OrderPageLocators.BLANKET_SWITCH).click()

    def add_ice_creams(self, number_of_ice_creams):
        """Clicks the '+' button to add a specified number of ice creams."""
        for _ in range(number_of_ice_creams):
            self.find_clickable_element(OrderPageLocators.ICE_CREAM_PLUS_BUTTON).click()

    def click_order_button(self):
        """Clicks the final 'Order' button to place the order."""
        self.find_clickable_element(OrderPageLocators.ORDER_BUTTON).click()

    def is_car_search_modal_visible(self):
        """Checks if the car search modal is visible after ordering."""
        try:
            self.find_element(OrderPageLocators.CAR_SEARCH_MODAL, time=5)
            return True
        except:
            return False


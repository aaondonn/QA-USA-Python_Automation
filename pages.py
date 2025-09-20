from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import retrieve_phone_code


class OrderPageLocators:
    """Locators for the Urban Routes order page."""
    # Stage 1: Setting the Route
    FROM_FIELD = (By.ID, "from")
    TO_FIELD = (By.ID, "to")
    ORDER_BUTTON_INITIAL = (By.XPATH, '//button[contains(@class, "round")]')

    # Stage 2: Selecting Tariff
    SUPPORTIVE_TARIFF = (By.XPATH, "//div[@class='tcard-title' and text()='Supportive']")
    ACTIVE_TARIFF_TEXT = (By.CSS_SELECTOR, ".tcard.active .tcard-title")

    # Stage 3: Phone Number
    PHONE_NUMBER_BUTTON = (By.CLASS_NAME, "np-button")
    PHONE_FIELD = (By.ID, "phone")
    PHONE_SUBMIT_BUTTON = (By.XPATH, "//div[contains(@class, 'number-picker')]//button[text()='Next']")
    CODE_FIELD = (By.ID, "code")
    CONFIRM_CODE_BUTTON = (By.XPATH, "//div[contains(@class, 'number-picker')]//button[text()='Confirm']")

    # Stage 4: Payment Method
    PAYMENT_METHOD_BUTTON = (By.CLASS_NAME, "pp-button")
    PAYMENT_METHOD_TEXT = (By.CSS_SELECTOR, ".pp-button .pp-value-text")
    ADD_CARD_LINK = (By.CLASS_NAME, "pp-plus")
    CARD_MODAL = (By.CLASS_NAME, "payment-picker")  # Locator for the entire modal
    CARD_NUMBER_FIELD = (By.CSS_SELECTOR, "input#number.card-input")
    CARD_CODE_FIELD = (By.CSS_SELECTOR, "input#code.card-input")
    CARD_SUBMIT_BUTTON = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')
    CLOSE_PAYMENT_MODAL_BUTTON = (By.CSS_SELECTOR, ".payment-picker.open .close-button")

    # Stage 5: Other Details
    COMMENT_FIELD = (By.ID, "comment")
    BLANKET_SWITCH = (By.XPATH, "//div[contains(., 'Blanket and handkerchiefs')]//div[@class='r-sw']")
    BLANKET_SWITCH_CHECKBOX = (By.XPATH, "//div[text()='Blanket and handkerchiefs']/../..//input[@type='checkbox']")
    ICE_CREAM_PLUS_BUTTON = (By.XPATH, "//div[text()='Ice cream']/following-sibling::div//div[@class='counter-plus']")
    ICE_CREAM_COUNTER = (By.XPATH,
                         "//div[text()='Ice cream']/following-sibling::div//div[contains(@class, 'counter-value')]")

    # Final Stage: Order Button and Verification
    ORDER_BUTTON_FINAL = (By.CSS_SELECTOR, ".smart-button-wrapper button")
    CAR_SEARCH_MODAL = (By.CLASS_NAME, "order-header")


# --- Base Page Class ---
class BasePage:
    """Base Page class containing common methods for all pages."""

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator))

    def find_clickable_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(EC.element_to_be_clickable(locator))

    def wait_for_element_invisibility(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(EC.invisibility_of_element_located(locator))


# --- Order Page Class ---
class OrderPage(BasePage):
    """Methods for interacting with the main order page."""

    def set_route(self, from_address, to_address):
        self.find_element(OrderPageLocators.FROM_FIELD).send_keys(from_address)
        self.find_element(OrderPageLocators.TO_FIELD).send_keys(to_address)

    def get_field_value(self, field_locator):
        return self.find_element(field_locator).get_attribute('value')

    def click_order_button_initial(self):
        self.find_clickable_element(OrderPageLocators.ORDER_BUTTON_INITIAL).click()
        self.find_element(OrderPageLocators.SUPPORTIVE_TARIFF)

    def select_supportive_tariff(self):
        self.find_clickable_element(OrderPageLocators.SUPPORTIVE_TARIFF).click()
        self.find_element(OrderPageLocators.ACTIVE_TARIFF_TEXT)

    def get_active_tariff_text(self):
        return self.find_element(OrderPageLocators.ACTIVE_TARIFF_TEXT).text

    def enter_phone_number_and_code(self, phone):
        self.find_clickable_element(OrderPageLocators.PHONE_NUMBER_BUTTON).click()
        phone_input = self.find_clickable_element(OrderPageLocators.PHONE_FIELD)
        phone_input.send_keys(phone)
        self.find_clickable_element(OrderPageLocators.PHONE_SUBMIT_BUTTON).click()

        phone_code = retrieve_phone_code(self.driver)
        code_field = self.find_element(OrderPageLocators.CODE_FIELD)
        code_field.send_keys(phone_code)

        self.find_clickable_element(OrderPageLocators.CONFIRM_CODE_BUTTON).click()
        self.find_element(OrderPageLocators.PAYMENT_METHOD_BUTTON)

    def get_phone_number_value(self):
        return self.get_field_value(OrderPageLocators.PHONE_FIELD)

    def add_payment_card(self, card_number, card_code):
        """Adds a credit card and closes the payment modal."""
        # Click the payment method to open the selector
        self.find_clickable_element(OrderPageLocators.PAYMENT_METHOD_BUTTON).click()

        # Click the 'Add card' link to open the modal
        self.find_clickable_element(OrderPageLocators.ADD_CARD_LINK).click()

        # Wait for the card number field to be ready, then type
        card_number_input = self.find_clickable_element(OrderPageLocators.CARD_NUMBER_FIELD)
        card_number_input.send_keys(card_number)

        # Find the CVV field and type
        card_code_field = self.find_element(OrderPageLocators.CARD_CODE_FIELD)
        card_code_field.send_keys(card_code)

        # Click the card number field again to ensure the CVV field loses focus
        card_number_input.click()

        # Click the 'Link' button to submit the card
        self.find_clickable_element(OrderPageLocators.CARD_SUBMIT_BUTTON).click()

        # Click the 'close' button to exit the payment pop-up
        self.find_clickable_element(OrderPageLocators.CLOSE_PAYMENT_MODAL_BUTTON).click()


    def get_payment_method_text(self):
        return self.find_element(OrderPageLocators.PAYMENT_METHOD_TEXT).text

    def set_comment_for_driver(self, comment):
        self.find_element(OrderPageLocators.COMMENT_FIELD).send_keys(comment)

    def request_blanket(self):
        self.find_clickable_element(OrderPageLocators.BLANKET_SWITCH).click()

    def is_blanket_selected(self):
        return self.find_element(OrderPageLocators.BLANKET_SWITCH_CHECKBOX).is_selected()

    def add_ice_creams(self, number_of_ice_creams):
        plus_button = self.find_clickable_element(OrderPageLocators.ICE_CREAM_PLUS_BUTTON)
        for _ in range(number_of_ice_creams):
            plus_button.click()

    def get_ice_cream_count(self):
        return int(self.find_element(OrderPageLocators.ICE_CREAM_COUNTER).text)

    def click_order_button_final(self):
        self.find_clickable_element(OrderPageLocators.ORDER_BUTTON_FINAL).click()

    def wait_for_car_search_modal(self):
        return self.find_element(OrderPageLocators.CAR_SEARCH_MODAL, time=15).is_displayed()
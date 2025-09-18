from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import data
from data import CARD_NUMBER, CARD_CODE


class UrbanRoutesPage:
    # --- Locators ---
    FROM_LOCATOR = (By.ID, 'from')
    TO_LOCATOR = (By.ID, 'to')
    CALL_TAXI_BUTTON_LOCATOR = (By.XPATH, "//button[text()='Call a taxi']")
    SUPPORTIVE_PLAN_LOCATOR = (By.XPATH, "//div[contains(text(),'Supportive')]")
    PHONE_FIELD_LOCATOR = (By.CLASS_NAME, 'np-button')
    PHONE_INPUT_LOCATOR = (By.ID, 'phone')
    PHONE_NEXT_BUTTON_LOCATOR = (By.XPATH, "//button[text()='Next']")
    SMS_CODE_INPUT_LOCATOR = (By.ID, 'code')
    CONFIRM_BUTTON_LOCATOR = (By.XPATH, "//button[text()='Confirm']")
    CONFIRMED_PHONE_LOCATOR = (By.CLASS_NAME, 'np-text')
    PAYMENT_METHOD_LOCATOR = (By.CLASS_NAME, 'pp-value-text')
    ADD_CARD_LINK_LOCATOR = (By.CLASS_NAME, 'pp-plus')
    CARD_NUMBER_INPUT_LOCATOR = (By.XPATH, '//*[@id="number"]')
    CARD_CVV_INPUT_LOCATOR = (By.XPATH, "//input[@id='code']")
    LINK_CARD_BUTTON_LOCATOR = (By.XPATH, "//button[text()='Link']")
    PAYMENT_MODAL_CLOSE_LOCATOR = (By.XPATH, "//div[@class='payment-picker open']//button[@class='close-button section-close']")
    COMMENT_FIELD_LOCATOR = (By.ID, 'comment')
    BLANKET_SWITCH_LOCATOR = (By.XPATH, "//div[label[text()='Blanket and handkerchiefs']]//span[@class='switch-input']")
    BLANKET_CHECKBOX_LOCATOR = (By.XPATH, "//div[label[text()='Blanket and handkerchiefs']]//input")
    ICE_CREAM_PLUS_LOCATOR = (By.XPATH, "//div[label[text()='Ice cream']]//div[@class='counter-plus']")
    ICE_CREAM_COUNTER_LOCATOR = (By.XPATH, "//div[label[text()='Ice cream']]//div[@class='counter-value']")
    ORDER_BUTTON_LOCATOR = (By.XPATH, "//div[@class='smart-button-wrapper']/button")
    CAR_SEARCH_MODAL_LOCATOR = (By.CLASS_NAME, 'order-body')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    # --- Methods ---
    def set_route(self, from_address, to_address):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.driver.find_element(*self.FROM_LOCATOR).send_keys(from_address)
        self.driver.find_element(*self.TO_LOCATOR).send_keys(to_address)



    def get_from_field_value(self):
        return self.driver.find_element(*self.FROM_LOCATOR).get_attribute('value')

    def select_supportive_plan(self):
        self.driver.find_element(*self.CALL_TAXI_BUTTON_LOCATOR).click()
        plan = self.driver.find_element(*self.SUPPORTIVE_PLAN_LOCATOR)
        # Click only if it's not already selected
        if 'active' not in plan.get_attribute('class'):
            plan.click()

    def is_supportive_plan_selected(self):
        return 'active' in self.driver.find_element(*self.SUPPORTIVE_PLAN_LOCATOR).get_attribute('class')

    def add_phone_number(self, phone):
        self.driver.find_element(*self.PHONE_FIELD_LOCATOR).click()
        self.driver.find_element(*self.PHONE_INPUT_LOCATOR).send_keys(phone)
        self.driver.find_element(*self.PHONE_NEXT_BUTTON_LOCATOR).click()

    def enter_sms_code(self, code):
        self.driver.find_element(*self.SMS_CODE_INPUT_LOCATOR).send_keys(code)
        self.driver.find_element(*self.CONFIRM_BUTTON_LOCATOR).click()

    def get_confirmed_phone_number(self):
        return self.wait.until(EC.visibility_of_element_located(self.CONFIRMED_PHONE_LOCATOR)).text

    def add_credit_card(self, card_number, cvv):
        self.driver.find_element(*self.PAYMENT_METHOD_LOCATOR).click()

        # Wait for the element and click it in one action
        self.wait.until(EC.element_to_be_clickable(self.ADD_CARD_LINK_LOCATOR)).click()

        # Wait for the modal to fully load
        card_number_field = self.wait.until(EC.element_to_be_clickable(self.CARD_NUMBER_INPUT_LOCATOR))
        card_cvv_field = self.wait.until(EC.element_to_be_clickable(self.CARD_CVV_INPUT_LOCATOR))

        # Debug: Check if elements are found
        print(f"Card number field found: {card_number_field}")
        print(f"CVV field found: {card_cvv_field}")
        print(f"Trying to enter: {card_number} and {cvv}")

        # Click to focus, clear, then enter data
        card_number_field.click()
        card_number_field.clear()
        card_number_field.send_keys(str(card_number))

        card_cvv_field.click()
        card_cvv_field.clear()
        card_cvv_field.send_keys(str(cvv))

        # Use TAB to change focus
        card_cvv_field.send_keys(Keys.TAB)

        # Wait for Link button to be clickable and click it
        self.wait.until(EC.element_to_be_clickable(self.LINK_CARD_BUTTON_LOCATOR)).click()

    def is_card_linked(self):
        return self.wait.until(EC.invisibility_of_element_located(self.PAYMENT_MODAL_CLOSE_LOCATOR))

    def add_comment(self, comment_text):
        self.driver.find_element(*self.COMMENT_FIELD_LOCATOR).send_keys(comment_text)

    def get_comment_text(self):
        return self.driver.find_element(*self.COMMENT_FIELD_LOCATOR).get_attribute('value')

    def select_blanket_and_handkerchiefs(self):
        self.driver.find_element(*self.BLANKET_SWITCH_LOCATOR).click()

    def is_blanket_selected(self):
        return self.driver.find_element(*self.BLANKET_CHECKBOX_LOCATOR).is_selected()

    def order_ice_creams(self, count):
        ice_cream_button = self.driver.find_element(*self.ICE_CREAM_PLUS_LOCATOR)
        for _ in range(count):
            ice_cream_button.click()

    def get_ice_cream_counter(self):
        return self.driver.find_element(*self.ICE_CREAM_COUNTER_LOCATOR).text

    def click_order_button(self):
        self.driver.find_element(*self.ORDER_BUTTON_LOCATOR).click()

    def is_car_search_modal_visible(self):
        return self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_MODAL_LOCATOR)).is_displayed()
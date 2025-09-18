import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import data
import helpers
from pages import UrbanRoutesPage

class TestUrbanRoutes:
    driver = None

    def setup_method(self):
        # Do not modify - we need additional logging enabled
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}

        self.driver = webdriver.Chrome()
        self.driver.get(data.URBAN_ROUTES_URL)
        self.driver.implicitly_wait(10)

    def test_end_to_end(self):
        routes_page = UrbanRoutesPage(self.driver)

        # Set route
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert self.driver.find_element(By.ID, 'from').get_attribute('value') == data.ADDRESS_FROM
        assert self.driver.find_element(By.ID, 'to').get_attribute('value') == data.ADDRESS_TO

        # Select Supportive plan
        routes_page.select_supportive_plan()
        assert routes_page.is_supportive_plan_selected()

        # Add phone number
        routes_page.add_phone_number(data.PHONE_NUMBER)
        code = helpers.retrieve_phone_code(self.driver)
        routes_page.enter_sms_code(code)
        assert routes_page.get_confirmed_phone_number() == data.PHONE_NUMBER

        # Add credit card
        routes_page.add_credit_card(data.CARD_NUMBER, data.CARD_CODE)
        assert routes_page.is_card_linked()

        # Add a comment for the driver
        routes_page.add_comment(data.MESSAGE_FOR_DRIVER)
        assert routes_page.get_comment_text() == data.MESSAGE_FOR_DRIVER

        # Order a blanket and handkerchiefs
        routes_page.select_blanket_and_handkerchiefs()
        assert routes_page.is_blanket_selected()

        # Click order button
        routes_page.click_order_button()

        # Verify car search modal is visible
        assert routes_page.is_car_search_modal_visible()

    def teardown_method(self):
        self.driver.quit()
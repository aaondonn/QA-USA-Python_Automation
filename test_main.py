from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from data import CARD_NUMBER, CARD_CODE
from pages import UrbanRoutesPage
import data
import helpers
import time


class TestUrbanRoutes:
    driver = None

    def setup_method(self):
        """
        Runs before each test method.
        Initializes a fresh browser and navigates to the URL.
        """
        # Do not modify - we need additional logging enabled
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}

        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(data.URBAN_ROUTES_URL)
        self.driver.implicitly_wait(10)

    def test_set_route(self):
        """Tests that the route can be set successfully."""
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert routes_page.get_ADDRESS_FROM_value() == data.ADDRESS_FROM
        assert routes_page.get_field_to_value() == data.ADDRESS_TO

    def test_select_plan(self):
        """Tests that the 'Supportive' plan can be selected."""
        routes_page = UrbanRoutesPage(self.driver)
        # Prerequisite: Set the route to see the plans
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_supportive_plan()
        assert routes_page.is_supportive_plan_selected()


    def test_fill_phone_number(self):
        """Tests the full phone number entry and confirmation flow."""
        routes_page = UrbanRoutesPage(self.driver)
        # Prerequisites: Set route and select a plan
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_supportive_plan()

        routes_page.add_phone_number(data.PHONE_NUMBER)
        self.driver.implicitly_wait(10)
        code = helpers.retrieve_phone_code(self.driver)
        routes_page.enter_sms_code(code)
        assert routes_page.get_confirmed_phone_number() == data.PHONE_NUMBER

    def test_fill_card(self):
        """Tests adding a credit card as a payment method."""
        routes_page = UrbanRoutesPage(self.driver)
        # Prerequisites: Set route and select a plan
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_supportive_plan()

        # Pass the card details as strings
        routes_page.add_credit_card(data.CARD_NUMBER, data.CARD_CODE)

        assert routes_page.is_card_linked(), "Card was not linked successfully"

    def test_comment_for_driver(self):
        """Tests adding a message for the driver."""
        routes_page = UrbanRoutesPage(self.driver)
        # Prerequisites: Set route and select a plan
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_supportive_plan()

        routes_page.add_comment(data.MESSAGE_FOR_DRIVER)
        assert routes_page.get_comment_text() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        """Tests selecting the 'Blanket and handkerchiefs' extra."""
        routes_page = UrbanRoutesPage(self.driver)
        # Prerequisites: Set route and select a plan
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_supportive_plan()

        routes_page.select_blanket_and_handkerchiefs()
        assert routes_page.is_blanket_selected(), "Blanket was not selected"

    def test_order_2_ice_creams(self):
        """Tests ordering two ice creams."""
        routes_page = UrbanRoutesPage(self.driver)
        # Prerequisites: Set route and select a plan
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_supportive_plan()

        routes_page.order_ice_creams(count=2)
        assert routes_page.get_ice_cream_counter() == "2", "Ice cream count is not 2"

    def test_car_search_model_appears(self):
        """Tests the final step of ordering a taxi and verifying the modal appears."""
        routes_page = UrbanRoutesPage(self.driver)
        # Perform all steps required to get to the final order button
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_supportive_plan()
        routes_page.add_phone_number(data.PHONE_NUMBER)
        code = helpers.retrieve_phone_code(self.driver)
        routes_page.enter_sms_code(code)
        routes_page.add_credit_card(data.CARD_NUMBER, data.CARD_CODE)
        routes_page.add_comment("Order for the final test")

        routes_page.click_order_button()
        assert routes_page.is_car_search_modal_visible(), "Car search modal did not appear"

    def teardown_method(self):
        """Runs after each test method to close the browser."""
        self.driver.quit()
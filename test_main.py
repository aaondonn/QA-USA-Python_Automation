from selenium import webdriver

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

        self.driver = webdriver.Chrome()
        self.driver.get(data.URBAN_ROUTES_URL)
        self.driver.implicitly_wait(10)

    def test_set_route(self):
        """Tests that the route can be set successfully."""
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route("East 2nd Street, 601", "1300 1st St")
        assert routes_page.get_ADDRESS_FROM_value() == "East 2nd Street, 601"
        assert routes_page.get_field_to_value() == "1300 1st St"

    def test_select_plan(self):
        """Tests that the 'Supportive' plan can be selected."""
        routes_page = UrbanRoutesPage(self.driver)
        # Prerequisite: Set the route to see the plans
        routes_page.set_route("East 2nd Street, 601", "1300 1st St")
        routes_page.select_supportive_plan

    def test_fill_phone_number(self):
        """Tests the full phone number entry and confirmation flow."""
        routes_page = UrbanRoutesPage(self.driver)
        # Prerequisites: Set route and select a plan
        routes_page.set_route("East 2nd Street, 601", "1300 1st St")
        routes_page.select_supportive_plan()

        routes_page.add_phone_number("+1 123 123 12 12")
        self.driver.implicitly_wait(10)
        code = helpers.retrieve_phone_code(self.driver)
        routes_page.enter_sms_code(code)
        assert routes_page.get_confirmed_phone_number() == "+1 123 123 12 12"

    def test_fill_card(self):
        """Tests adding a credit card as a payment method."""
        routes_pages = UrbanRoutesPage(self.driver)
        # Prerequisites: Set route and select a plan
        routes_pages.set_route("East 2nd Street, 601", "1300 1st St")
        routes_pages.select_supportive_plan()

        # Pass the card details as strings
        routes_pages.add_credit_card("1234567891011121", "123")

        assert routes_pages.is_card_linked(), "Card was not linked successfully"

    def test_comment_for_driver(self):
        """Tests adding a message for the driver."""
        routes_page = UrbanRoutesPage(self.driver)
        # Prerequisites: Set route and select a plan
        routes_page.set_route("East 2nd Street, 601", "1300 1st St")
        routes_page.select_supportive_plan()

        comment = "Please meet at the main entrance."
        routes_page.add_comment(comment)
        assert routes_page.get_comment_text() == comment

    def test_order_blanket_and_handkerchiefs(self):
        """Tests selecting the 'Blanket and handkerchiefs' extra."""
        routes_page = UrbanRoutesPage(self.driver)
        # Prerequisites: Set route and select a plan
        routes_page.set_route("East 2nd Street, 601", "1300 1st St")
        routes_page.select_supportive_plan()

        routes_page.select_blanket_and_handkerchiefs()
        assert routes_page.is_blanket_selected(), "Blanket was not selected"

    def test_order_2_ice_creams(self):
        """Tests ordering two ice creams."""
        routes_page = UrbanRoutesPage(self.driver)
        # Prerequisites: Set route and select a plan
        routes_page.set_route("East 2nd Street, 601", "1300 1st St")
        routes_page.select_supportive_plan()

        routes_page.order_ice_creams(count=2)
        assert routes_page.get_ice_cream_counter() == "2", "Ice cream count is not 2"

    def test_car_search_model_appears(self):
        """Tests the final step of ordering a taxi and verifying the modal appears."""
        routes_page = UrbanRoutesPage(self.driver)
        # Perform all steps required to get to the final order button
        routes_page.set_route("East 2nd Street, 601", "1300 1st St")
        routes_page.select_supportive_plan()
        routes_page.add_phone_number("123-456-7890")
        code = helpers.retrieve_phone_code(self.driver)
        routes_page.enter_sms_code(code)
        routes_page.add_credit_card("1234567891011121", "123")
        routes_page.add_comment("Order for the final test")

        routes_page.click_order_button()
        assert routes_page.is_car_search_modal_visible(), "Car search modal did not appear"

    def teardown_method(self):
        """Runs after each test method to close the browser."""
        self.driver.quit()
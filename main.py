import unittest
import time
from selenium import webdriver
from pages import OrderPage


# Renamed to match your original test class name
class TestUrbanRoutes(unittest.TestCase):

    # It's better to initialize these in setUp to ensure each test is isolated.
    # driver = None
    # order_page = None

    # We will use instance-level setup and teardown instead of class-level.
    # This is more robust and ensures a clean state for each test.
    def setUp(self):
        """Set up the test environment before each test."""
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.order_page = OrderPage(self.driver)
        # The driver.get() method will handle connection errors,
        # which is a more standard approach for WebDriver tests.
        self.driver.get("https://cnt-17aa8ae4-a756-4bf4-8fcb-69bc74150e95.containerhub.tripleten-services.com/")

    def tearDown(self):
        """Clean up after each test has run."""
        self.driver.quit()

    def test_full_order_flow(self):
        """
        Tests a full order flow, combining the original separate tests
        into a single, logical user journey.
        """
        print("\n--- Starting Urban Routes Order Flow Test ---")

        # This section corresponds to your original 'test_set_route'
        self.order_page.set_route("east 2nd ST, 601", "1300 1st, st")
        print("1. Route has been set.")

        # This corresponds to 'test_select_plan'
        self.order_page.select_comfort_plan()
        print("2. 'Comfort' plan has been selected.")

        # This corresponds to 'test_fill_phone_number'
        self.order_page.set_phone_number("+15551234567")
        print("3. Phone number has been filled.")

        # This corresponds to 'test_fill_card'
        self.order_page.set_payment_method_to_card("1234 5678 9101 1121", "123")
        print("4. Card details have been filled.")

        # This corresponds to 'test_comment_for_driver'
        self.order_page.set_comment_for_driver("Please call upon arrival.")
        print("5. Comment for the driver has been added.")

        # This corresponds to 'test_order_blanket_and_handkerchiefs'
        self.order_page.order_blanket_and_handkerchiefs()
        print("6. Ordered a blanket and handkerchiefs.")

        # This corresponds to 'test_order_2_ice_creams'
        self.order_page.add_ice_creams(2)
        print("7. Successfully ordered 2 ice creams.")

        # This section click the final button and checks the result,
        # corresponding to 'test_car_search_model_appears'
        self.order_page.click_order_button()
        print("8. Order button clicked.")

        time.sleep(1)

        self.assertTrue(self.order_page.is_car_search_modal_visible(),
                        "Car search modal should be visible.")
        print("9. Car search modal has appeared as expected. Test passed!")


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)


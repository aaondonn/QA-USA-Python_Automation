from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



    FROM_LOCATOR = (By.ID, 'from')
    TO_LOCATOR = (By.ID, 'to')

    def __init__(self, driver):
        self.driver = driver

    def set_route(self, from_address, to_address):









    def click_order_button(self):

    def is_car_search_modal_visible(self):
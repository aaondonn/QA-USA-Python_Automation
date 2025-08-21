import data
import helpers
from helpers import is_url_reachable


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        if is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            # If it fails:
            print("Cannot connect to Urban Routes. Check the server is on and still running")

    def test_set_route(self):
        # Add in S8
        print("function created for setting route")
        pass

    def test_select_plan(self):
        # Add in S8
        print("function for selecting a plan")
        pass

    def test_fill_phone_number(self):
        # Add in S8
        print("function for filling a phone number")
        pass

    def test_fill_card(self):
        # Add in S8
        print("function for filling a card")
        pass

    def test_comment_for_driver(self):
        # Add in S8
        print("function for comment for driver")
        pass

    def test_order_blanket_and_handkerchiefs(self):
        # Add in S8
        print("function for ordering blanket and handkerchiefs")
        pass

    def test_order_2_ice_creams(self):
        for i in range(2):
            # Add in S8
            print("function for ordering 2 ice creams")
            pass

    def test_car_search_model_appears(self):
        # Add in S8
        print("function for car model searches")
        pass
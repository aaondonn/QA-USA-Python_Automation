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

# Add in S8
def test_set_route():
    print("function created for set route")
    pass

  # Add in S8
def test_select_plan(self):
    print()
    pass

  # Add in S8
def test_fill_phone_number(self):
    print()
    pass

   # Add in S8
def test_fill_card(self):
    print()
    pass

  # Add in S8
def test_comment_for_driver(self):
    print()
    pass

 # Add in S8
def test_order_blanket_and_handkerchiefs(self):
    print()
    pass

# Add in S8
def test_order_2_ice_creams(self):
    for i in range(2):
        print()
        pass

    # Add in S8
def test_car_search_model_appears(self):
    print()
    pass
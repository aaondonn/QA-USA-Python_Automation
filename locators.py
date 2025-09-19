from selenium.webdriver.common.by import By

class OrderPageLocators:
    """
    Locators for the Urban Routes order page.
    """
    # Stage 1: Setting the Route
    FROM_FIELD = (By.ID, "from")
    TO_FIELD = (By.ID, "to")
    CALL_TAXI_BUTTON = (By.XPATH, "//button[text()='Call a taxi']")

    # Stage 2: Selecting Tariff
    # Locators are now hardcoded to specifically target the 'Supportive' plan.
    SUPPORTIVE_TARIFF = (By.XPATH, "//div[@class='tcard-title' and text()='Supportive']")
    ACTIVE_SUPPORTIVE_TARIFF = (By.XPATH, "//div[contains(@class, 'tcard-active')]//div[text()='Supportive']")

    # Stage 3: Phone Number
    PHONE_FIELD = (By.ID, "phone")
    PHONE_SUBMIT_BUTTON = (By.XPATH, "//div[contains(@class, 'number-picker')]//button[text()='Next']")
    CODE_FIELD = (By.ID, "code")
    CONFIRM_CODE_BUTTON = (By.XPATH, "//div[contains(@class, 'number-picker')]//button[text()='Confirm']")

    # Stage 4: Payment Method
    PAYMENT_METHOD_BUTTON = (By.CLASS_NAME, "pp-button")
    PAYMENT_MODAL = (By.CLASS_NAME, "payment-picker") # For focus change
    ADD_CARD_LINK = (By.CLASS_NAME, "pp-plus")
    CARD_NUMBER_FIELD = (By.CSS_SELECTOR, ".card-form #number")
    CARD_CODE_FIELD = (By.CSS_SELECTOR, ".card-form #code")
    CARD_SUBMIT_BUTTON = (By.XPATH, "//div[@class='card-form']//button[text()='Link']")
    CLOSE_PAYMENT_MODAL_BUTTON = (By.CSS_SELECTOR, ".payment-picker.open .close-button")

    # Stage 5: Other Details
    COMMENT_FIELD = (By.ID, "comment")
    BLANKET_SWITCH = (By.XPATH, "//div[text()='Blanket and handkerchiefs']/following-sibling::div//label")
    BLANKET_SWITCH_CHECKBOX = (By.XPATH, "//div[text()='Blanket and handkerchiefs']/ancestor::div[contains(@class, 'r-sw')]//input")
    ICE_CREAM_COUNTER = (By.XPATH, "//div[text()='Ice cream']/following-sibling::div//div[contains(@class, 'counter-value')]")
    ICE_CREAM_PLUS_BUTTON = (By.XPATH, "//div[text()='Ice cream']/following-sibling::div//div[@class='counter-plus']")

    # Final Stage: Order Button and Verification
    ORDER_BUTTON = (By.CLASS_NAME, "smart-button")
    CAR_SEARCH_MODAL_TITLE = (By.CLASS_NAME, "order-header-title")


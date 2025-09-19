from selenium.webdriver.common.by import By

class OrderPageLocators:
    """
    Locators for the Urban Routes order page.
    """
    # Stage 1: Setting the Route
    FROM_FIELD = (By.ID, "from")
    TO_FIELD = (By.ID, "to")
    ORDER_BUTTON_INITIAL = (By.XPATH, '//button[@class="button round"]')
    CUSTOM_OPTION_LOCATOR = (By.XPATH, '//div[text()="Custom"]')

    # Stage 2: Selecting Tariff
    SUPPORTIVE_TARIFF = (By.XPATH, "//div[@class='tcard-title' and text()='Supportive']")
    ACTIVE_TARIFF_TEXT = (By.CSS_SELECTOR, ".tcard.active .tcard-title")

    # Stage 3: Phone Number
    # ✨ ADDED: Locator for the button that opens the phone input modal
    PHONE_NUMBER_BUTTON = (By.CLASS_NAME, "np-button")
    PHONE_FIELD = (By.ID, "phone")
    PHONE_SUBMIT_BUTTON = (By.XPATH, "//div[contains(@class, 'number-picker')]//button[text()='Next']")
    CODE_FIELD = (By.ID, "code")
    # ✨ ADDED: The missing locator for the "Confirm" button
    CONFIRM_CODE_BUTTON = (By.XPATH, "//div[contains(@class, 'number-picker')]//button[text()='Confirm']")

    # Stage 4: Payment Method
    PAYMENT_METHOD_BUTTON = (By.CLASS_NAME, "pp-button")
    PAYMENT_METHOD_TEXT = (By.CSS_SELECTOR, ".pp-button .pp-value-text")
    ADD_CARD_LINK = (By.CLASS_NAME, "pp-plus")
    CARD_NUMBER_FIELD = (By.CSS_SELECTOR, "input#number.card-input")
    CARD_CODE_FIELD = (By.CSS_SELECTOR, "input#code.card-input")
    # ✨ UPDATED: Using your new, more reliable selector for the 'Link' button
    CARD_SUBMIT_BUTTON = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')
    CLOSE_PAYMENT_MODAL_BUTTON = (By.CSS_SELECTOR, ".payment-picker.open .close-button")

    # Stage 5: Other Details
    COMMENT_FIELD = (By.ID, "comment")
    BLANKET_SWITCH = (By.XPATH, "//div[contains(., 'Blanket and handkerchiefs')]//div[@class='r-sw']")
    BLANKET_SWITCH_CHECKBOX = (By.XPATH, "//div[text()='Blanket and handkerchiefs']/../..//input[@type='checkbox']")
    ICE_CREAM_PLUS_BUTTON = (By.XPATH, "//div[text()='Ice cream']/following-sibling::div//div[@class='counter-plus']")
    ICE_CREAM_COUNTER = (By.XPATH, "//div[text()='Ice cream']/following-sibling::div//div[contains(@class, 'counter-value')]")

    # Final Stage: Order Button and Verification
    ORDER_BUTTON_FINAL = (By.CSS_SELECTOR, ".smart-button-wrapper button")
    CAR_SEARCH_MODAL = (By.CLASS_NAME, "order-header")
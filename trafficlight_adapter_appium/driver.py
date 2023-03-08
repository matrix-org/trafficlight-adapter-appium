from typing import Dict, Any

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver


class TrafficlightDriver:
    def __init__(self, driver: WebDriver, appium_type: str):
        self.driver = driver
        self.appium_type = appium_type
        self._android = self.appium_type == "sl-android" or self.appium_type == "bs-android" or self.appium_type == "local-android"

    def find_element(self, identifier: str):
        if self._android:
            self.driver.find_element(by=AppiumBy.XPATH, value='//*[@resource-id="'+identifier+'"]')
        else:
            self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=identifier)


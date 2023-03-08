import logging

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver

logger = logging.getLogger(__name__)


class TrafficlightDriver:
    def __init__(self, driver: WebDriver, appium_type: str):
        self.driver = driver
        self.appium_type = appium_type
        self._android = self.appium_type == "sl-android" or \
                        self.appium_type == "bs-android" or \
                        self.appium_type == "local-android"

    def find_element(self, identifier: str):
        if self._android:
            # This method is required because while it looks like we should be able to find resource-id using By.ID
            # the underlying uiautomator2 code prepends a package to it (eg, io.element.x.android) which is then
            # not found. So we use xpath to search for exactly one element by resource-id. A bit slower but not bad.
            # This also would be less of a problem if we weren't using jetpack compose; there isn't the same resource-id
            # model for items created that way.
            return self.driver.find_element(by=AppiumBy.XPATH, value='//*[@resource-id="' + identifier + '"]')
        else:
            # iOS is fine because ACCESSIBILITY_IDs are in place.
            return self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=identifier)

    def finish(self):
        logger.info("Terminal page source: " + self.driver.page_source)
        self.driver.quit()

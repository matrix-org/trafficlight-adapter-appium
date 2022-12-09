import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    appPackage='io.element.android.x',
    appActivity='.MainActivity',
    language='en',
    locale='GB',
    adbExecTimeout="30000",
    disableIdLocatorAutocompletion=True,
)

appium_server_url = 'http://localhost:4723'

class Adapter():
  def setup(self) -> None:
    self.driver = webdriver.Remote(appium_server_url, capabilities)
    self.driver.implicitly_wait(30) # waits up to 5 seconds when finding elements
    print ("Finished setup")

  def finish(self) -> None:
    if self.driver:
       print ("Tearing down driver")
       self.driver.quit()
       self.driver = None

  def login(self, server: str, user: str, passwd: str) -> None:
     time.sleep(5)
     el = self.driver.find_element(by=AppiumBy.ID, value='sign_in')
     el.click()
     el = self.driver.find_element(by=AppiumBy.ID, value='login-change_server')
     el.click()
     el = self.driver.find_element(by=AppiumBy.ID, value='change_server-server')
     el.clear()
     el.send_keys(server)
     el = self.driver.find_element(by=AppiumBy.ID, value='change_server-continue')
     el.click()
     el = self.driver.find_element(by=AppiumBy.ID, value='login-email_username')
     el.clear()
     el.send_keys(user)
     el = self.driver.find_element(by=AppiumBy.ID, value='login-password')
     el.clear()
     el.send_keys(passwd)
     el = self.driver.find_element(by=AppiumBy.ID, value='login-continue')
     el.click()

	



if __name__ == '__main__':
  adapter = Adapter()
  adapter.setup()
  adapter.login('matrix.org','wibble','wobble')
  time.sleep(5)
  adapter.finish()
 

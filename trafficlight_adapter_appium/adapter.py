import logging
import uuid

import requests
from appium import webdriver

from trafficlight_adapter_appium.action import system, login, room, crypto
from trafficlight_adapter_appium.driver import TrafficlightDriver
from trafficlight_adapter_appium.request import Request
from trafficlight_adapter_appium.response import Response

logger = logging.getLogger(__name__)

class Adapter:
    def __init__(self, args):
        self.trafficlight_url = args.trafficlight_url
        self.uuid = uuid.uuid4()
        self.actions = {
            "idle": system.idle,
            "login": login.login,
            "logout": login.logout,
            "open_room": room.open_room,
            "get_timeline": room.get_timeline,
            "start_crosssign": crypto.start_crosssign,
            "accept_crosssign": crypto.accept_crosssign,
            "verify_crosssign": crypto.verify_crosssign,
            "verify_crosssign_emoji": crypto.verify_crosssign,
        }
        self.args = args
        self.driver = None

    def create_driver(self) -> TrafficlightDriver:

        if self.args.appium_type == 'local-android':
            capabilities = dict(
                platformName='Android',
                automationName='uiautomator2',
                deviceName='Android',
                appPackage=self.args.package,
                appActivity='io.element.android.x.MainActivity',
                language='en',
                locale='GB',
                adbExecTimeout="30000",
                disableIdLocatorAutocompletion=True,
            )
            appium_url = "http://localhost:4567"

        if self.args.appium_type == 'local-ios':
            capabilities = {}
            appium_url = "http://localhost:4567"


        if self.args.appium_type == 'sl-android':
            capabilities =  {
                "platformName" : "Android",
                "automationName": 'uiautomator2',
                "platformVersion" : "12.0",
                "deviceName" : "Android GoogleAPI Emulator",
                "app" : "storage:filename=eax-nightly.apk",
                'sauce:options' : {
                    "build": "appium-build-PLUR4",
                    "name": "trafficlight"
                },
            }
            appium_url = f"https://{self.args.username}:{self.args.password}@ondemand.eu-central-1.saucelabs.com:443/wd/hub"
            logger.info(appium_url)

        if self.args.appium_type == 'sl-ios':
            capabilities = {
                "platformName": "iOS",
                "appium:deviceName": "iPhone.*",
                "appium:automationName": "XCUITest",
                "appium:app": "storage:filename=element-x-ios-pr.ipa",
                "sauce:options": {
                    "name": "trafficlight",
                    "build": "lalalal",
                }
            }
            appium_url = f"https://{self.args.username}:{self.args.password}@ondemand.eu-central-1.saucelabs.com:443/wd/hub"
            logger.info(appium_url)
        
        if self.args.appium_type == 'bs-android':
            capabilities =  {
                "platformName" : "android",
                "platformVersion" : "9.0",
                "automationName": 'uiautomator2',
                "deviceName" : "Google Pixel 3",
                "app" : "eax-nightly",
                'bstack:options' : {
                    "projectName" : "trafficlight",
                    "appiumVersion" : "2.0.0",
                    "disableAnimations" : "true",
                    "userName": self.args.username,
                    "accessKey": self.args.password,
                },
            }
            appium_url = f"http://{self.args.username}:{self.args.password}@hub.browserstack.com/wd/hub"

        if self.args.appium_type == 'bs-ios':
            capabilities = {
                "platformName": "ios",
                "appium:deviceName": "iPhone 14",
                "appium:app": "element-x-ios-pr",
                "bstack-options": {
                    "projectName": "trafficlight",
                    "appiumVersion": "2.0.0",
                    "disableAnimations": "true",
                    "userName": self.args.username,
                    "accessKey": self.args.password
                }
            }
            logger.info(capabilities)
            appium_url = f"http://{self.args.username}:{self.args.password}@hub.browserstack.com/wd/hub"

            # One-off actions should leave app as it was found.
        if self.args.one_off:
            capabilities['noReset'] = True

        driver = webdriver.Remote(appium_url, capabilities)
        driver.implicitly_wait(30)
        self.driver = TrafficlightDriver(driver, self.args.appium_type)
        return self.driver

    def register(self) -> None:
        if self.args.appium_type == "bs-android" or self.args.appium_type == "local-android" or self.args.appium_type == "sl-android":
            reg_type = "element-android"
        else:
            reg_type = "element-ios"

        registration_json = {
            "type": reg_type,
            "version": "UNKNOWN"
        }
        requests.post(f"{self.trafficlight_url}/client/{self.uuid}/register",
                      json=registration_json
                      )
        # TODO: check if needs type application/json

    def run(self) -> None:


        # urgh, maybe better as two separate loops?
        try:
            while (True):
                poll_rsp = self.poll()
                if self.driver is None:
                    if poll_rsp.action == "idle":
                        action = self.actions[poll_rsp.action]
                        logger.info(f"{poll_rsp.action} {poll_rsp.data}")
                        action(self.driver, poll_rsp)
                    else:
                        self.create_driver() # Side effect: driver is now not None
                        action = self.actions[poll_rsp.action]
                        logger.info(f"{poll_rsp.action} {poll_rsp.data}")
                        action_rsp = action(self.driver, poll_rsp)
                        self.respond(action_rsp)
                else:
                    # General loop.
                    action = self.actions[poll_rsp.action]
                    logger.info(f"{poll_rsp.action} {poll_rsp.data}")
                    action_rsp = action(self.driver, poll_rsp)
                    if poll_rsp.action != "idle":
                        self.respond(action_rsp)
                # and loop until bored...
        except Exception as e:
            source = self.driver.page_source
            logger.error(f"Context:\n {source}")
            raise e
        finally:
            self.driver.finish()

    def poll(self) -> Request:
        rsp = requests.get(f"{self.trafficlight_url}/client/{self.uuid}/poll")
        return Request(rsp.json())

    def respond(self, response: Response) -> None:
        rsp = requests.post(f"{self.trafficlight_url}/client/{self.uuid}/respond", response.data)
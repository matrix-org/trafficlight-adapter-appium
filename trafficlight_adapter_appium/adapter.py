import argparse
import uuid

import requests
import logging

from appium import webdriver
from appium.webdriver.webdriver import WebDriver
from action import system, login, room
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

        }
        self.args = args
        self.driver = None

    def create_driver(self) -> WebDriver:

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


        if self.args.appium_type == 'bs-android':
            capabilities =  {
                "platformName" : "android",
                "platformVersion" : "9.0",
                "deviceName" : "Google Pixel 3",
                "app" : "eax-nightly",
                'bstack:options' : {
                    "projectName" : "trafficlight",
                    "appiumVersion" : "2.0.0",
                    "disableAnimations" : "true",
                    "userName": self.args.browserstack_username,
                    "accessKey": self.args.browserstack_password,
                },
            }
            appium_url = "http://hub.browserstack.com/wd/hub"

        if self.args.appium_type == 'bs-ios':
                capabilities = {
                    "app": "eix-nightly",
                    'bstack:options': {
                        "projectName": "trafficlight",
                        "appiumVersion": "2.0.0",
                        "disableAnimations": "true",
                        "userName": self.args.browserstack_username,
                        "accessKey": self.args.browserstack_password,
                    },
                },

                appium_url = "http://hub.browserstack.com/wd/hub"

            # One-off actions should leave app as it was found.
        if self.args.one_off:
            capabilities['noReset'] = True

        driver = webdriver.Remote(appium_url, capabilities)
        driver.implicitly_wait(30)
        self.driver = driver
        return driver

    def register(self) -> None:
        registration_json = {
            "type": "element-android",
            "version": "UNKNOWN"
        }
        requests.post(f"{self.trafficlight_url}/client/{self.uuid}/register",
                      json=registration_json
                      )
        # TODO: check if needs type application/json

    def run(self) -> None:


        # urgh, maybe better as two separate loops?

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
                    action(self.driver, poll_rsp)
                    self.respond(action_rsp)
            else:
                # General loop.
                action = self.actions[poll_rsp.action]
                logger.info(f"{poll_rsp.action} {poll_rsp.data}")
                action_rsp = action(self.driver, poll_rsp)

                self.respond(action_rsp)
            # and loop until bored...

    def poll(self) -> Request:
        rsp = requests.get(f"{self.trafficlight_url}/client/{self.uuid}/poll")
        return Request(rsp.json())

    def respond(self, response: Response) -> None:
        rsp = requests.post(f"{self.trafficlight_url}/client/{self.uuid}/respond", response.data)

def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(description="Appium adapter for trafficlight")
    parser.add_argument(
        "--trafficlight-url",
        dest="trafficlight_url",
        type=str,
        default="http://localhost:5000",
        help="HTTP(S) endpoint to connect to trafficlight",
    )

    parser.add_argument(
        "--package",
        dest="package",
        type=str,
        default='io.element.android.x.debug',
        help="Package of build being worked with"
    )

    parser.add_argument(
        "--app-file",
        dest="apk",
        type=str,
        help="File on disk to upload to device"
    )

    parser.add_argument(
        "--bs-uri",
        dest="browserstack_uri",
        type=str,
        help="Browserstack uploaded URI (bs://....)"
    )

    parser.add_argument(
        "--appium-type",
        dest="appium_type",
        choices=['local-android', 'local-ios', 'bs-android', 'bs-ios'],
        help="Appium provider"
    )

    parser.add_argument(
        "--user",
        dest="browserstack_username",
        help="browserstack username"
    )
    parser.add_argument(
        "--pass",
        dest="browserstack_password",
        help="browserstack password"
    )

    parser.add_argument(
        "--one-off",
        dest="one_off",
        action="store_true",
        help="Run a one-off action"
    )

    parser.add_argument(
        "--action",
        dest="one_off_action",
        type=str,
        help="Action to perform"
    )

    parser.add_argument(
        "--data",
        dest="one_off_data",
        action="append",
        type=str,
        default=[],
        help="Data for one-off action, in NAME=VALUE format"
    )

    args = parser.parse_args()
    if args.one_off:
        adapter = Adapter(args)
        adapter.create_driver()
        action = args.one_off_action
        action_function = adapter.actions.get(action)
        data = {}
        for item in args.one_off_data:
            (key,value) = item.split('=')
            data[key] = value

        request = Request({"action": action, "data": data})
        response = action_function(adapter.driver,request)
        print(response.data)
    else:
        adapter = Adapter(args)
        adapter.register()
        # Wait until mid-run to create driver...
        adapter.run()



if __name__ == '__main__':
    main()

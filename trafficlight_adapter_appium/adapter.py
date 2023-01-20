import argparse
import uuid

import requests

from appium import webdriver
from appium.webdriver.webdriver import WebDriver
from action import system, login, room
from trafficlight_adapter_appium.request import Request


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
        self.driver = self.create_driver(args)

    def create_driver(self, args) -> WebDriver:
        capabilities = dict(
            platformName='Android',
            automationName='uiautomator2',
            deviceName='Android',
            appPackage=args.package,
            appActivity='.MainActivity',
            language='en',
            locale='GB',
            adbExecTimeout="30000",
            disableIdLocatorAutocompletion=True,
        )
        # One-off actions should leave app as it was found.
        if args.one_off:
            capabilities['noReset'] = True

        driver = webdriver.Remote(args.appium_url, capabilities)
        driver.implicitly_wait(30)  # waits up to 5 seconds when finding elements
        return driver

    def register(self) -> None:
        registration_json = {
            "type": "element-android",
            "version": "UNKNOWN"
        }
        requests.post(f"${self.trafficlight_url}/client/${self.uuid}/register",
                      json=registration_json
                      )
        # TODO: check if needs type application/json

    def run(self) -> None:
        while (True):
            poll_rsp = self.poll()

            action = self.actions[poll_rsp.data]

            action_rsp = action(self.driver, poll_rsp)

            self.respond(action_rsp)
            # and loop until bored...

    def poll(self) -> Request:
        rsp = requests.get(f"${self.trafficlight_url}/client/${self.uuid}/poll")
        return Request(rsp.json())


def main():
    parser = argparse.ArgumentParser(description="Appium adapter for trafficlight")
    parser.add_argument(
        "--trafficlight-url",
        dest="trafficlight_url",
        type=str,
        help="HTTP(S) endpoint to connect to trafficlight",
    )
    parser.add_argument(
        "--package",
        dest="package",
        type=str,
        default='io.element.android.x',
        help="Package of build being worked with"
    )
    parser.add_argument(
        "--apk-file",
        dest="apk",
        type=str,
        help="APK to upload to device"
    )

    parser.add_argument(
        "--appium-url",
        dest="appium_url",
        type=str,
        default='http://localhost:4723',
        help="Appium URL to connect to"
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
        adapter.reset()
        adapter.run()



if __name__ == '__main__':
    main()

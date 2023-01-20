import argparse
import uuid

import requests

from typing import Any, Dict
from appium import webdriver
from action import system, login


class Request:
    def __init__(self, json: Dict[str, Any]):
        self.action = json['action']
        self.data = json['data']


class Response:
    def __init__(self, json: Dict[str, Any]):
        self.data = json


class Adapter:
    def __init__(self, args):
        self.trafficlight_url = args.trafficlight_url
        self.uuid = uuid.uuid4()
        self.actions = {
            "idle": system.idle,
            "login": login.login,
            "logout": login.logout,
            
        }
        self.driver = self.create_driver(args)

    def create_driver(self, args):
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

    args = parser.parse_args()
    if args.one_off:
        adapter = Adapter(args)
        action = adapter.actions.get(args.action)
        request = Request({"action": action, "data": {}})
        response = action(adapter.driver,request)
        print(response.data)
        
    adapter = Adapter(args)
    adapter.register()
    adapter.reset()
    adapter.run()



if __name__ == '__main__':
    main()

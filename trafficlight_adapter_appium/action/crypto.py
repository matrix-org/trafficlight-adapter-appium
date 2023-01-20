from appium.webdriver.common.appiumby import AppiumBy
from trafficlight_adapter_appium.action import ActionException
from trafficlight_adapter_appium.response import Response
from trafficlight_adapter_appium.request import Request
from typing import Optional



def start_crosssign(driver, request: Request) -> Response:
    user_id: Optional(str) = request.data["userId"]
    raise ActionException()

def accept_crosssign(driver, request: Request) -> Response:
    raise ActionException()


def verify_crosssign(driver, request: Request) -> Response:
    raise ActionException()

def verify_last_message_is_trusted(driver, request: Request) -> Response:
    raise ActionException()

def verify_last_message_is_utd(driver, request: Request) -> Response:
    raise ActionException()

def verify_trusted_device(driver, request: Request) -> Response:
    raise ActionException()

def enable_dehydrated_device(driver, request: Request) -> Response:
    key_backup_passphrase = request.data['key_backup_passphrase']
    raise ActionException()

def enable_key_backup(driver, request: Request) -> Response:
    key_backup_passphrase = request.data['key_backup_passphrase']
    raise ActionException()

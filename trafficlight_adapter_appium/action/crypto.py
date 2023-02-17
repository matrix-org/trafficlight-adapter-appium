from appium.webdriver.common.appiumby import AppiumBy
from trafficlight_adapter_appium.action import ActionException
from trafficlight_adapter_appium.response import Response
from trafficlight_adapter_appium.request import Request
import time

def start_crosssign(driver, request: Request) -> Response:
    if "user_id" in request.data:
        # We need to open a DM to the user and then sign the user there.
        raise ActionException()
    else:
        # Start crosssigning via popup
        driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="home_screen-verification_continue").click()
        time.sleep(5)  # the animation gets in the way of this click...

        driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="session_verification-request_verification").click()
        return Response({})


def accept_crosssign(driver, request: Request) -> Response:
    # Target has been notified they are being signed against and should agree.
    driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="session_verification-request_verification").click()
    driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="session_verification-start_sas_verification").click()
    return Response({})


def verify_crosssign(driver, request: Request) -> Response:
    driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='session_verification-emojis')
    # TOOD: parse out emojis and return to TL.
    time.sleep(5)  # the animation gets in the way of this click...

    driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='session_verification-accept_challenge').click()
    return Response({})


def verify_last_message_is_trusted(driver, request: Request) -> Response:
    raise ActionException()


def verify_last_message_is_utd(driver, request: Request) -> Response:
    raise ActionException()


def verify_trusted_device(driver, request: Request) -> Response:
    raise ActionException()


def enable_dehydrated_device(driver, request: Request) -> Response:
    if "key_backup_passphrase" in request.data:
        raise ActionException()
    else:
        raise ActionException()


def enable_key_backup(driver, request: Request) -> Response:
    if "key_backup_passphrase" in request.data:
        raise ActionException()
    else:
        raise ActionException()

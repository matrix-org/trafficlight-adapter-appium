from appium.webdriver.common.appiumby import AppiumBy

from trafficlight_adapter_appium.action import ActionException
from trafficlight_adapter_appium.adapter import Request, Response


def send_message(driver, request: Request) -> Response:
    message = request.data['message']
    # implementable....
    raise ActionException("Not implemented yet")


def create_room(driver, request: Request) -> Response:
    room_name = request.data['name']
    raise ActionException("Not implemented yet")


def create_dm(driver, request: Request) -> Response:
    user_id = request.data['userId']
    raise ActionException("Not implemented yet")


def invite_user(driver, request: Request) -> Response:
    user_id = request.data['userId']
    raise ActionException("Not implemented yet")


def accept_invite(driver, request: Request) -> Response:
    raise ActionException("Not implemented yet")


def open_room(driver, request: Request) -> Response:
    room_name = request.data['name']
    raise ActionException("Not implemented yet")


def change_room_history_visibility(driver, request: Request) -> Response:
    history_visibility = request.data['historyVisibility']
    raise ActionException("Not implemented yet")


def verify_message_in_timeline(driver, request: Request) -> Response:
    message = request.data["message"]
    raise ActionException("Not implemented yet")


def get_timeline(driver, request: Request) -> Response:
    raise ActionException("Not implemented yet")


def verify_last_message_is_trusted(driver, request: Request) -> Response:
    raise ActionException("Not implemented yet")


def verify_last_message_is_utd(driver, request: Request) -> Response:
    raise ActionException("Not implemented yet")


def verify_trusted_device(driver, request: Request) -> Response:
    raise ActionException("Not implemented yet")


def open_room(driver, request: Request) -> Response:
    """
    Also unfortunately bound as `open-room`
    """
    room_name = request.data["name"]
    raise ActionException("Not implemented yet")

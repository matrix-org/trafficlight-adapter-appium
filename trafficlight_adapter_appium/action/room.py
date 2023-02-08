from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webelement import WebElement
from appium.webdriver.webdriver import WebDriver
import xml.etree.ElementTree as ET

from trafficlight_adapter_appium.action import ActionException
from trafficlight_adapter_appium.response import Response
from trafficlight_adapter_appium.request import Request


def send_message(driver, request: Request) -> Response:
    message = request.data['message']
    # click on message text box
    el = driver.find_element(by=AppiumBy.ID, value="io.element.android.x:id/richTextComposerEditText")
    el.clear()
    el.send_keys(message)
    el = driver.find_element(by=AppiumBy.ID, value="io.element.android.x:id/sendButton")
    el.click()


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


def get_timeline(driver: WebDriver, request: Request) -> Response:

    el: WebElement = driver.find_element(by=AppiumBy.XPATH, value="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[2]")
    # EL is the timeline bounding box.
    # Note getting page source is SLOOOWW, but verbose. Useful for this timeline mangling
    page_source = driver.page_source

    root = ET.fromstring(page_source)

    # Top-level elements
    print(root)
    # Start at compose view to cut out all the layers
    compose_view = root.findall(".//*[@class='androidx.compose.ui.platform.ComposeView']")[0]
    print(compose_view)
    # Find the timeline view (TODO: select this by an ID instead!)
    timeline_view = compose_view.findall("./View/View/View[index=1]")
    for timeline_entry in timeline_view:
        print(timeline_entry)



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
    driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="search").click()
    # TODO: swap out for an ID of some form...
    el = driver.find_element(by=AppiumBy.XPATH, value="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[1]/android.widget.EditText")
    el.clear()
    el.send_keys(room_name)
    # Do a search as it pretty much guarantees the room name will be on screen at this point
    # TODO: swap out for something by ID here, but we work.
    el = driver.find_element(by=AppiumBy.XPATH, value="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[2]/android.view.View")
    el.click()
    return Response({})


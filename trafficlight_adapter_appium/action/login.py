import logging
import time

from appium.webdriver.common.appiumby import AppiumBy

from trafficlight_adapter_appium.response import Response
from trafficlight_adapter_appium.request import Request

logger = logging.getLogger(__name__)


def login(driver, request: Request) -> Response:
    user = request.data['username']
    passwd = request.data['password']
    server = request.data['homeserver_url']['local']

    adapted_server_name = server.replace("https://","")
    adapted_server_name = adapted_server_name.replace("http://", "")

    driver.find_element('onboarding-sign_in').click()
    time.sleep(5) # the animation gets in the way of this click...
    el = driver.find_element('login-change_server')
    logger.info(el)
    el.click()
    time.sleep(5)  # the animation gets in the way of this click...
    el = driver.find_element('change_server-server')
    el.clear()
    el.send_keys(adapted_server_name)
    driver.find_element('change_server-continue').click()
    el = driver.find_element('login-email_username')
    el.clear()
    el.send_keys(user)
    el = driver.find_element('login-password')
    el.clear()
    el.send_keys(passwd)
    driver.find_element('login-continue').click()
    return Response({})


def logout(driver, request: Request) -> Response:
    driver.find_element('logout').click()
    driver.find_element('continue').click()
    return Response({})

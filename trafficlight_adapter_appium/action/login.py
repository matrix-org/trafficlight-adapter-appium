from appium.webdriver.common.appiumby import AppiumBy

from trafficlight_adapter_appium.response import Response
from trafficlight_adapter_appium.request import Request


def login(driver, request: Request) -> Response:
    user = request.data['user']
    passwd = request.data['password']
    server = request.data['url']

    driver.find_element(by=AppiumBy.ID, value='sign_in').click()
    driver.find_element(by=AppiumBy.ID, value='login-change_server').click()
    el = driver.find_element(by=AppiumBy.ID, value='change_server-server')
    el.clear()
    el.send_keys(server)
    driver.find_element(by=AppiumBy.ID, value='change_server-continue').click()
    el = driver.find_element(by=AppiumBy.ID, value='login-email_username')
    el.clear()
    el.send_keys(user)
    el = driver.find_element(by=AppiumBy.ID, value='login-password')
    el.clear()
    el.send_keys(passwd)
    driver.find_element(by=AppiumBy.ID, value='login-continue').click()
    return Response({})


def logout(driver, request: Request) -> Response:
    driver.find_element(by=AppiumBy, value='logout').click()
    driver.find_element(by=AppiumBy, value='continue').click()
    return Response({})
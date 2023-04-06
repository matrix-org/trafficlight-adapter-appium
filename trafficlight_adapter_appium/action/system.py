import logging

from trafficlight_adapter_appium.response import Response
from trafficlight_adapter_appium.request import Request
from trafficlight_adapter_appium.action import ActionException
import time
import logging

logger = logging.getLogger(__name__)

def idle(driver, request: Request) -> Response:
    duration = int(request.data['delay'])
    time.sleep(duration / 1000)
    return Response({})

def exit(driver, request: Request) -> Response:
    logger.info("Closing down adapter on server request")
    return Response({})

def advance_clock(driver, request: Request) -> Response:
        time_ms = request.data['milliseconds']
        raise ActionException()

def reload(driver, request: Request) -> Response:
    """
    Not even sure if we should implement this; may be web specific
    """
    raise ActionException()


def clear_idb_storage(driver, request: Request) -> Response:
    """
    Not even sure if we should implement this; may be web specific
    """
    raise ActionException()

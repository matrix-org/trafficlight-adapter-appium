from trafficlight_adapter_appium.adapter import Request, Response
from trafficlight_adapter_appium.action import ActionException
import os

def idle(driver, request: Request) -> Response:
    duration = request.data['duration_ms']
    os.sleep(duration / 1000)
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

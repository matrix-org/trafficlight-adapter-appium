import argparse
import logging
from trafficlight_adapter_appium.adapter import Adapter
from trafficlight_adapter_appium.request import Request


logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Appium adapter for trafficlight")
    parser.add_argument(
        "--trafficlight-url",
        dest="trafficlight_url",
        type=str,
        default="http://localhost:5000",
        help="HTTP(S) endpoint to connect to trafficlight",
    )

    parser.add_argument(
        "--package",
        dest="package",
        type=str,
        default='io.element.android.x.debug',
        help="Package of build being worked with"
    )

    parser.add_argument(
        "--app-file",
        dest="apk",
        type=str,
        help="File on disk to upload to device"
    )

    parser.add_argument(
        "--bs-uri",
        dest="browserstack_uri",
        type=str,
        help="Browserstack uploaded URI (bs://....)"
    )

    parser.add_argument(
        "--appium-type",
        dest="appium_type",
        choices=['local-android', 'local-ios', 'bs-android', 'bs-ios', 'sl-android','sl-ios'],
        help="Appium provider"
    )

    parser.add_argument(
        "--user",
        dest="username",
        help="username"
    )
    parser.add_argument(
        "--pass",
        dest="password",
        help="Password"
    )
    
    parser.add_argument(
        "--api-key",
        dest="password",
        help="API Key"
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
        driver = adapter.create_driver()
        try:
            action = args.one_off_action
            action_function = adapter.actions.get(action)
            data = {}
            for item in args.one_off_data:
                (key,value) = item.split('=')
                data[key] = value

            request = Request({"action": action, "data": data})
            response = action_function(adapter.driver,request)
            print(response.data)
        finally:
            driver.finish()
    else:
        adapter = Adapter(args)
        adapter.register()
        # Wait until mid-run to create driver...
        adapter.run()



if __name__ == '__main__':
    main()

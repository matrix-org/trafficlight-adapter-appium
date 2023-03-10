FROM python:3.11-slim-buster

WORKDIR /app

COPY README.md /app
COPY setup.cfg /app
COPY pyproject.toml /app
COPY trafficlight_adapter_appium/ /app/trafficlight_adapter_appium/

RUN ls -la /app 
RUN python -m venv venv
RUN venv/bin/pip install --upgrade setuptools
RUN venv/bin/pip install .

ENTRYPOINT ["venv/bin/python3", "-m", "trafficlight_adapter_appium"]
# Assume ARGS will be always be passed like this --appium-type $APPIUM_TYPE --user $USERNAME --pass $PASSWORD




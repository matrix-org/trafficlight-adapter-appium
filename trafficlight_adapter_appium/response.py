from typing import Dict, Any


class Response:
    def __init__(self, json: Dict[str, Any]):
        self.data = json

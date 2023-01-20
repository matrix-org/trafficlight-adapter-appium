from typing import Dict, Any


class Request:
    def __init__(self, json: Dict[str, Any]):
        self.action = json['action']
        self.data = json['data']

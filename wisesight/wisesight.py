from typing import Dict, List
import datetime
import requests

class Wisesight():
    base_url: str
    username: str
    password: str
    headers: Dict[str, str]
    expiration_date: datetime
    request_timeout: int

    def __init__(self,
                 base_url: str,
                 username: str,
                 password: str
                 ):
        super().__init__()
        self.username = username
        self.password = password
        self.base_url = base_url
        self.request_timeout = 3*60
        self.expiration_date = None
        print('bank')
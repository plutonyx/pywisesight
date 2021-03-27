from typing import Dict, List
import logging
import datetime
import requests
import jwt

logger = logging.getLogger(__name__)
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

    def _get_headers(self) -> Dict[str, str]:
        self.authenticate()
        return self.headers

    def authenticate(self) -> None:
        if self.expiration_date is None or self.expiration_date <= datetime.datetime.now():
            logger.error('[x] renew token ')
            url = f'{self.base_url}/generate-token'
            headers_connect = {'Content-type': 'application/json'}
            payload = {
                'username': self.username,
                'password': self.password
            }
            response = {}
            try:
                response = requests.post(
                    url=url, json=payload, headers=headers_connect, timeout=int(self.request_timeout))
            except requests.exceptions.Timeout:
                print('[x]_authenticate request timeout.')

            if response.ok:
                data = response.json()
                token = data.get('token', {})
                # Actually token contain a expiration but I lazy to manage the expiration i will assume expiration will have 12hrs life-time.
                token_data = jwt.decode(token, options={"verify_signature": False})
                self.headers = {
                    "content-type": "application/json",
                    "Authorization": f"Bearer {token}",
                }
                self.expiration_date = datetime.datetime.now() + datetime.timedelta(hours=12)

        else:
            logger.error('[x] use existing token ')
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

    def get_campaigns(self) -> List[Dict[str, str]]:
        campaigns = []
        url = f'{self.base_url}/api/v1/campaigns/list'
        headers = self._get_headers()
        try:
            response = requests.get(url=url, headers=headers, timeout=int(self.request_timeout))
            if response.ok:
                campaigns = response.json()
        except requests.exceptions.Timeout:
            logger.error('[x] get_campaigns timeout ')
        except Exception as e:
            logger.error(f'[x] get_campaigns {e}')
        return campaigns

    def get_campaign(self, campaign_id: str) -> List[Dict[str, str]]:
        campaigns = []
        url = f'{self.base_url}/api/v1/campaigns/{campaign_id}'
        headers = self._get_headers()
        try:
            response = requests.get(url=url, headers=headers, timeout=int(self.request_timeout))
            if response.ok:
                campaigns = response.json()
        except requests.exceptions.Timeout:
            logger.error('[x] get_campaign detail timeout ')
        except Exception as e:
            logger.error(f'[x] get_campaign detail {e}')
        return campaigns

    def get_campaign_categories(self, campaign_id: str) -> List[Dict[str, str]]:
        campaigns = []
        url = f'{self.base_url}/api/v1/campaigns/{campaign_id}/categories'
        headers = self._get_headers()
        try:
            response = requests.get(url=url, headers=headers, timeout=int(self.request_timeout))
            if response.ok:
                campaigns = response.json()
        except requests.exceptions.Timeout:
            logger.error('[x] get_campaign_categories timeout ')
        except Exception as e:
            logger.error(f'[x] get_campaign_categories {e}')
        return campaigns

    def get_campaign_keywords(self, campaign_id: str) -> List[Dict[str, str]]:
        campaigns = []
        url = f'{self.base_url}/api/v1/campaigns/{campaign_id}/keywords'
        headers = self._get_headers()
        try:
            response = requests.get(url=url, headers=headers, timeout=int(self.request_timeout))
            if response.ok:
                campaigns = response.json()
        except requests.exceptions.Timeout:
            logger.error('[x] get_campaign_keywords timeout ')
        except Exception as e:
            logger.error(f'[x] get_campaign_keywords {e}')
        return campaigns

    def campaign_summary(self, campaign_id: str, date_start: int, date_end: int, duration: str = 'day') -> List[Dict[str, str]]:
        campaigns = []
        url = f'{self.base_url}/api/v1/campaigns/{campaign_id}/summary'
        headers = self._get_headers()
        try:
            data = {
                'date_start': date_start,
                'date_end': date_end,
                'duration': duration,
            }
            response = requests.post(url=url, json=data, headers=headers, timeout=int(self.request_timeout))
            if response.ok:
                campaigns = response.json()
        except requests.exceptions.Timeout:
            logger.error('[x] campaign_summary timeout ')
        except Exception as e:
            logger.error(f'[x] campaign_summary {e}')
        return campaigns

    def campaign_influencers(self, campaign_id: str, date_start: int, date_end: int) -> List[Dict[str, str]]:
        campaigns = []
        url = f'{self.base_url}/api/v1/campaigns/{campaign_id}/influencers'
        headers = self._get_headers()
        try:
            data = {
                'date_start': date_start,
                'date_end': date_end,
            }
            response = requests.post(url=url, json=data, headers=headers, timeout=int(self.request_timeout))
            if response.ok:
                campaigns = response.json()
        except requests.exceptions.Timeout:
            logger.error('[x] campaign_summary timeout ')
        except Exception as e:
            logger.error(f'[x] campaign_summary {e}')
        return campaigns

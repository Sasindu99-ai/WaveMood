from os import environ
from typing import Optional, Dict, Callable

import requests

from vvecon.qt.logger import logger
from vvecon.qt.models import Error
from vvecon.qt.util import Settings

__all__ = ['Controller']


class Controller:
    base: str = environ.get('API_URL', 'http://127.0.0.1:8000')
    api: str = NotImplemented
    refreshUrl: str = f'{base}/api/v1/auth/token/refresh'

    def generateUrl(self, endpoint: str) -> str:
        return f'{self.base}/{self.api}{endpoint}'

    @staticmethod
    def returnError(res):
        if res.headers.get('Content-Type') == 'application/json':
            logger.error(f'{res.status_code}: {res.json()}')
            return Error(status_code=res.status_code, error=res.json())
        else:
            logger.error(f'{res.status_code}: {res.text}')
            return Error(status_code=res.status_code, error=dict(detail=res.text))

    @staticmethod
    def returnJson(res):
        if res.headers.get('Content-Type') == 'application/json':
            return res.json()
        else:
            logger.error(f'{res.status_code}: {res.text}')
            return Error(status_code=res.status_code, error=dict(detail=res.text))

    def _retryLogin(self, method: Callable, endpoint: str, params: Optional[Dict] = None, data: Optional[Dict] = None):
        params = params or {}
        data = data or {}
        try:
            response = requests.post(
                self.refreshUrl, json={'refresh': Settings.get('REFRESH_TOKEN', '')}, timeout=10
            )
            if response.status_code != 200:
                return Error(status_code=response.status_code, error=dict(
                    detail=response.json() if response.headers.get(
                        'Content-Type') == 'application/json' else response.text))
            jsonData = response.json()
            Settings.set('ACCESS_TOKEN', jsonData.get('access'))
            return method(endpoint, params=params, data=data, authorized=True, retry=False)
        except Exception as e:
            logger.error(f'Refresh URL failed {e}')
            return Error(status_code=500, error=dict(detail='Refresh URL failed')), 500

    def request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None,
                authorized: bool = False, retry: bool = True):
        params = params or {}
        data = data or {}
        try:
            url = self.generateUrl(endpoint)
            headers = {'Content-Type': 'application/json'}
            if authorized:
                headers['Authorization'] = f"Bearer {Settings.get('ACCESS_TOKEN', '')}"

            logger.debug(f'{method} {url} {data}')
            logger.info(f'{method} {url}')
            response = requests.request(
                method=method, url=url, json=data, params=params, headers=headers, timeout=10, verify=False
            )
            logger.debug(f'{method} {url} {response.status_code}')
            logger.info(f'{method} {url} {response.status_code}')
            if response.status_code in (400, 401, 403) and retry and authorized:
                return self._retryLogin(
                    lambda ep, **kwargs: self.request(method, ep, **kwargs), endpoint, params=params, data=data
                )
            elif response.status_code in range(200, 300):
                return self.returnJson(response), response.status_code
            return self.returnError(response), response.status_code
        except requests.exceptions.ConnectionError:
            logger.error('Connection Error')
            return Error(status_code=503, error=dict(detail='Connection Error')), 503
        except requests.exceptions.Timeout:
            logger.error('Request Timeout')
            return Error(status_code=504, error=dict(detail='Request Timeout')), 504

    def post(self, endpoint: str, data: Optional[Dict] = None, **kwargs):
        return self.request('POST', endpoint, data=data, **kwargs)

    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs):
        return self.request('GET', endpoint, params=params, **kwargs)

    def put(self, endpoint: str, data: Optional[Dict] = None, **kwargs):
        return self.request('PUT', endpoint, data=data, **kwargs)

    def delete(self, endpoint: str, data: Optional[Dict] = None, **kwargs):
        return self.request('DELETE', endpoint, data=data, **kwargs)

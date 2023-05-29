from flights.utils import logger
from flights.config.settings import s

import requests

from typing import Optional

log = logger.create(__name__)


class BaseApi:
    def __init__(self, url: str, headers: Optional[dict] = None):
        self.url = url
        self.headers = headers or {}

    # def get(self, params: Optional[dict] = None) -> requests.Response or None:
    #     response = None
    #     for _ in range(s.Api.NUMBER_OF_TRIES):
    #         try:
    #             response = requests.get(self.url, headers=self.headers, params=params, timeout=s.Api.TIMEOUT)
    #             response.raise_for_status()
    #         except requests.exceptions.ConnectionError as e:
    #             log.error(f'ConnectionError: {e}')
    #         except requests.exceptions.Timeout as e:
    #             log.error(f'Timeout after {s.Api.TIMEOUT} seconds: {e}')
    #         except requests.exceptions.HTTPError as e:
    #             log.error(f'HTTPError for {e.response.request.method}: {e}')
    #             log.error(f'Response: {e.response.text}')
    #             log.error(f'Response headers: {e.response.headers}')
    #         if response and response.status_code == 200:
    #             log.debug(response.json())
    #             return response.json()
    #     log.critical(f'Failed to GET 200 status after {s.Api.NUMBER_OF_TRIES} tries. Url: {self.url} Params: {params}')
    #     if response:
    #         log.critical(f'Status code {response.status_code}, response text:\n{response.text}')
    #     return None

    def _make_request(self, method: str, params: Optional[dict] = None) -> Optional[requests.Response]:
        try:
            response = requests.request(method, self.url, params=params, headers=self.headers, timeout=s.Api.TIMEOUT)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as error:
            self._log_error(error)
            return None

    def _log_error(self, error: requests.exceptions.RequestException):
        request = error.request
        response = error.response
        log.error(f'Error for {request.method} {request.url}: {error}')
        if response is not None:
            log.error(f'Status code {response.status_code}, response text:\n{response.text}')

    def get(self, params: Optional[dict] = None) -> Optional[dict]:
        for _ in range(s.Api.NUMBER_OF_TRIES):
            response = self._make_request('GET', params)
            if response is not None and response.status_code == 200:
                log.debug(response.json())
                return response.json()
        log.critical(f'Failed to GET 200 status after {s.Api.NUMBER_OF_TRIES} tries. Url: {self.url} Params: {params}')
        if response:
            log.critical(f'Status code {response.status_code}, response text:\n{response.text}')
        return None

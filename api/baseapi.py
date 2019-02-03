import aiohttp
from typing import Dict, Optional

from ..api.method import Method


class BaseAPI(object):
    """ Base API class for interacting with the Streamlabs AI"""

    BASE_API_URL = "https://streamlabs.com/api/v1.0"
    API_URL = ""

    def __init__(self, access_token: str):
        self._access_token = access_token

    def _build_api_url(self, append_path: str = None):
        """
        Builds the API URL from the Subclass value.
        :param append_path: Path to append to the API url.
        :return: Built Streamlabs API endpoint URL.
        """
        append_path = "" if append_path is None else append_path
        return f"{self.BASE_API_URL}{self.API_URL}{append_path}"

    async def _raw_request(
        self, method: Method, params: Optional[Dict] = None, data: Optional[Dict] = None, append_path: str = None
    ) -> Dict:
        """
        Raw POST request to the Streamlabs API.
        :param method: HTTP Method (GET, POST, etc)
        :param params: Params will be included in the query string.
        :param data: Data will be included in POST requests.
        :param append_path: Path to append to the API URL
        :return: JSON response from the API
        """
        async with aiohttp.ClientSession() as session:
            if method == Method.GET:
                async with session.get(url=self._build_api_url(append_path=append_path), params=params) as resp:
                    return await resp.json()
            elif method == Method.POST:
                async with session.post(url=self._build_api_url(append_path=append_path), data=data) as resp:
                    return await resp.json()

    async def _request(
        self, method: Method, params: Optional[Dict] = None, data: Optional[Dict] = None, append_path: str = None
    ) -> Dict:
        """
        Handles adding the API access token to the Request parameters/data.
        :param method: HTTP Method (GET, POST, etc)
        :param params: Params will be included in the query string.
        :param data: Data will be included in POST requests.
        :param append_path: Path to append to the API URL
        :return: JSON response from the API
        """
        params = {} if params is None else params
        params["access_token"] = self._access_token

        data = {} if data is None else data
        data["access_token"] = self._access_token
        return await self._raw_request(method=method, params=params, data=data, append_path=append_path)

    async def _post(self, data: Dict = None, append_path: str = None) -> Dict:
        """
        POST to the API URL.

        :param data: Data to send in the POST request. Will have the access token added to the data.
        :param append_path: Path to append to the API URL
        :return: JSON response from the API
        """
        return await self._request(method=Method.POST, data=data, append_path=append_path)

    async def _get(self, params: Optional[Dict] = None, append_path: str = None) -> Dict:
        """

        :param params: Params to append as query string to the GET request. Access token will be added.
        :param append_path: Path to append to the API URL
        :return: JSON response from the API
        """
        params = {} if params is None else params
        return await self._request(method=Method.GET, params=params, append_path=append_path)

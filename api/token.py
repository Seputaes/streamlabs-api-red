from typing import Union, Dict

import aiohttp

from ..seplib.utils import Result
from . import BaseAPI


class TokenAPI(BaseAPI):
    """
    Representation of the Streamlabs Token API.
    API Reference: https://dev.streamlabs.com/v1.0/reference#token-1
    """

    API_URL = "/token"

    @staticmethod
    def build_token_url():
        return f"{BaseAPI.BASE_API_URL}{TokenAPI.API_URL}"

    @staticmethod
    async def get_access_token(
        client_id: str, client_secret: str, redirect_uri: str, auth_code: str
    ) -> Union[Result, Dict[str, str]]:
        """
        Retrieve the access token and refresh_token based on the authorization code
        provided when the user authorized the the Streamlabs app to their their account.

        :param client_id: Client ID of the Streamlabs App.
        :param client_secret: Client Secret of the Streamlabs App.
        :param redirect_uri: Redirect URI of the Streamlabs App.
        :param auth_code: Auth code generated after the user has authorized the Streamlabs app.
        :return: Raw JSON response from the Token API
        """
        auth_data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=TokenAPI.build_token_url(), data=auth_data) as resp:
                if resp.status != 200:
                    reply = await resp.json()
                    return Result(
                        success=False, error=f"Streamlabs Token API request failed. Error: {reply}", value=False
                    )
                return await resp.json()

    @staticmethod
    async def refresh_access_token(
        client_id: str, client_secret: str, redirect_uri: str, refresh_token: str
    ) -> Union[Result, Dict[str, str]]:
        """
            Refreshes the access token and refresh_token based on the refresh_token
            if it has expired.

            According to Streamlabs docs, this will never expire, but you never know...
            https://dev.streamlabs.com/docs/oauth-2#section-do-not-refresh-tokens

            :param client_id: Client ID of the Streamlabs App.
            :param client_secret: Client Secret of the Streamlabs App.
            :param redirect_uri: Redirect URI of the Streamlabs App.
            :param refresh_token: Refresh token provided in the previous authentication.
            :return: Raw JSON response from the Token API
            """
        auth_data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
            "redirect_uri": redirect_uri,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=TokenAPI.build_token_url(), data=auth_data) as resp:
                if resp.status != 200:
                    reply = await resp.json()
                    return Result(
                        success=False, error=f"Streamlabs Token API request failed. Error: {reply}", value=False
                    )
                return await resp.json()

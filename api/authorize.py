from urllib.parse import urlencode

from . import BaseAPI


class AuthorizeAPI(BaseAPI):
    """
    Representation of the Streamlabs Authorize API
    API Representation: https://dev.streamlabs.com/v1.0/reference#authorize
    """

    API_URL = "/authorize"

    SL_API_SCOPE = "alerts.create donations.read donations.create alerts.write"  # TODO: Figure out actual scopes

    @staticmethod
    def build_auth_url(client_id: str, redirect_uri: str) -> str:
        """
        Builds the Streamlabs app authorization URL that the user will need to go to to authorize the app.
        :param client_id: Client ID of the Streamlabs App.
        :param redirect_uri: Redirect URI of the Streamlabs App
        :return: Built Streamlabs authorization URL that the user will need to go to to authorize the app.
        """
        url = f"{BaseAPI.BASE_API_URL}{AuthorizeAPI.API_URL}"
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": AuthorizeAPI.SL_API_SCOPE,
            "response_type": "code",
        }
        query_string = urlencode(params)
        return f"{url}?{query_string}"

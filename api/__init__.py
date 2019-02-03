from .baseapi import BaseAPI

### DO NOT MOVE BASEAPI THIS BELOW THIS LINE
from .alerts import AlertsAPI
from .authorize import AuthorizeAPI
from .donations import DonationsAPI
from .token import TokenAPI


class SLAPI(object):
    """
    Entry point for storing singleton instances of a particuarl StreamLabs API with access token.
    """

    def __init__(self, access_token: str):
        self.__access_token = access_token

    @property
    def alerts(self) -> AlertsAPI:
        try:
            return self.__alerts
        except AttributeError:
            self.__alerts = AlertsAPI(access_token=self.__access_token)
        return self.__alerts

    @property
    def donations(self) -> DonationsAPI:
        try:
            return self.__donations
        except AttributeError:
            self.__donations = DonationsAPI(access_token=self.__access_token)
        return self.__donations

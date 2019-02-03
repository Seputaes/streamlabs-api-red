from decimal import Decimal
from typing import Dict, Optional, Union, List

from ..seplib.utils import Result
from . import BaseAPI


class DonationsAPI(BaseAPI):
    """
    Representation of the Streamlabs Donations API
    API Reference: https://dev.streamlabs.com/v1.0/reference#donations
    """

    API_URL = "/donations"

    async def get_donations(
        self,
        limit: Optional[int] = None,
        before: Optional[int] = None,
        after: Optional[int] = None,
        currency: Optional[str] = None,
        verified: Optional[bool] = None,
    ) -> Dict:
        """
        Gets a list of Streamlabs donations on the user's Streamlabs Account.

        :param limit: Maximum number of results to get.
        :param before: Limits the donations to those before a certain donation ID.
        :param after: Limits the donations to those after a certain donation ID.
        :param currency: Limits the donations to specified currency code: https://dev.streamlabs.com/docs/currency-codes
        :param verified: Boolean to indicate whether you only want verified donations.
        :return: List of Streamlabs Donations.
        """
        params = {}
        args = {
            "limit": limit,
            "before": before,
            "after": after,
            "currency": currency,
            "verified": int(verified) if verified is not None else None,
        }
        params.update((k, v) for k, v in args.items() if v is not None)
        json_resp = await self._get(params=params)
        return json_resp

    async def create_donation(
        self,
        name: str,
        identifier: str,
        amount: Union[int, float, Decimal],
        currency: str,
        message: str = None,
        created_at: str = None,
        skip_alert: bool = False,
    ) -> Union[Result, int]:
        # TODO: Input Validation
        """
        Creates a new Streamlabs donation.

        :param name: The name of the donor. Has to be between 2-25 chars and can only be alphanumeric + underscores.
        :param identifier: An identifier for this donor, which is used to group donations with the same donor.
                           For example, if you create more than one donation with the same identifier,
                           they will be grouped together as if they came from the same donor.
                           Typically this is best suited as an email address, or a unique hash.
        :param amount: The amount of this donation.
        :param currency: The 3 letter currency code for this donation: https://dev.streamlabs.com/docs/currency-codes
        :param message: The message from the donor. Must be < 255 characters
        :param created_at: A timestamp that identifies when this donation was made. Defaults to Now.
        :param skip_alert:Boolean to indicate whether the alert should be skipped when the donation is posted.
        :return: Result, if with error if result was not successful
        """

        if isinstance(amount, float):
            amount = Decimal.from_float(amount)
        elif isinstance(amount, int):
            amount = Decimal(str(amount))

        amount = round(amount, 2)

        data = {"name": name, "identifier": identifier, "amount": amount, "currency": currency}
        args = {"created_at": created_at, "message": message, "skip_alert": "yes" if skip_alert is True else None}
        data.update((k, v) for k, v in args.items() if v is not None)
        json_resp = await self._post(data=data)
        result = Result.get_result(check=lambda: "donation_id" in json_resp, error=json_resp.get("error"))
        if not result.success:
            return result
        return json_resp.get("donation_id")

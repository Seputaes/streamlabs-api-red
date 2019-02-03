from ..seplib.utils import Result
from . import BaseAPI


class AlertsAPI(BaseAPI):
    """
    Representation of the Streamlabs Alerts API
    API Reference: https://dev.streamlabs.com/v1.0/reference#alerts
    """

    API_URL = "/alerts"

    def __init__(self, access_token: str):
        super(AlertsAPI, self).__init__(access_token=access_token)

    async def create_alert(
        self,
        type_: str,
        image_href: str = None,
        sound_href: str = None,
        message: str = None,
        user_message: str = None,
        duration: str = None,
        special_text_color: str = None,
    ) -> Result:
        """
        Creates a Streamlabs alert.

        :param type_: Type of the alert. Can be one of [follow, subscription, host, donation].
        :param image_href: URL of an image to include on the alert.
        :param sound_href: URL of a sound to play with the alert.
        :param message: Primary message to display on the alert. Special text can be enclosed in single asterisks.
        :param user_message: User's message to include on the alert.
                             This will only work for donations and subscriptions.
        :param duration: Duration in milliseconds that the alert should display.
        :param special_text_color: CSS color value of the special text (eg #FF0000 for red)
        :return: Result, if with error if result was not successful
        """
        # TODO: Add validation

        data = {"type": type_}

        args = {
            "image_href": image_href,
            "sound_href": sound_href,
            "message": message,
            "user_message": user_message,
            "duration": duration,
            "special_text_color": special_text_color,
        }
        data.update((k, v) for k, v in args.items() if v is not None)

        json_resp = await self._post(data=data)
        return Result.get_result(check=lambda: "error" not in json_resp, error=json_resp.get("error"))

    async def skip_alert(self) -> Result:
        """
        Skips the next unapproved alert.
        :return: Result, if with error if result was not successful
        """
        json_resp = await self._post(data=None, append_path="/skip")
        return Result.get_result(check=lambda: "error" not in json_resp, error=json_resp.get("error"))

    async def mute_volume(self) -> Result:
        """
        Mutes the alert volume until unmute_volume is called.
        :return: Result, if with error if result was not successful
        """
        json_resp = await self._post(data=None, append_path="/mute_volume")
        return Result.get_result(check=lambda: "error" not in json_resp, error=json_resp.get("error"))

    async def unmute_volume(self) -> Result:
        """
        Unmuted the alert volume.
        :return: Result, if with error if result was not successful
        """
        json_resp = await self._post(data=None, append_path="/unmute_volume")
        return Result.get_result(check=lambda: "error" not in json_resp, error=json_resp.get("error"))

    async def pause_queue(self) -> Result:
        """
        Pauses all future alerts until unpuase_queue is called.
        :return: Result, if with error if result was not successful
        """
        json_resp = await self._post(data=None, append_path="/pause_queue")
        return Result.get_result(check=lambda: "error" not in json_resp, error=json_resp.get("error"))

    async def unpause_queue(self) -> Result:
        """
        Unpauses the alert queue.
        :return: Result, if with error if result was not successful
        """
        json_resp = await self._post(data=None, append_path="/unpause_queue")
        return Result.get_result(check=lambda: "error" not in json_resp, error=json_resp.get("error"))

    async def send_test_alert(self, type_: str, platform: str = None) -> Result:
        """
        Sends a test alert of the specified type.
        :param type_: Type of the test alert. Can be one of [follow, subscription, donation, host, raid, bits]
        :param platform: (optional) Platform of the alert (Twitch or Youtube)
        :return: Result, if with error if result was not successful
        """
        data = {"type": type_}
        if platform is not None:
            data["platform"] = platform

        json_resp = await self._post(data=data, append_path="/send_test_alert")
        return Result.get_result(check=lambda: "error" not in json_resp, error=json_resp.get("error"))

    async def show_video(self) -> Result:
        """
        Toggles a Stramlabs Media Share video to ON in the Alert Box.
        :return: Result, if with error if result was not successful
        """
        json_resp = await self._post(data=None, append_path="/show_video")
        return Result.get_result(check=lambda: "error" not in json_resp, error=json_resp.get("error"))

    async def hide_video(self) -> Result:
        """
        Hides the Streamlabs Media Share video in the Alert Box.
        :return: Result, if with error if result was not successful
        """
        json_resp = await self._post(data=None, append_path="/hide_video")
        return Result.get_result(check=lambda: "error" not in json_resp, error=json_resp.get("error"))

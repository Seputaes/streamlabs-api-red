import logging
from typing import Dict, Optional, Union

import discord

from redbot.core.commands import Context
from ..api import TokenAPI
from ..api import AuthorizeAPI
from ..replies import StreamlabsReply
from ..seplib.replies import ErrorReply, InteractiveActions, SuccessReply
from ..seplib.utils import ContextWrapper, HexColor, Result
from ..utils import GetReplyPredicate

LOGGER = logging.getLogger("red.streamlabsapi.StreamlabsConfig")
LOGGER.setLevel(logging.INFO)


class StreamlabsConfig(object):
    @staticmethod
    async def __config_welcome(ctx: Context, timeout: int) -> bool:
        welcome_title = "Streamlabs Cog Configuration [Part 1 of 6] - Streamlabs Application Setup"
        welcome_message = (
            f"{ctx.author.mention} Welcome to Streamlabs configuration!\n\n"
            f"**WARNING:** Make sure you are running this configuration in a SECURE/PRIVATE CHANNEL!\n\n"
            f"The operations you will be performing will require telling me secret keys and codes. "
            f"I will do my best to clean them up, but there's still risk of them being exposed.\n\n"
            f"Again, execute this configuration in a **SECURE/PRIVATE CHANNEL**. This will be the last warning.\n\n"
        )
        welcome_embed = StreamlabsReply(message=welcome_message, title=welcome_title).build()
        await ctx.send(content=ctx.author.mention, embed=welcome_embed)

        # confirmation of private channel

        confirm_title = "Streamlabs Cog Configuration - Private Channel Confirmation"
        confirm_message = "Please confirm that this channel is private"
        confirm_embed = StreamlabsReply(message=confirm_message, title=confirm_title, color=HexColor.warning()).build()

        confirm_response = await InteractiveActions.yes_or_no_action(ctx=ctx, embed=confirm_embed, timeout=timeout)
        return confirm_response

    @staticmethod
    async def __config_get_response(ctx: Context, timeout: int, title: str, message: str):
        reply = StreamlabsReply(message=message, title=title)
        await reply.send(ctx)

        predicate_check = GetReplyPredicate.string_reply(ctx=ctx, user=ctx.author)
        await ctx.bot.wait_for("message", check=predicate_check, timeout=timeout)
        response_text = predicate_check.result.clean_content
        await predicate_check.result.delete()
        return response_text

    @staticmethod
    async def __config_client_id(ctx: Context, timeout: int) -> str:
        title = "Streamlabs Cog Configuration [Part 2 of 6] - Client ID"
        message = "Please tell me the **Client ID** of your Streamlabs App"
        return await StreamlabsConfig.__config_get_response(ctx=ctx, timeout=timeout, message=message, title=title)

    @staticmethod
    async def __config_client_secret(ctx: Context, timeout: int) -> str:
        title = "Streamlabs Cog Configuration [Part 3 of 6] - Client Secret"
        message = "Please tell me the **Client Secret** of your Streamlabs App"
        return await StreamlabsConfig.__config_get_response(ctx=ctx, timeout=timeout, message=message, title=title)

    @staticmethod
    async def __config_redirect_uri(ctx: Context, timeout: int) -> str:
        title = "Streamlabs Cog Configuration [Part 4 of 6] - Redirect URI"
        message = "Please tell me the **Redirect URI:** of your Streamlabs App"
        return await StreamlabsConfig.__config_get_response(ctx=ctx, timeout=timeout, message=message, title=title)

    @staticmethod
    async def __config_auth_code(ctx: Context, timeout: int = 60) -> str:
        title = "Streamlabs Cog Configuration [Part 6 of 6] - Enter Authorization Code"
        message = (
            "Great! In the address of the page you were redirected to (it probably won't load), "
            "tell me the **code** parameter.\n\n"
            "__**For example**__\n"
            "**Address:** `https://localhost/sl_auth?code=HrHiYOCo8N3xgL9tkk`\n"
            "**Your Code:** `HrHiYOCo8N3xgL9tkk`\n\n"
            "The code will likely be about 40 characters long."
        )
        return await StreamlabsConfig.__config_get_response(ctx=ctx, timeout=timeout, message=message, title=title)

    @staticmethod
    async def __config_give_auth_url(ctx: Context, auth_url: str):
        title = "Streamlabs Cog Configuration [Part 5 of 6] - App Authorization"
        message = (
            f"You'll now need to **authorize** your Streamlabs App to interact with you Streamlabs account.\n\n"
            f"Please go to [this URL]({auth_url}) and authorize the App.\n\n"
        )
        next_step_message = (
            f"Once you've authorized the app and have been redirected (likely to a blank page), "
            f"please continue with command `{ctx.prefix}streamlabs continue`"
        )
        embed = StreamlabsReply(message=message, title=title).build()
        embed.add_field(name="Next Step", inline=False, value=next_step_message)
        return await ctx.send(content=ctx.author.mention, embed=embed)

    @staticmethod
    async def config_guide(ctx: Context) -> discord.Message:
        message = (
            "Here's an overview of steps you need to take to get Streamlabs up and running:\n\n"
            "1. Log into your Streamlabs account, and follow the instructions to Register a new App here: https://streamlabs.com/dashboard#/apisettings\n"
            "2. While registering the app, be sure to set the the **Redirect URI** to either a domain that you actully own/control, or simply `https://localhost/sl_auth` for security purposes.\n"
            "3. After the application is created, you will be shown the **Client ID** and **Client Secret**. You will need this, along with the **Redirect URI** in the next steps.\n"
            f"4. You will supply your Discord Bot with these 3 items by running the `{ctx.prefix}streamlabs config` command.\n"
            f"5. After supplying the information, the bot will direct you to navigate to a Streamlabs webpage to grant the new app you created access to your Streamlabs account\n"
            "6. After authorizing the app, you will be redirected to the **Redirect URI** specified above. Since this is localhost, the page won't load.\n"
            "7. In the address of that page, you should see a **code** parameter. Copy that for the next step.\n"
            f"8. In Discord, use the command `{ctx.prefix}streamlabs continue` to proceed. This step will ask for the code you copied in the previous step.\n"
            "9. Success! At this point, the Discord bot should be able to configure the rest, and will tell you if it was a success or if anything went wrong."
        )
        embed = StreamlabsReply(message=message, title="Streamlabs Configuration Guide")
        return await embed.send(ctx)

    @staticmethod
    async def start_config(ctx: Context, timeout: int = 60) -> Optional[Dict[str, str]]:
        """
        Begin setting up Streamlabs configuration. This will proceed through a series of steps to instruct the user
        how to configure the StreamLabs API.

        It is part of a two-command process. The second of which is "continue_config".

        How you store the auth configuration returned from this method is up to you (per user, per server, global, etc).

        The auth configuration returned from this method is partical. You will need to update the dict returned
        from this method with the one returned from "continue_config".

        Data returned from this method:
        {
            "client_id": str,
            "client_secret": str,
            "redirect_uri": str,
        }

        :param ctx: Context in which the command was issued.
        :param timeout: Amount of time between each config step that the user will have to provide answers.
        :return: Auth configuration consisting of client_id, client_secret, and redirect_uri.
        """

        auth_data = {}

        # CONFIG INTRO MESSAGE
        confirmed = await StreamlabsConfig.__config_welcome(ctx=ctx, timeout=timeout)
        if not confirmed:
            await ContextWrapper(ctx).cross()
            return

        # CLIENT ID
        client_id = await StreamlabsConfig.__config_client_id(ctx=ctx, timeout=timeout)
        if not client_id:
            await ContextWrapper(ctx).cross()
            return
        auth_data["client_id"] = client_id

        # CLIENT SECRET
        client_secret = await StreamlabsConfig.__config_client_secret(ctx=ctx, timeout=timeout)
        if not client_secret:
            await ContextWrapper(ctx).cross()
            return
        auth_data["client_secret"] = client_secret

        # REDIRECT URI
        redirect_uri = await StreamlabsConfig.__config_redirect_uri(ctx=ctx, timeout=timeout)
        if not redirect_uri:
            await ContextWrapper(ctx).cross()
            return
        auth_data["redirect_uri"] = redirect_uri

        # ASK USER TO APPROVE APP
        auth_url = AuthorizeAPI.build_auth_url(client_id=client_id, redirect_uri=redirect_uri)
        await StreamlabsConfig.__config_give_auth_url(ctx=ctx, auth_url=auth_url)
        return auth_data

    @staticmethod
    async def continue_config(
        ctx: Context, auth_data: Dict[str, str], timeout: int = 60
    ) -> Optional[Dict[str, Union[str, int]]]:
        """
        Continues the Streamlabs configuration. This is the second of 2 commands, the first one is start_config.

        This will update the auth_data data which you received from the start_config method.

        Data added by this method:
        {
            "access_token": str,
            "expires_in": int,
            "refresh_token": str,
        }

        Final Result:
        {
            "client_id": str,
            "client_secret": str,
            "redirect_uri": str,
            "access_token": str,
            "expires_in": int,
            "refresh_token": str,
        }

        :param ctx: Context the continue command was called in.
        :param auth_data: auth_data received from the start_config method,
                          consisting of client_id, client_secret, and redirect_uri
        :param timeout: Amount of time the user will have to enter the auth code.
        :return: Updates/Returns the auth_data with the fully created authorization values from the
                 Streamlabs Token API. You can then store this accordingly.
        """

        if not all(k in auth_data for k in ["client_id", "client_secret", "redirect_uri"]):
            message = (
                f"Configuration for this guild is not started or complete. P"
                f"lease run `{ctx.prefix}streamlabs config` first."
            )
            return await ErrorReply(message=message).send(ctx)

        auth_code = await StreamlabsConfig.__config_auth_code(ctx=ctx, timeout=timeout)
        if not auth_code:
            await ContextWrapper(ctx).cross()
            return

        result = await TokenAPI.get_access_token(
            client_id=auth_data.get("client_id"),
            client_secret=auth_data.get("client_secret"),
            redirect_uri=auth_data.get("redirect_uri"),
            auth_code=auth_code,
        )
        if isinstance(result, Result):
            return await ErrorReply(message=result.error).send(ctx)
        await SuccessReply(message="Success!").send(ctx)
        auth_data.update(result)
        return auth_data

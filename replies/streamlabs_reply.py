import discord
from discord import Color

from ..seplib.replies import EmbedReply
from ..seplib.utils import HexColor


class StreamlabsReply(EmbedReply):
    def __init__(self, message: str, title: str, color: Color = HexColor(0x31C3A2)):
        super(StreamlabsReply, self).__init__(message=message, emoji=None, color=color)
        self.TITLE = title

    def build(self):
        embed = discord.Embed(description=self.build_message(), color=self.color, title=self.TITLE)
        embed.set_author(name="Streamlabs Cog by Seputaes", icon_url="https://streamlabs.com/favicon.ico")
        return embed

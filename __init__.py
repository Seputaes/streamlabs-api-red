from redbot.core.bot import Red

from .streamlabsapi import StreamlabsAPI


def setup(bot: Red):
    bot.add_cog(StreamlabsAPI(bot=bot))

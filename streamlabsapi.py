from redbot.core import commands
from redbot.core.bot import Red


class StreamlabsAPI(commands.Cog):
    def __init__(self, bot: Red):
        super(StreamlabsAPI, self).__init__()
        self.bot = bot


# this is a shared library cog and has no functionality

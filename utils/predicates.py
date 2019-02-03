from typing import Optional

import discord

from redbot.core.commands import Context

from redbot.core.utils.predicates import MessagePredicate

__all__ = ["GetReplyPredicate"]


class GetReplyPredicate(MessagePredicate):
    """
    Collection of message predicates which return the actual user message which triggered the predicate.
    """

    @classmethod
    def string_reply(
        cls, ctx: Optional[Context] = None, channel: Optional[discord.TextChannel] = None, user: [discord.User] = None
    ):
        """
        Predicate which returns the user message which triggered the predicate if the response is any string > 0.
        :param ctx: Context in which to restrict the response.
        :param channel: Channel in which to restrict the response.
        :param user: User for which to restrict the response
        :return: Returns the predicate, with actual message that triggered the predicate in the result if true.
        """

        same_context = cls.same_context(ctx, channel, user)

        def predicate(self: MessagePredicate, m: discord.Message) -> bool:
            if not same_context(m):
                return False
            content = m.content.lower()
            if len(content) > 0:
                self.result = m
                return True
            return False

        return cls(predicate)

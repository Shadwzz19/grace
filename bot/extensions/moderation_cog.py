from typing import Optional
from bot import app
from logging import info
from discord import Member
from discord.ext.commands import Cog, has_permissions, hybrid_command, Context
from bot.helpers.log_helper import danger
from datetime import datetime


class ModerationCog(Cog, name="Moderation", description="Collection of administrative commands."):
    def __init__(self, bot):
        self.bot = bot

    @property
    def moderation_channel(self):
        return self.bot.get_channel_by_name("moderation_logs")

    @hybrid_command(name='purge', help="Deletes n amount of messages.")
    @has_permissions(manage_messages=True)
    async def purge(self, ctx: Context, limit: int, reason: Optional[str] = "No reason given") -> None:
        """Purge a specified number of messages from the channel.
        
        :param ctx: The context in which the command was called.
        :type ctx: Context
        :param limit: The number of messages to be purged.
        :type limit: int
        :param reason: The reason for the purge
        :type reason: Optional[str]
        """
        await ctx.defer()

        log = danger("PURGE", f"{limit} message(s) purged by {ctx.author.mention} in {ctx.channel.mention}")
        log.add_field("Reason", reason)

        await ctx.channel.purge(limit=int(limit) + 1, bulk=True, reason=reason)
        await log.send(self.moderation_channel or ctx.channel)

    @Cog.listener()
    async def on_member_join(self, member) -> None:
        """A listener function that checks if a member's account age meets the minimum required age to join the server. 
        If it doesn't, the member is kicked.

        :param member: The member who has just joined the server.
        :type member: discord.Member
        """
        minimum_account_age = app.config.get("moderation", "minimum_account_age")
        account_age_in_days = (datetime.now().replace(tzinfo=None) - member.created_at.replace(tzinfo=None)).days

        if account_age_in_days <= minimum_account_age:
            info(f"{member} kicked due to account age restriction!")

            log = danger("KICK", f"{member} has been kicked.")
            log.add_field("Reason: ", "Automatically kicked due to account age restriction")

            await member.send(f"Your account needs to be {minimum_account_age} days old or more to join the server.")
            await member.guild.kick(user=member, reason="Account age restriction")

            if self.moderation_channel:
                await log.send(self.moderation_channel)


async def setup(bot):
    await bot.add_cog(ModerationCog(bot))

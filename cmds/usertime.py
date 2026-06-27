# pyright: reportInvalidTypeForm=false

import discord
from discord.ext import commands
from datetime import datetime
import pytz
from addons.ut_atlas import db
from addons.ut_helper import timezone_autocomplete

# Access the MongoDB collection
user_timezones = db["timezones"]


class Usertime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _get_time_logic(self, ctx, user: discord.User):
        tz_info = user_timezones.find_one({"userid": str(user.id)})
        if not tz_info:
            if ctx.author.id != user.id:
                extra = "\nAsk them to set their timezone with `/add`"
            else:
                extra = "\nTake the moment to set it with `/add`!"
            await ctx.respond(
                f"{user.mention}'s timezone is not set." + extra,
                ephemeral=True
            )
            return
        try:
            now = datetime.now(pytz.timezone(tz_info["timezone"]))
            formatted_time = now.strftime('%A, %B %d, %Y at %I:%M %p %Z')
            await ctx.respond(
                f"🕒 {user.mention}'s current time:\n**{formatted_time}**",
                ephemeral=True
            )
        except Exception as e:
            await ctx.respond("Error getting time.", ephemeral=True)
            raise

    async def _set_timezone_logic(self, ctx, user: discord.User, timezone: str):
        if ctx.author.id == user.id or ctx.author.id in self.bot.owner_ids:
            try:
                pytz.timezone(timezone)
            except pytz.UnknownTimeZoneError:
                await ctx.respond(
                    "❌ Invalid timezone.\nPlease provide a [valid timezone](https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568) (e.g., `America/Bogota`).",
                    ephemeral=True
                )
                return

            existing_entry = user_timezones.find_one({"userid": str(user.id)})

            if existing_entry:
                existing_tz = existing_entry["timezone"]
                user_timezones.update_one(
                    {"userid": str(user.id)},
                    {"$set": {"timezone": timezone}}
                )
                await ctx.respond(
                    f"✅ {user.mention}'s timezone has been **updated**.\nBefore: `{existing_tz}`\nAfter: `{timezone}`.",
                    ephemeral=True
                )
            else:
                user_timezones.insert_one(
                    {"userid": str(user.id), "timezone": timezone})
                await ctx.respond(
                    f"✅ {user.mention}'s timezone has been **set** to `{timezone}`.",
                    ephemeral=True
                )
        else:
            await ctx.respond("❌ You can't update other people's timezones.",
                              ephemeral=True)

    @commands.user_command(
        name="Check the user's time",
        integration_types=[discord.IntegrationType.user_install]
    )
    async def get_time_context(self, ctx, user: discord.User):
        await self._get_time_logic(ctx, user)

    @commands.slash_command(
        name="time",
        description="Get the current time for a user based on their set timezone.",
        integration_types=[discord.IntegrationType.user_install]
    )
    async def get_time_slash(self, ctx, user: discord.User):
        await self._get_time_logic(ctx, user)

    @commands.slash_command(
        name="add",
        description="Set or update another user's timezone (e.g., America/New_York).",
        integration_types=[discord.IntegrationType.user_install]
    )
    async def addtz(self, ctx,
                    timezone: discord.Option(
                        str,
                        description="Timezone to set",
                        autocomplete=timezone_autocomplete
                    ),
                    user: discord.User = None
                    ):
        if user is None:
            user = ctx.author
        await self._set_timezone_logic(ctx, user, timezone)

    @commands.slash_command(
        name="remove",
        description="Remove a user's timezone from the database.",
        integration_types=[discord.IntegrationType.user_install]
    )
    async def remove_tz(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.author
        if ctx.author.id == user.id or ctx.author.id in self.bot.owner_ids:
            result = user_timezones.delete_one({"userid": str(user.id)})

            if result.deleted_count:
                await ctx.respond(
                    f"✅ Removed timezone for {user.mention}.",
                    ephemeral=True
                )
            else:
                await ctx.respond(
                    f"❌ {user.mention} doesn't have a timezone set.",
                    ephemeral=True
                )
        else:
            await ctx.respond("❌ You can't update other people's timezones.",
                              ephemeral=True)


def setup(bot):
    bot.add_cog(Usertime(bot))

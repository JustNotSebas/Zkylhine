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
        userid = str(user.id)
        tz_info = user_timezones.find_one({"userid": userid})

        if not tz_info:
            await ctx.respond(
                f"""{user.mention}'s timezone is not set.\nUse the command `/add` to set their timezone.""",
                ephemeral=True
            )
            return

        try:
            tz = pytz.timezone(tz_info["timezone"])
            now = datetime.now(tz)
            formatted_time = now.strftime('%A, %B %d, %Y at %I:%M %p %Z')

            await ctx.respond(
                f"🕒 {user.mention}'s current time:\n**{formatted_time}**",
                ephemeral=True
            )
        except Exception as e:
            await ctx.respond("Error getting time.", ephemeral=True)
            print(f"[Error getting time for {user.id}]: {e}")

    async def _set_timezone_logic(self, ctx, user: discord.User, timezone: str):
        userid = str(user.id)

        # Validate timezone
        try:
            pytz.timezone(timezone)
        except pytz.UnknownTimeZoneError:
            await ctx.respond(
                "❌ Invalid timezone. Please provide a valid timezone (e.g., `America/Bogota`).",
                ephemeral=True
            )
            return

        existing_entry = user_timezones.find_one({"userid": userid})

        if existing_entry:
            user_timezones.update_one(
                {"userid": userid},
                {"$set": {"timezone": timezone}}
            )
            await ctx.respond(
                f"✅ {user.mention}'s timezone has been **updated** to `{timezone}`.",
                ephemeral=True
            )
        else:
            user_timezones.insert_one({"userid": userid, "timezone": timezone})
            await ctx.respond(
                f"✅ {user.mention}'s timezone has been **set** to `{timezone}`.",
                ephemeral=True
            )

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
                    user: discord.User
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
        userid = str(user.id)
        result = user_timezones.delete_one({"userid": userid})

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


def setup(bot):
    bot.add_cog(Usertime(bot))

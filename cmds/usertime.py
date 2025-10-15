import discord
from discord.ext import commands
from datetime import datetime
import pytz
from database import db

# Access the MongoDB collection
user_timezones = db["timezones"]

class Usertime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # -----------------------
    # GLOBAL ERROR HANDLER
    # -----------------------
    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        """Handles command errors gracefully."""
        # 404: Unknown interaction (likely expired or duplicate)
        if isinstance(error, discord.NotFound):
            print(
                f"[{datetime.now()}] [404 Unknown Interaction]\n"
                f"- Author: {getattr(ctx.author, 'name', 'Unknown')} ({getattr(ctx.author, 'id', 'N/A')})\n"
                f"- Command: {getattr(ctx.command, 'qualified_name', 'Unknown')}\n"
                f"- Interaction ID: {getattr(ctx.interaction, 'id', 'N/A')}\n"
                f"- Guild: {getattr(ctx.guild, 'name', 'DM or Unknown')}\n"
            )
            return  # silently return to prevent further response attempts

        # Handle missing permissions, bad args, etc.
        elif isinstance(error, commands.MissingPermissions):
            await ctx.respond("You don't have permission to use this command.", ephemeral=True)

        elif isinstance(error, commands.BadArgument):
            await ctx.respond("Invalid argument provided. Please check your input.", ephemeral=True)

        else:
            # Unexpected errors → log full details
            print(
                f"[{datetime.now()}] [Command Error]\n"
                f"- Author: {getattr(ctx.author, 'name', 'Unknown')} ({getattr(ctx.author, 'id', 'N/A')})\n"
                f"- Command: {getattr(ctx.command, 'qualified_name', 'Unknown')}\n"
                f"- Guild: {getattr(ctx.guild, 'name', 'DM or Unknown')}\n"
                f"- Error: {type(error).__name__}: {error}\n"
            )
            try:
                await ctx.respond("An internal error occurred while executing this command.", ephemeral=True)
            except discord.NotFound:
                # Interaction already closed, just skip
                pass

    # -----------------------
    # USER CONTEXT COMMAND
    # -----------------------
    @commands.user_command(
        name="Check the user's time",
        integration_types=[discord.IntegrationType.user_install]
    )
    async def get_time(self, ctx, user: discord.User):
        userid = str(user.id)
        tz_info = user_timezones.find_one({"userid": userid})

        if not tz_info:
            await ctx.respond(
                f"{user.mention}'s timezone is not set. Ask them to set it using the `/add` command.",
                ephemeral=True
            )
            return

        try:
            tz = pytz.timezone(tz_info["timezone"])
            now = datetime.now(tz)
            await ctx.respond(
                f"{user.mention}'s current time is: **{now.strftime('%Y-%m-%d %H:%M:%S')}**",
                ephemeral=True
            )
        except Exception as e:
            await ctx.respond("Error getting time.", ephemeral=True)
            print(f"[Error getting time for {user.id}]: {e}")

    # -----------------------
    # SLASH COMMAND
    # -----------------------
    @commands.slash_command(
        name="add",
        description="Set or update a user's timezone (e.g., America/New_York).",
        integration_types=[discord.IntegrationType.user_install]
    )
    async def addtz(self, ctx, user: discord.User, timezone: str):
        userid = str(user.id)

        try:
            pytz.timezone(timezone)
        except pytz.UnknownTimeZoneError:
            await ctx.respond(
                "Invalid timezone. Please provide a valid timezone (e.g., `America/Bogota`).",
                ephemeral=True
            )
            return

        existing_entry = user_timezones.find_one({"userid": userid})

        if existing_entry:
            user_timezones.update_one({"userid": userid}, {"$set": {"timezone": timezone}})
            await ctx.respond(
                f"{user.mention}'s timezone has been **updated** to `{timezone}`.",
                ephemeral=True
            )
        else:
            user_timezones.insert_one({"userid": userid, "timezone": timezone})
            await ctx.respond(
                f"{user.mention}'s timezone has been **set** to `{timezone}`.",
                ephemeral=True
            )


def setup(bot):
    bot.add_cog(Usertime(bot))

import discord
import pytz


def timezone_autocomplete(self, ctx: discord.AutocompleteContext):
    """All timezones with filtering"""
    all_timezones = pytz.all_timezones
    # Filter based on what user typed
    if ctx.value:
        return [tz for tz in all_timezones if ctx.value.lower() in tz.lower()][:25]
    # If nothing typed, show common ones
    return [
        "America/New_York", "America/Chicago", "America/Los_Angeles",
        "Europe/London", "Europe/Paris", "Asia/Tokyo", "UTC"
    ][:25]

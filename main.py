import discord  # pip install py-cord
import os  # part of standard library
from discord.ext import commands  # part of py-cord
from datetime import datetime  # part of standard library
from dotenv import load_dotenv  # pip install python-dotenv
import pytz  # pip install pytz

load_dotenv()

bot = commands.Bot(intents=discord.Intents.default(), auto_sync_commands=True)
bot.tz = pytz.timezone(os.getenv("TIMEZONE"))
bot.start_time = datetime.now(bot.tz)

extensions = [  # Auto-load all command files in cmds/ directory
    f"cmds.{file[:-3]}" for file in os.listdir("cmds") if file.endswith(".py")
]


@bot.event
async def on_connect():  # Load extensions and print bot info on connect
    print(
        f"""
    ★ | Authenticated in Discord.
    User: {bot.user.name}
    ID: {bot.user.id}
        """)

    if extensions and not hasattr(bot, 'synced'):
        print("★ | Loading extensions...")
        for ext in extensions:
            try:
                bot.load_extension(ext)
                print(f"✓ | Loaded {ext}")
            except Exception as e:
                print(f"✗ | Failed to load {ext}: {e}")
        print()


@bot.event
async def on_ready():  # Print bot info on ready
    if not hasattr(bot, 'synced'):
        await bot.sync_commands(force=True)
        bot.synced = True
        print("✓ | Commands synced.")

    print("January 25th 2026: You still can't retrieve the user count directly.")
    print(f"✓ | Ready! Ping: {round(bot.latency * 1000)}ms")


@bot.before_invoke
async def auto_indicator(ctx):
    """Automatically show 'working...' for both app and prefix commands."""
    try:
        # Slash / user / message commands (Interactions)
        if isinstance(ctx, discord.ApplicationContext):
            if not ctx.response.is_done():
                await ctx.defer(ephemeral=True)

        # Classic text (prefix) commands
        else:
            await ctx.trigger_typing()

    except discord.NotFound:
        # Interaction expired or bot reconnected mid-command — safe to ignore
        pass
    except Exception as e:
        print(f"[auto_indicator] Error while indicating work: {e}")


@bot.event
async def on_application_command_error(ctx, error):
    invoker = ctx.author
    server = ctx.guild.name if hasattr(
        ctx, "guild") and ctx.guild != None else "Executed in DM"
    print(
        f"""
    !! | An error ocurred.          
    User: {invoker}
    Executed in: {server}
    Error: {type(error).__module__}.{type(error).__name__}
    Information: {error}
        """)

    if ctx.interaction.response.is_done():
        return

bot.run(os.getenv("TOKEN"))

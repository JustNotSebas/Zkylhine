import discord, os # pip install py-cord
from discord.ext import commands # part of py-cord
from datetime import datetime # part of standard library
from dotenv import load_dotenv # pip install python-dotenv

load_dotenv()

token = os.getenv("TOKEN") # Set on .env file or environment variable
intents = discord.Intents.default() # For convenience; adjust as needed
bot = commands.Bot(intents=intents, auto_sync_commands=True)
bot.start_time = datetime.now()

extensions = [ # Auto-load all command files in cmds/ directory
    f"cmds.{file[:-3]}" for file in os.listdir("cmds") if file.endswith(".py")
]

@bot.event
async def on_connect(): # Load extensions and print bot info on connect
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Connected as {bot.user.name} ({bot.user.id})")
    if extensions:
        print("Loading extensions...")
        for ext in extensions:
            try:
                bot.load_extension(ext)
                print(f"✓ Loaded {ext}")
            except Exception as e:
                print(f"✗ Failed to load {ext}: {e}")

@bot.event
async def on_ready(): # Print bot info on ready
    if not hasattr(bot, 'synced'):
        await bot.sync_commands(force=True)
        print("✓ Commands synced.")
        bot.synced = True
        
    print("Guilds:")
    for guild in bot.guilds:
        print(f"- {guild.name} (ID: {guild.id})")
    print(f"✓ Ready! Ping: {round(bot.latency * 1000)}ms")

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


bot.run(token)


import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Load cogs
async def load_extensions():
    await bot.load_extension('cogs.temperature')

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')

async def main():
    await load_extensions()
    await bot.start(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

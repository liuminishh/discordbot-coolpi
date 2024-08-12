import discord
from discord.ext import commands
import os
from gpiozero import CPUTemperature
from crontab import CronTab
from dotenv import load_dotenv

load_dotenv()

class Temperature(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='temperature')
    async def temp(self, ctx):
        """Check the Raspberry Pi hardware temperature."""
        try:
            cpu = CPUTemperature()
            temp = cpu.temperature
            await ctx.send(f"The current hardware temperature is {temp:.2f}°C.")
        except Exception as e:
            await ctx.send(f"Failed to retrieve temperature: {str(e)}")

    @commands.command(name='schedule')
    async def schedule_temp_check(self, ctx):
        """Schedule a cron job to check temperature every 30 minutes."""
        try:
            # Get the path to the current script
            script_path = os.path.abspath(__file__)

            # Create a cron job
            cron = CronTab(user=True)
            job = cron.new(command=f'python3 {script_path}', comment='Temperature Check Cron Job')
            job.minute.on(0, 1)  # Every 30 minutes

            cron.write()

            await ctx.send("Scheduled a temperature check every 30 minutes.")
        except Exception as e:
            await ctx.send(f"Failed to schedule the temperature check: {str(e)}")

async def setup(bot):
    await bot.add_cog(Temperature(bot))

# Standalone execution check for cron job
if __name__ == "__main__":
    try:
        cpu = CPUTemperature()
        temp = cpu.temperature

        bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
        bot_channel = bot.get_channel(1272423613164818464)  # Replace with your channel ID

        if temp > 70:
            message = f"Warning: The CPU temperature is {temp:.2f}°C, which is above the threshold of 70°C."
        else:
            message = f"The current hardware temperature is {temp:.2f}°C."

        async def send_temp_alert():
            async with bot:
                await bot_channel.send(message)

        bot.run(os.getenv("DISCORD_TOKEN"))
    except Exception as e:
        print(f"Failed to retrieve temperature: {str(e)}")

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
            script_path = os.path.abspath(__file__)
            cron = CronTab(user=True)
            job = cron.new(command=f'python3 {script_path}', comment='Temperature Check Cron Job')
            job.minute.every(30)

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

        if temp > 70:
            bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
            bot_channel_id = 1272423613164818464

            message = f"Warning: The CPU temperature is {temp:.2f}°C, which is above the threshold of 70°C."

            async def send_temp_alert():
                bot_channel = bot.get_channel(bot_channel_id)
                if bot_channel:
                    await bot_channel.send(message)
                else:
                    print(f"Could not find channel with ID {bot_channel_id}")

            @bot.event
            async def on_ready():
                await send_temp_alert()
                await bot.close()

            bot.run(os.getenv("DISCORD_TOKEN"))
        else:
            print(f"The current hardware temperature is {temp:.2f}°C.")

    except Exception as e:
        print(f"Failed to retrieve temperature: {str(e)}")

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
            await ctx.send(f"The current hardware temperature is {temp:.2f}�C.")
        except Exception as e:
            await ctx.send(f"Failed to retrieve temperature: {str(e)}")

    @commands.command(name='schedule')
    async def schedule_temp_check(self, ctx):
        """Schedule a cron job to check temperature every minute."""
        try:
            # Get the path to the current script
            script_path = os.path.abspath(__file__)

            # Create a cron job
            cron = CronTab(user=True)
            job = cron.new(command=f'python3 {script_path} check_temp', comment='Temperature Check Cron Job')
            job.minute.every(1)

            cron.write()

            await ctx.send("Scheduled a temperature check every minute.")
        except Exception as e:
            await ctx.send(f"Failed to schedule the temperature check: {str(e)}")

    @commands.command(name='check_temp')
    async def check_temp(self, ctx=None):
        """Check the Raspberry Pi hardware temperature and send an alert if it's above 70�C."""
        try:
            cpu = CPUTemperature()
            temp = cpu.temperature
            if temp > 70:
                channel = self.bot.get_channel(1272423613164818464)  # Replace with your channel ID
                await channel.send(f"Warning: The CPU temperature is {temp:.2f}�C, which is above the threshold of 70�C.")
        except Exception as e:
            if ctx:
                await ctx.send(f"Failed to retrieve temperature: {str(e)}")
            else:
                print(f"Failed to retrieve temperature: {str(e)}")

async def setup(bot):
    await bot.add_cog(Temperature(bot))

# Standalone execution check for cron job
if __name__ == "__main__":
    from dotenv import load_dotenv
    import discord
    from discord.ext import commands

    load_dotenv()
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)
    bot.run(os.getenv("DISCORD_TOKEN"))

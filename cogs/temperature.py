import discord
from discord.ext import commands
from gpiozero import CPUTemperature

class Temperature(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='temperature')
    async def temp(self, ctx):
        """Check the Raspberry Pi CPU temperature."""
        try:
            cpu = CPUTemperature()
            temp = cpu.temperature
            await ctx.send(f"The current CPU temperature is {temp:.2f}°C.")
        except Exception as e:
            await ctx.send(f"Failed to retrieve temperature: {str(e)}")

async def setup(bot):
    await bot.add_cog(Temperature(bot))

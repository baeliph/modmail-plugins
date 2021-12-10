import discord
from discord.ext import commands, tasks

class Speak(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def plswork(self, ctx):
        await ctx.reply("Should work.")
        
    @commands.command()
    async def speak(self, ctx, channel: discord.TextChannel, *, message: str):
        await channel.send(message)

def setup(bot):
    cog = Speak(bot)
    bot.add_cog(cog)

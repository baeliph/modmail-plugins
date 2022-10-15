import discord
from discord.ext import commands, tasks

class GetUsers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def getusers(self, ctx, channel: discord.TextChannel):
        """
        Returns a list of all the users who sent a message in the given channel.
        Usage: x/getusers #channel
        """

        def batch(iterable, n=1):
            """
            Helper function that splits the given list into sub-lists of size n.
            """
            l = len(iterable)
            for ndx in range(0, l, n):
                yield iterable[ndx:min(ndx + n, l)]
        
        # Get all the messages in a channel.
        await ctx.channel.send("Working...")
        messages = await channel.history(limit=None).flatten()
        await ctx.channel.send("Got all the messages in {}. Total: {}".format(channel.name, len(messages)))
        
        # Get a list of unique users who sent those messages.
        users = set()
        for msg in messages:
            if not msg.author.bot:
                users.add(str(msg.author))
        users = list(users)

        # Output the users in batches of 50.
        for users_batch in batch(users, 50):
            await ctx.channel.send("\n".join(users_batch))

async def setup(bot):
    cog = GetUsers(bot)
    await bot.add_cog(cog)

import discord
from discord.ext import commands, tasks
import numpy as np
import math

class Chances(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def character(self, ctx, wishes: int, pity: int, guarantee: str):
        if pity > 90:
            await ctx.send_help(ctx.command)
            return

        guarantee_bool = "y" in guarantee.lower()
        embed = self.five_star_character(wishes, pity, guarantee_bool)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def weapon(self, ctx, wishes: int, pity: int):
        if pity > 80:
            await ctx.send_help(ctx.command)
            return

        embed = self.five_star_weapon(wishes, pity)
        await ctx.send(embed=embed)

    @staticmethod
    def five_star_character(wishes, pity, guarantee): 
        P = 0.006
        ramp_rate = 0.06
            
        cum_prob = np.zeros((91,))
        cum_prob[0] = 0
        cum_prob[1:74] = P
        cum_prob[90] = 1
        for i in range(74, 90):
            cum_prob[i] = P + ramp_rate * (i-73)
        ones = np.ones((91,))
        complement = ones - cum_prob
        base_gf_coefficents = np.zeros((91, ))
        for i in range(91):
            base_gf_coefficents[i] = np.prod(complement[0:i]) * cum_prob[i]
        gf_coefficents = np.zeros((14, 1 + 90*14))
        pity_sum = np.cumsum(base_gf_coefficents)[pity]
        gf_coefficents[0][pity+1:91] = base_gf_coefficents[pity+1:] / (1-pity_sum)
        for i in range(1, 14):
            for j in range(1, 90*i+1):
                gf_coefficents[i][j: j+91] += gf_coefficents[i-1][j] * base_gf_coefficents[0:91]
        five_star_prob = gf_coefficents.cumsum(axis=1)[:, wishes+pity]
        
        embed = discord.Embed().from_dict({
            "title" : "Character chances calculator",
            "description" : "If you wish to understand the math behind this calculation, view the explanation [here](https://drive.google.com/file/d/1EECcjNVpfiOTqRoS48hHWqH2Ake902vq/view?usp=sharing)",
            "color" : 0x4eb9a0,
        })
        for i in range(7):
            embed.add_field(name=f"C{i}", value=f"{np.format_float_positional((100 * np.dot([math.comb(i+1-guarantee, j)/(2 ** (i+1-guarantee)) for j in range(i+2-guarantee) ], five_star_prob[i:2*i+2-guarantee])), precision=4, unique=False, fractional=False, trim='k')}%")
        embed.set_footer(text="Credit bryanli#2718 @ Kusanali Mains")
        return embed

    @staticmethod
    def five_star_weapon(wishes, pity):
        P = 0.007
        ramp_rate = 0.07
        cum_prob = np.zeros((78,))
        cum_prob[0] = 0
        cum_prob[1:63] = P
        cum_prob[77] = 1
        for i in range(63, 77):
            cum_prob[i] = P + ramp_rate * (i-62)
        ones = np.ones((78,))
        complement = ones - cum_prob
        base_gf_coefficents = np.zeros((78, ))
        for i in range(78):
            base_gf_coefficents[i] = np.prod(complement[0:i]) * cum_prob[i]
        gf_coefficents = np.zeros((15, 1 + 77*15))
        pity_sum = np.cumsum(base_gf_coefficents)[pity]
        gf_coefficents[0][pity+1:78] = base_gf_coefficents[pity+1:] / (1-pity_sum)
        for i in range(1, 15):
            for j in range(1, 77*i+1):
                gf_coefficents[i][j: j+78] += gf_coefficents[i-1][j] * base_gf_coefficents[0:78]
        five_star_prob = gf_coefficents.cumsum(axis=1)[:, wishes+pity]
        path_gf_coefficents = np.zeros((5, 16))
        path_gf_coefficents[0][0:4] = [0, 3/8, 17/64, 23 / 64] #rly wierd numbers but trust the process
        for i in range(1, 5):
            for j in range(1, 3*i+1):
                path_gf_coefficents[i][j: j+4] += path_gf_coefficents[i-1][j] * path_gf_coefficents[0][0:4]
        
        embed = discord.Embed().from_dict({
            "title" : "Weapon banner chances calculator",
            "description" : "If you wish to understand the math behind this calculation, view the explanation [here](https://drive.google.com/file/d/1EECcjNVpfiOTqRoS48hHWqH2Ake902vq/view?usp=sharing)",
            "color" : 0x4eb9a0,
        })
        for i in range(5):
            embed.add_field(name=f"R{i+1}", value=f"{np.format_float_positional((100 * np.dot(path_gf_coefficents[i][1:], five_star_prob[:])), precision=4, unique=False, fractional=False, trim='k')}%") 
        embed.set_footer(text="Credit bryanli#2718 @ Kusanali Mains")
        return embed

async def setup(bot):
    cog = Chances(bot)
    await bot.add_cog(cog)


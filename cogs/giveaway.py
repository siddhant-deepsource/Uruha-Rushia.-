import discord
import datetime
import time
import asyncio
import random
import time
import re

from datetime import timedelta
from time import sleep

from discord.ext import commands
from discord import Embed

time_units = {'s': 'seconds', 'm': 'minutes', 'h': 'hours', 'd': 'days', 'w': 'weeks'}

def make_sleep():
    async def sleep(delay, result=None, *, loop=None):
        coro = asyncio.sleep(delay, result=result, loop=loop)
        task = asyncio.ensure_future(coro)
        sleep.tasks.add(task)
        try:
            return await task
        except asyncio.CancelledError:
            return result
        finally:
            sleep.tasks.remove(task)

    sleep.tasks = set()
    sleep.cancel_all = lambda: sum(task.cancel() for task in sleep.tasks)
    return sleep

def to_seconds(s):
    return int(timedelta(**{

        time_units.get(m.group('unit').lower(), 'seconds'): int(m.group('val'))
        
        for m in re.finditer(r'(?P<val>\d+)(?P<unit>[smhdw]?)', s, flags=re.I)
    
    }).total_seconds())

class Giveaway(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ["gstart", "g", "gs"])
    @commands.has_permissions(manage_messages=True)
    async def giveaway(self, ctx, time, *, prize):
        giveawayembed = discord.Embed(
            title="🎉 New Giveaway! 🎉",
            colour=discord.Color.green()
            )

        giveawayembed.add_field(name="Prize", value="**{}**".format(prize), inline=False)
        giveawayembed.add_field(name="Hosted by", value=f"{ctx.author.mention}", inline=False)
        giveawayembed.add_field(name="Ends in", value="**{}**".format(time))

        giveawayembed.set_footer(text="React with 🎉 to join the giveaway!")

        msg = await ctx.send(embed=giveawayembed)

        await msg.add_reaction("🎉")

        await asyncio.sleep(to_seconds(time))

        msg = await msg.channel.fetch_message(msg.id)
        winner = None
        
        for reaction in msg.reactions:
            if reaction.emoji == "🎉":
                users = await reaction.users().flatten()
                users.remove(self.client.user)
                winner = random.choice(users)

        if winner is not None:
            endembed = discord.Embed(
                title="Giveaway ended!",
                description="Prize: **{}**\nWinner: **{}**!".format(prize, winner),
                colour=discord.Color.red()
                )
            
            await msg.edit(embed=endembed)

    @giveaway.error
    async def giveaway_error(self, ctx, error):
        await ctx.send(error)
        raise error

def setup(client):
    client.add_cog(Giveaway(client))
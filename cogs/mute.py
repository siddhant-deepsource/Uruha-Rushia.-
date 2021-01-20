import discord
import datetime
import asyncio
import re

from datetime import timedelta

from discord import Embed
from discord.ext import commands

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

class Mute(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	@commands.guild_only()
	@commands.has_guild_permissions(mute_members=True, administrator=True)
	async def mute(self, ctx, member: discord.Member , time, *, reason):
		guild = ctx.guild
		channel = ctx.message.channel
		
		role = discord.utils.get(guild.roles, name='Muted' or 'muted')
		
		if role:
			await member.add_roles(role)

			perms = channel.overwrites_for(role)
			perms.send_messages=False

			await channel.set_permissions(member, overwrite=perms, reason="Muted!")

			mutedembed = discord.Embed(
				title=f"Muted {member.name}",
				description=f"For the reason `{reason}`\nModerator: {ctx.author.mention}",
				timestamp=datetime.datetime.now(),
				colour=discord.Color.red()
				)
			
			await ctx.send(embed=mutedembed)

			await asyncio.sleep(to_seconds(time))

			await member.remove_roles(role, reason="Unmuted")
			await ctx.send("Unmuted {}".format(member))
			return

		else:
			perms = discord.Permissions(send_messages=False, read_messages=True)
			newRole = await guild.create_role(name="Muted", permissions=perms)

			await member.add_roles(newRole)
				
			mutembed = discord.Embed(
				title=f"Muted {member.name}",
				description="For the reason `{}`/nModerator: `{}` (`{}#{}`)".format(reason, ctx.author.mention, ctx.author.name, ctx.author.discriminator),
				timestamp=datetime.datetime.now(),
				colour=discord.Color.red()
				)

			await ctx.send(embed=mutembed)

			await asyncio.sleep(to_seconds(time))

			await member.remove_roles(newRole, reason="Unmuted", atomic=True)
			await ctx.send("Unmuted {}".format(member))
			return

	@mute.error
	async def mute_error(self, ctx, error):
		await ctx.send(error)
		print(error)
		raise error

	@commands.command()
	@commands.guild_only()
	@commands.has_guild_permissions(mute_members=True, administrator=True)
	async def unmute(self, ctx, member: discord.Member):
		guild = ctx.guild

		role = discord.utils.get(guild.roles, name='Muted' or 'muted')

		if role:
			await member.remove_roles(role)
			await ctx.send("Unmuted {}".format(member))
			return

def setup(client):
	client.add_cog(Mute(client))
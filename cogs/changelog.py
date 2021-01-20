import discord, datetime, time

from time import sleep
from discord import Embed
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

class Changelog(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(aliases = ["change", "chlog"])
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def changelog(self, ctx):

		async with ctx.channel.typing():
		
			changelogembed = discord.Embed(
				title="Changelog",
				colour=discord.Color.green(),
				timestamp=datetime.datetime.now()
				)

			changelogembed.add_field(name="[!] NEW FEATURE!", value="Bot is now 24/7!", inline=False)
			changelogembed.add_field(name="[+] Added a command", value="Added `mute` and `unmute` :')", inline=False)
			changelogembed.add_field(name="[+] Added a command", value="Added corona stuff", inline=False)
			changelogembed.add_field(name="[+] Added a command", value="Added `nuke` :3", inline=False)
			changelogembed.add_field(name='[!] Improved a command', value='Improved help (,help <category>', inline=False)
			changelogembed.add_field(name='[+] Added a command', value='Added `bug`, (Report and bug)', inline=False)
			changelogembed.add_field(name='[+] Added a command', value='Added `nick` and `unnick` :>', inline=False)

			await ctx.send(ctx.author.mention, embed=changelogembed)

	@changelog.error
	async def changelog_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(' {} Cooldown activated! Please try again in {:.2}s'.format(ctx.author.mention, error.retry_after))

		else:
			await ctx.send(error)
			print(error)

def setup(client):
	client.add_cog(Changelog(client))
import discord
from discord import Embed
from discord.ext import commands

class Greater(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def greater(self, ctx, number1, number2):
		if number1 == number2:
			await ctx.send(f"{number1} is **the same** to {number2}")
		
		elif number1 > number2:
			await ctx.send(f"{number1} is **Greater** than {number2}")

		elif number1 < number2:
			await ctx.send(f"{number1} is **Weaker** than {number2}")

		else:
			await ctx.send(f"{ctx.user.mention}, there was a problem running this command please try again")

def setup(client):
	client.add_cog(Greater(client))
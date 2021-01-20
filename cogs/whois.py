import discord
from discord.ext import commands

class Whois(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(aliases = ["userinfo", "uinf", "userinf"])
	async def whois(self, ctx, *, user: discord.Member = None):
		
		user = user or ctx.author or user.id

		whoisembed = discord.Embed(
			title=f"{user} Info",
			colour=discord.Color.green()

			).set_footer(
			icon_url=ctx.author.avatar_url,
			text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}"

			).set_thumbnail(
			url=user.avatar_url

			).add_field(
			name="User Name",
			value=user.name

			).add_field(
			name="User Discriminator",
			value=user.discriminator

			).add_field(
			name="Created at",
			value=user.created_at

			).add_field(
			name="User ID",
			value=user.id

			).add_field(
			name="Created at",
			value=user.created_at

			).add_field(
			name="Bot",
			value=user.bot
			)

		await ctx.send(ctx.author.mention, embed=whoisembed)

	@whois.error
	async def whois_error(self, ctx, error):
		await ctx.send(f"{ctx.author.mention}, Something went wrong. Please try again.")
		return print(error)


def setup(client):
	client.add_cog(Whois(client))
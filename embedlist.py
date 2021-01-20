import discord, datetime
from discord import Embed
from discord.ext import commands

joinembed = discord.Embed(
	title=":wave: Hello :wave:",
	description="Thank's for adding me to your server!\nMy prefix is `,`.\nTo get started, please type `,help`.",
	colour=discord.Color.green(),
	timestamp=datetime.datetime.utcfromtimestamp(1599119820)
	)

prefixembed = discord.Embed(
	title="My prefix is `,`!",
	description="Do ,help to see my list of commands.",
	colour=discord.Color.green(),
	timestamp=datetime.datetime.utcfromtimestamp(1599119820)
	)
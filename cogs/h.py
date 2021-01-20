import discord
import reddit
import praw
import redditset
import random
import datetime
from redditset import reddit
from discord import Embed
from discord.ext import commands
import json

choices = "hentai", "hentaibondage"

class Hentai(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	@commands.is_nsfw()
	@commands.cooldown(1, 4, commands.BucketType.user) 
	async def hentai(self, ctx):

		async with ctx.channel.typing():

			memes_submissions = reddit.subreddit(f'{random.choice(choices)}').hot()
			post_to_pick = random.randint(1, 100)
			for i in range(0, post_to_pick):	
			    submission = next(x for x in memes_submissions if not x.stickied)

			memeembed = discord.Embed(
				title=submission.title,
				timestamp=datetime.datetime.utcfromtimestamp(1599119820)
				)
			    
			memeembed.set_image(url=submission.url)
			    
			await ctx.send(embed=memeembed)

	@hentai.error
	async def hentai_error(self, ctx, error):
		if isintance(error, CommandOnCooldown):
			await ctx.send("Cooldown  activated, please try again in `{:.2}`s".format(error.retry_after))

	@hentai.error
	async def hentai_error(self, ctx, error):
		await ctx.send(error)
		print(error)

	@commands.command()
	@commands.is_nsfw()
	async def dmhentai(self, ctx):
		await ctx.message.delete()

		async with ctx.channel.typing():

			memes_submissions = reddit.subreddit('hentai' or 'hentaibondage').hot()
			post_to_pick = random.randint(1, 100)
			for i in range(0, post_to_pick):	
			    submission = next(x for x in memes_submissions if not x.stickied)

			memeembed = discord.Embed(
				title=submission.title,
				timestamp=datetime.datetime.utcfromtimestamp(1599119820)
				)
			    
			memeembed.set_image(url=submission.url)
			    
			await ctx.author.send(embed=memeembed)

	@dmhentai.error
	async def dmhentai_error(self, ctx, error):
		await ctx.send(error)
		print(error)

def setup(client):
	client.add_cog(Hentai(client))
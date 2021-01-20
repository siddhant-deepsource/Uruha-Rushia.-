import discord
import reddit
import praw
import random
import datetime
from discord import Embed
from discord.ext import commands
from redditset import reddit

class Trap(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(aliases = ["traph", "traphentai"])
	@commands.is_nsfw()
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def trap(self, ctx):

		async with ctx.channel.typing():

			memes_submissions = reddit.subreddit('traphentai').hot()
			post_to_pick = random.randint(1, 100)
			for i in range(0, post_to_pick):
			    submission = next(x for x in memes_submissions if not x.stickied)

			memeembed = discord.Embed(
				title=submission.title,
				timestamp=datetime.datetime.now()
				)
			    
			memeembed.set_image(url=submission.url)
			    
			await ctx.send(embed=memeembed)

	@trap.error
	async def trap_error(self, ctx, error):
		await ctx.send(error)
		print(error)
		
def setup(client):
	client.add_cog(Trap(client))
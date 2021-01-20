import discord
import datetime
import random

from discord.ext.commands.cooldowns import BucketType
from discord import Embed
from discord.ext import commands

class Help(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(aliases = ['Help'])
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def help(self, ctx, *, category = None):

	    categories = {
	        'mod': ['mod',],
	        'fun': ['fun',],
	        'nsfw': ['nsfw',],
	        'covid': ['cv',],
	        'random': ['random']
	    }
	    
	    if category is None:
	       desc = '\n'.join(categories.keys())
	       embed = discord.Embed(
	            title="Help list",
	            timestamp=datetime.datetime.now(),
	            colour=discord.Color.green(),
	            description=f'Categories:\n{desc}'
	        )

	       await ctx.send(ctx.author.mention, embed=embed)
	    
	    elif category is not None:
	    	#Mod Help
	    	if category in ['mod', 'moderation', 'Mod', 'Moderation']:
	    		modhelpembed = discord.Embed(
	    			title="⚒️ Moderation Help ⚒️",
	    			timestamp=datetime.datetime.now(),
	    			colour=discord.Color.green()
	    			)

	    		modhelpembed.add_field(name='kick', value="Kicks a member from the server", inline=False)
	    		modhelpembed.add_field(name='ban', value='bans a member from the server', inline=False)
	    		modhelpembed.add_field(name='unban', value='unbans a member from the server', inline=False)
	    		modhelpembed.add_field(name="nuke", value="Nukes a channel :>", inline=False)
	    		modhelpembed.add_field(name='mute', value="Mute a member", inline=False)
	    		modhelpembed.add_field(name="purge", value='purges (deletes) a certain ammount of messages', inline=False)
	    		
	    		await ctx.send(f'{ctx.author.mention}')
	    		await ctx.send(embed=modhelpembed)
	    		return

	    	#Fun Help
	    	elif category in ['fun', 'Fun']:
	    		funembed = discord.Embed(
	    			title="🙂 Fun Help 🙂",
	    			timestamp=datetime.datetime.now(),
	    			colour=discord.Color.green()
	    			)
	    		funembed.add_field(name='meme', value='shows a meme from r/memes', inline=False)
	    		funembed.add_field(name='waifu', value='shows a waifu (pic or link) from r/waifu', inline=False)
	    		funembed.add_field(name='anime', value='shows a anime (image or link) from r/anime', inline=False)
	    		funembed.add_field(name='spotify', value='Tells you the targeted user listening on', inline=False)
	    		funembed.add_field(name="song", value="Tells you the whats the targeted user listening in Spotify", inline=False)
	    		funembed.add_field(name="album", value="Tells you whats the targeted user album", inline=False)
	    		funembed.add_field(name="timer", value="Sets a Timer for you.", inline=False)

	    		await ctx.send(f'{ctx.author.mention}')
	    		await ctx.send(embed=funembed)
	    		return

	    	elif category in ['covid', 'Covid', 'CV', 'Cv', 'cv', 'cV', 'corona', 'Corona']:
	    		coronaembed = discord.Embed(
	    			title="😷 Covid-19 Help 😷" ,
	    			timestamp=datetime.datetime.now(),
	    			colour=discord.Color.green()
	    			)

	    		coronaembed.add_field(name='cv', value='Covid status', inline=False)
	    		coronaembed.add_field(name='cvlb', value='Covid-19 Leaderboard', inline=False)
	    		coronaembed.add_field(name='cvh', value='Covid-19 History', inline=False)

	    		await ctx.send(ctx.author.mention, embed=coronaembed)
	    		return

	    	elif category in ['nsfw']:
	    		nsfwembed = discord.Embed(
	    			title='🔞 NSFW 🔞',
	    			colour=discord.Color.red(),
	    			timestamp=datetime.datetime.now()
	    			)

	    		nsfwembed.add_field(name='hentai', value='Get a random hentai pics from r/hentai', inline=False)
	    		nsfwembed.add_field(name='dmhentai', value='Get a random hentai pics from r/hentai but in dms', inline=False)
	    		nsfwembed.add_field(name='traphentai', value='Trap Hentai', inline=False)

	    		await ctx.send(ctx.author.mention, embed=nsfwembed)
	    		return

	    	elif category in ['random', 'ownerhelp']:
	    		randomhelp = discord.Embed(
	    			title='❓ Random help ❓',
	    			colour=discord.Color.green(),
	    			timestamp=datetime.datetime.now()
	    			)

	    		randomhelp.add_field(name='suggest', value='Suggest a command', inline=False)
	    		randomhelp.add_field(name='bug', value='Report a bug', inline=False)
	    		randomhelp.add_field(name='howgay', value='A Random Chances (0 - 100%)', inline=False)
	    		randomhelp.add_field(name='drop', value='Drop a stuff.', inline=False)
	    		randomhelp.add_field(name='giveaway', value='Giveaway command', inline=False)
	    		randomhelp.add_field(name='raffle', value='Raffle (Random winner)', inline=False)
	    		randomhelp.add_field(name='info', value='Bot info', inline=False)
	    		randomhelp.add_field(name='whois', value='user info', inline=False)
	    		randomhelp.add_field(name='song', value='spotify dong (listening to)', inline=False)
	    		randomhelp.add_field(name='say', value='make the bot repeats the word that you included', inline=False)
	    		randomhelp.add_field(name='spotify', value='Spotify (Full Info)', inline=False)
	    		randomhelp.add_field(name='album', value='Spotify album', inline=False)
	    		randomhelp.add_field(name='artist', value='Spotify (listening to) Artist', inline=False)

	    		await ctx.send(ctx.author.mention, embed=randomhelp)
	    		return

	    	else:
	    		category = category.lower()
	    		if not category in categories.keys():
	    			await ctx.send('Category name is invalid!')
	    			return

	    		embed = discord.Embed(
	    			title=f"{category.capitalize()} Help",
	    			timestamp=datetime.datetime.now(),
	    			colour=discord.Color.green()
	    			)

	    		for cmd in categories[category]:
	    			cmd = client.get_command(cmd)
	    			embed.add_field(name=cmd.name, value=cmd.description)

	    		await ctx.send(ctx.author.mention, embed=embed)
	    		return

def setup(client):
	client.add_cog(Help(client))
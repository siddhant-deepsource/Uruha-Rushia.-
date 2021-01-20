import discord, json, random, os, asyncio, datetime, youtube_dl, math, builtins, requests
import reddit, praw, re
import aiohttp

import time
from time import sleep

from discord.ext import commands, tasks
from discord.utils import get
from discord import Spotify, Embed, Reaction

from itertools import cycle
from setuptools import setup, find_packages
from codecs import open
from os import path

from discord.ext.commands import when_mentioned_or

import settings
from settings import language, developer, devteam, ownerid, ownertag, no_perm, invitelink
from settings import mainprefix

import embedlist
from embedlist import joinembed, prefixembed

import perms
from perms import missingreqarg, no_perm
	
import redditset
from redditset import reddit

from datetime import timedelta
from time import sleep

from keep_alive import keep_alive

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

players = {}


def get_prefix(client, message):
	return when_mentioned_or(",")(client, message)	
choices = "hentai", "hentaibondage"
client = commands.Bot(command_prefix = get_prefix)
client.remove_command('help')
builtins.bot = client

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

@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send(f'{ctx.author.mention}, Invalid command, please look at `,help` to see my command list.')

@client.event
async def on_ready():
	change_status.start()
	testemony.start()
	print("Bot Info:")
	print("===============================")
	print(f"Bot Tag       : {client.user.name}#{client.user.discriminator}")
	print("===============================")
	print(f"Bot Ping      : {round(client.latency * 1000)} ms")
	print("===============================")
	print(f"Playing On    : " + str(len(client.guilds)) + " Servers")
	print("===============================")
	print(f"Discord.Py Version: {discord.__version__}")
	print()
	
	for cog in os.listdir("./cogs"):
		if cog.endswith(".py"):
			try:
				cog = f"cogs.{cog.replace('.py', '')}"
				client.load_extension(cog)
			except Exception as e:
				print(f"{cog} Can not be loaded")
				raise e
			else:
				print("{} has been succesfully Loaded.".format(cog))

@tasks.loop(seconds=5)
async def change_status():
	await client.change_presence(activity=discord.Game(next(status))),
	await client.change_presence(activity=discord.Streaming(name=f"Watching " + str(len(client.guilds)) + " Servers", url="http://www.twitch.tv/pokimane"))

status = cycle([f',help | now with waifu command!', f',help | Now with meme command!'])

@tasks.loop(seconds=1)
async def testemony():
    while True:
        try:
            memes_submissions = reddit.subreddit(f'{random.choice(choices)}').hot()
            ss1 = memes_submissions = reddit.subreddit(f'{random.choice(choices)}').top(limit=100000)
            post_to_pick = random.randint(1, 100000)
            for i in range(0, post_to_pick):
                submission = next(x for x in memes_submissions if not x.stickied)

                channel = client.get_channel(750511185568464926)

                s1 = next(x for x in ss1 if not x.stickied)

                await channel.send(s1.title + "\n" + s1.url)

                await channel.send(submission.title + "\n" + submission.url)
                c = requests.get('https://nekos.life/api/v2/img/cum_jpg')
                cum = json.loads(c.text)
                await channel.send(cum["url"])
                b = requests.get('https://nekos.life/api/v2/img/blowjob')
                bj = json.loads(b.text)
                await channel.send(bj["url"])
                hn = requests.get('https://nekos.life/api/v2/img/hentai')
                j = json.loads(hn.text)
                await channel.send(j["url"])
                m = requests.get('https://nekos.life/api/v2/img/maid')
                md = json.loads(m.text)
                await channel.send(md["url"])
                p = requests.get('https://nekos.life/api/v2/img/pussy')
                ps = json.loads(p.text)
                await channel.send(ps["url"])
                u = requests.get('https://nekos.life/api/v2/img/uniform')
                uf = json.loads(u.text)
                await channel.send(uf["url"])
                y = requests.get('https://nekos.life/api/v2/img/yuri')
                yr = json.loads(y.text)
                await channel.send(yr["url"])
                continue
        except StopIteration:
            continue
        except ValueError:
            continue
        except:
            continue
        else:
            continue

@client.command()
async def ping(ctx):
	await ctx.send(f":ping_pong:! My ping is {round(client.latency * 1000)}ms!")

@client.command()
async def say(ctx, *, message):
	await ctx.send(message)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member , *, reason=None):

	banembed = discord.Embed(
		title="Member banned!",
		description=f"banned {member} for the reason {reason}.\nAuthor: {ctx.author.mention}"
		)

	await member.ban(reason=reason)
	await ctx.send(embed=banembed)

	bannedembed = discord.Embed(
		title="You've been banned.",
		description=f"You've been banned from the server `{ctx.guild.name}`.",
		colour=discord.Color.red(),
		timestamp=datetime.datetime.now()
		)

	await member.send(embed=bannedembed)

@client.command()
@commands.guild_only()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, ammount : int):
	if ammount <= 0:
		await ctx.send(f"{ctx.author.mention} Please enter a valid number (1-100)")
		return

	else:
		await ctx.channel.purge(limit=ammount + 1)

@client.command()
@commands.guild_only()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
	await member.kick(member, reason=reason)
	await ctx.send(f'Kicked {member.name}#{member.discriminator}')

@client.command()
@commands.guild_only()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	member_name, member_discriminator = member.split('#')

	for ban_entry in banned_users:
		user = ban_entry.user

		if (user.name, user.discriminator) == (member_name, member_discriminator):
			await ctx.guild.unban(user)
			await ctx.send(f"Unbanned {user.mention}.")
			return

@client.command(aliases = ["spot"])
@commands.guild_only()
async def spotify(ctx, user: discord.Member = None):
    
    user = user or ctx.author or user.id or user.name
    spot = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)
    
    if spot is None:
        await ctx.send(embed=spoterror)
        return

    embedspotify = discord.Embed(
    	title=f"{user.name}'s Now playing Song",
    	color=0x1eba10,
    	timestamp=datetime.datetime.now()
    	)
    
    embedspotify.add_field(name="Song", value=spot.title)
    embedspotify.add_field(name="Artist", value=spot.artist)
    embedspotify.add_field(name="Album", value=spot.album)
    embedspotify.add_field(name="Duration", value=spot.duration)
    embedspotify.add_field(name="track ID", value=spot.track_id)
    embedspotify.add_field(name="Listening Party ID", value=spot.party_id)

    embedspotify.set_thumbnail(url=spot.album_cover_url)

    await ctx.send(embed=embedspotify)

@client.command()
@commands.guild_only()
async def song(ctx, user: discord.Member = None):
    
    user = user or ctx.author or user.id
    spot = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)
    
    if spot is None:
        await ctx.send(embed=spoterror)
        return

    emspotify = discord.Embed(
    	title=f"{user.name}'s Now playing Song",
    	color=0x1eba10,
    	timestamp=datetime.datetime.now()
    	)

    emspotify.add_field(name="Track link", value="https://open.spotify.com/track/" + spot.track_id)
    emspotify.add_field(name="Song", value=spot.title)
    emspotify.set_image(url=spot.album_cover_url)

    await ctx.send(embed=emspotify)

@client.command()
@commands.guild_only()
async def album(ctx, user: discord.Member = None):
	
	user = user or ctx.author or user.id
	spot = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)

	if spot is None:
		await ctx.send(embed=spoterror)
		return

	albumembed = discord.Embed(
		title=f"{user.name} is listening to the album",
		colour=discord.Color.green(),
		timestamp=datetime.datetime.now()
		)
	albumembed.add_field(name="Album", value=spot.album, inline=True)
	albumembed.add_field(name="Artist", value=spot.artist, inline=True)
	albumembed.set_image(url=spot.album_cover_url)

	await ctx.send(embed=albumembed)

@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(embed=joinembed)
        break

@client.command()
@commands.guild_only()
async def timer(ctx, time: int):
   await ctx.send('Timer set for: ' + str(time) + 's')
   await asyncio.sleep(time)
   await ctx.send(f"{ctx.author.mention} Time's Up!")
   await ctx.author.send(f"{ctx.author.mention} Your timer for {time}s has ended from the server: `{ctx.author.guild.name}`")
   return

@client.command()
async def astolfo(ctx):

	async with ctx.channel.typing():
    
	    memes_submissions = reddit.subreddit('astolfo').hot()
	    post_to_pick = random.randint(1, 10)
	    for i in range(0, post_to_pick):
	        submission = next(x for x in memes_submissions if not x.stickied)

	    memeembed = discord.Embed(
	    	title=submission.title,
	    	timestamp=datetime.datetime.now()
	    	)
	    
	    memeembed.set_image(url=submission.url)
	    
	    await ctx.send(embed=memeembed)

@astolfo.error
async def astolfo_error(ctx, error):
	await ctx.send("Something went wrong, try again later.")
	return print(error)	

@client.command()
async def anime(ctx):
	
	async with ctx.channel.typing():

	    memes_submissions = reddit.subreddit('anime').hot()
	    post_to_pick = random.randint(1, 10)
	    for i in range(0, post_to_pick):
	        submission = next(x for x in memes_submissions if not x.stickied)

	    memeembed = discord.Embed(
	    	title=submission.title,
	    	timestamp=datetime.datetime.now()
	    	)
	    
	    memeembed.set_image(url=submission.url)
	    
	    await ctx.send(embed=memeembed)

@anime.error
async def anime_error(ctx, error):
	await ctx.send("Something went wrong, try again later.")
	return print(error)

@client.command()
async def serverinfo(ctx):

	async with ctx.channel.typing():
	
	    serverembed = discord.Embed(
	    
	    title=f"{ctx.guild.name}",
	    color=discord.Color.green(),
	   	timestamp=datetime.datetime.now(),
	    )
	    
	    serverembed.set_thumbnail(url=f"{ctx.guild.icon_url}")
	    serverembed.set_footer(icon_url=f"{ctx.author.guild.icon_url}", text=f"Guild ID: {ctx.guild.id}")
	    
	    serverembed.add_field(name=f'Server ID', value=f"{ctx.author.guild.id}")
	    serverembed.add_field(name=f'Owner Name', value=f"{ctx.author.guild.owner}")
	    serverembed.add_field(name=f'Server Region', value=f"{ctx.author.guild.region}")
	    serverembed.add_field(name=f'Member count', value=f"{ctx.author.guild.member_count}")
	    serverembed.add_field(name=f'Created at', value=f"{ctx.author.guild.created_at}")
	    serverembed.add_field(name=f'Nitro boosters', value=f"{ctx.author.guild.premium_subscription_count}")

	    await ctx.send(embed=serverembed)

@serverinfo.error
async def serverinfo_error(ctx, error):
	await ctx.send("Something went wrong, try again later.")
	return print(error)

@client.command()
async def waifu(ctx):
	
	async with ctx.channel.typing():
		
		memes_submissions = reddit.subreddit('Waifu').hot()
		post_to_pick = random.randint(1, 10)
		for i in range(0, post_to_pick):
		    submission = next(x for x in memes_submissions if not x.stickied)

		memeembed = discord.Embed(
			title=submission.title,
			timestamp=datetime.datetime.now()
			)
		    
		memeembed.set_image(url=submission.url)

		await ctx.send(embed=memeembed)

@client.command(aliases = ["av"])
async def avatar(ctx, *, user: discord.Member = None):
	user = user or ctx.author or user.id

	avatarembed = discord.Embed(
		title=f"{user.name} Avatar",
		color=discord.Color.green(),
		timestamp=datetime.datetime.now()
		)

	avatarembed.set_image(url=user.avatar_url)

	await ctx.send(embed=avatarembed)

'''
@client.command(aliases = ["connect"])
async def join(ctx):
	joionembed = discord.Embed(
		title=f"Connected",
		colour=discord.Color.green(),
		timestamp=datetime.datetime.now()
		)

	channel = ctx.author.voice.channel
	await ctx.send(embed=joionembed)
	await channel.connect()

@client.command(aluases = ["disonnect"])
async def leave(ctx):
	leavembed = discord.Embed(
		title="Disconnected",
		colour=discord.Color.red(),
		timestamp=datetime.datetime.now()
		)

	await ctx.voice_client.disconnect()
	await ctx.send(embed=leavembed)
'''

@client.command()
async def meme(ctx):
	await ctx.message.delete()

	async with ctx.channel.typing():

		memes_submissions = reddit.subreddit('memes' or 'meme' or 'dankmemes').hot()
		post_to_pick = random.randint(1, 10)
		for i in range(0, post_to_pick):
		    submission = next(x for x in memes_submissions if not x.stickied)

		memeembed = discord.Embed(
			title=submission.title,
			timestamp=datetime.datetime.now()
			)
		    
		memeembed.set_image(url=submission.url)
		    
		await ctx.send(embed=memeembed)

@meme.error
async def meme_error(ctx, error):
	await ctx.send("Something went wrong, try again later.")
	return print(error)

	print("Meme cog has been loaded.")

@client.command()
async def dmwaifu(ctx):
	await ctx.message.delete()

	async with ctx.channel.typing():

		memes_submissions = reddit.subreddit('waifu').hot()
		post_to_pick = random.randint(1, 10)
		for i in range(0, post_to_pick):
		    submission = next(x for x in memes_submissions if not x.stickied)

		memeembed = discord.Embed(
			title=submission.title,
			timestamp=datetime.datetime.now()
			)
		    
		memeembed.set_image(url=submission.url)
		    
		await ctx.author.send(embed=memeembed)

@client.command(aliases = ["dmeme"])
async def dmmeme(ctx):
	await ctx.message.delete()

	async with ctx.channel.typing():

		memes_submissions = reddit.subreddit('memes' or 'meme' or 'dankmemes').hot()
		post_to_pick = random.randint(1, 100)
		for i in range(0, post_to_pick):	
		    submission = next(x for x in memes_submissions if not x.stickied)

		memeembed = discord.Embed(
			title=submission.title,
			timestamp=datetime.datetime.now()
			)
		    
		memeembed.set_image(url=submission.url)
		    
		await ctx.author.send(embed=memeembed)

@client.command()
async def dmanime(ctx):
	await ctx.message.delete()

	async with ctx.channel.typing():

		memes_submissions = reddit.subreddit('Anime').hot()
		post_to_pick = random.randint(1, 100)
		for i in range(0, post_to_pick):
		    submission = next(x for x in memes_submissions if not x.stickied)

		memeembed = discord.Embed(
			title=submission.title,
			timestamp=datetime.datetime.now()
			)
		    
		memeembed.set_image(url=submission.url)
		    
		await ctx.author.send(embed=memeembed)

@client.command()
async def track(ctx, *, user: discord.Member = None):

	user = user or ctx.author or user.id
	spot = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)

	if spot is None:
		await ctx.send(f"{ctx.author.mention}, {user.name} is not listening to Spotify.")
		return

	await ctx.send(f"{ctx.author.mention}, Here!\n`{user.name}` Track: \nhttps://open.spotify.com/track/" + spot.track_id)

@client.command(aliases = ["inf"])
async def info(ctx):
	infoembed = discord.Embed(
		title="Bot Info",
		colour=discord.Color.green(),
		timestamp=datetime.datetime.now()
		)

	infoembed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}")
	infoembed.set_thumbnail(url=client.user.avatar_url)

	infoembed.add_field(name="Bot name", value=f"{client.user.name}", inline=False)
	infoembed.add_field(name="Bot discriminator", value=f"{client.user.discriminator}", inline=False)
	infoembed.add_field(name="Developer", value=f"{developer}", inline=False)
	infoembed.add_field(name="Bot ping", value=f"{round(client.latency * 1000)}ms", inline=False)
	infoembed.add_field(name="Watching", value=str(len(client.guilds)) + " Servers")

	await ctx.send(embed=infoembed)

@client.command()
async def test551(ctx):	
	test551embed = discord.Embed(
		title="test",
		timestamp=datetime.datetime.now()
		)

	await ctx.send(embed=test551embed)

@client.command()
async def gentest(ctx):
    
    genembed = discord.Embed(
        title="Minecraft NFA",
        colour=discord.Color.green(),
        timestamp=datetime.datetime.now()
        )

    with open('alts.json', 'r') as f:
        alts = json.load(f)
    
    choice = random.choice(alts)
    genembed.add_field(name="Account:", value=choice, inline=False)

    with open('alts.json', 'w') as f:
        del alts[alts.index(choice)]
        f.write(json.dumps(alts, indent=4))

    await ctx.author.send(embed=genembed)
    await ctx.send(f"{ctx.author.mention} Please check your DMs!")

@gentest.error
async def gentest_error(ctx, error):
	await ctx.send(error)
	print(error)
	raise error

@client.command()
async def raffle(ctx, *, prize):
	raffleembed = discord.Embed(
		title="New Raffle!",
		description="Prize: **{}**!\nfirst one to react with 🎉 wins!".format(prize),
		colour=discord.Color.green()
		)

	msg = await ctx.send(embed=raffleembed)

	await msg.add_reaction("🎉")

	reaction, user = await client.wait_for(
		'reaction_add',
		check=lambda reaction,
		user: reaction.emoji == '🎉')

	await user.send(f"You're the winner of **{prize}**!")
	await ctx.send(f"The winner is {user}!")

@client.command()
async def drop(ctx, *, prize):
	dropembed = discord.Embed(
		title="{} Drop!".format(prize),
		description="First one to react wins!",
		colour=discord.Color.green()
		)

	msg = await ctx.send(embed=dropembed)

	reaction, user = await client.wait_for('reaction_add')

	await ctx.send(f"{user} Reacted first!")
	await ctx.author.send(f"{user} Reacted!")

@client.command()
async def suggest(ctx, *, suggestion):

	suggestembed = discord.Embed(
		title="New Suggestion!",
		description=f"{ctx.author.name}#{ctx.author.discriminator} Suggested with `{suggestion}`"
		)

	user = client.get_user(694446165197979670)

	await user.send(embed=suggestembed)

	suggestsent = discord.Embed(
		title="Thanks for your sugestion(s)!",
		colour=discord.Color.green()
		)

	await ctx.send(f"{ctx.author.mention}")
	await ctx.send(embed=suggestsent)
	return

@suggest.error
async def suggest_error(ctx, error):
	await ctx.send(error)
	print(error)

@raffle.error
async def raffle_error(self, ctx, error):
	await ctx.send(error)
	print(error)
	raise error

@client.command()
@commands.is_owner()
async def shutdown(ctx):
	await ctx.message.delete()
	await client.close()

@client.command()
async def remind(ctx, time, *, remind):
	await ctx.send("Reminder set!")

	await asyncio.sleep(to_seconds(time))

	await ctx.author.send("Reminder! {}".format(remind))
	return

@client.command(aliases = ["request"])
async def req(ctx, *, message):
	reqembed = discord.Embed(
		title="New Request!",
		description=f"{ctx.author.name}#{ctx.author.discriminator} requested with `{suggestion}`"
		)

	user = client.get_user(694446165197979670)

	await user.send(embed=reqembed)

	reqsent = discord.Embed(
		title="Thanks for your request!",
		colour=discord.Color.green()
		)

	await ctx.send(f"{ctx.author.mention}")
	await ctx.send(embed=reqsent)
	return

@client.command(aliases = ["gay"])
async def howgay(ctx, user: discord.Member = None):
	user = user or ctx.author

	gayness = random.randint(0, 100)

	hgembed = discord.Embed(
		title="How gay",
		description=f"{user} Is {gayness}% gay",
		colour=discord.Color.green()
		)

	msg2 = await ctx.send(ctx.author.mention, embed=hgembed)
	return

	if gayness >= 50:

		await msg.delete()
		await msg2.delete()

		hgaembed = discord.Embed(
		title="How gay",
		description=f"{user} Is {gayness}% gay lol",
		colour=discord.Color.green()
		)

		await ctx.send(f'{ctx.author.mention}')
		await ctx.send(embed=hgaembed)
		return

	elif gayness == 100:

		await msg.delete()
		await msg2.delete()

		hgaembed = discord.Embed(
		title="How gay",
		description=f"{user} Is {gayness}% Gay...",
		colour=discord.Color.red()
		)

		await ctx.send(f'{ctx.author.mention}')
		await ctx.send(embed=hgaembed)
		return

@client.command()
async def helptest11(ctx):
	await ctx.send("category 1\ncategory 2\ncategory 3")

	try:
		msg = await client.wait_for('message', check=lambda message: message.author == ctx.author)

		if msg.content == '1':
			msg2 = await msg.edit('1')
			
			msg1 = await client.wait_for('message', check=lambda message: message.author == ctx.author)

			if msg.content == "return":
				await msg2.edit(msg)
				return

		elif msg.contemt == '2':
			await ctx.send('2')
			return

		elif msg.content == '3':
			await ctx.send('3')
			return

	except asyncio.TimeoutError:
		pass

@client.command()
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):

	channel = ctx.channel
	channel_position = channel.position

	new_channel = await channel.clone()
	await channel.delete()
	await new_channel.edit(position=channel_position, sync_permissions=True)
	return

@nuke.error
async def nuke_error(ctx, error):
	await ctx.send(error)
	print(error)
	raise error

@client.command()
async def emtest(ctx):
	etest = discord.Embed(
		title="none"
		)

	etest.add_field(name='Donate', value='[test](https://open.spotify.com/track/3NEuSQZbVmfQwRuDKol40Y?si=ridvNM6UTmiYYSnT0nUVJQ)')

	await ctx.send(embed=etest)

@emtest.error
async def emtest_error(ctx, error):
	await ctx.send(error)
	print(error)
	raise error

@client.command()
async def snipe(ctx, users_id: int):

	oldestMessage = None

	for channel in ctx.guild.text_channels:
		fetchMessage = await channel.history().find(lambda m: m.author.id == users_id)
		if fetchMessage is None:
			continue

		if oldestMessage is None:
			oldestMessage = fetchMessage

		else:
			if fetchMessage.created_at > oldestMessage.created_at:
				oldestMessage = fetchMessage

	if (oldestMessage is not None):
		snipeembed = discord.Embed(
			title=f"{users_id} Says",
			description=f'{oldestMessage.content}',
			colour=discord.Color.green(),
			timestamp=datetime.datetime.now()
			)
		await ctx.send(embed=snipeembed)

	else:
		await ctx.send("No message found.")

@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def bug(ctx, *, bug):
	await ctx.send(f'{ctx.author.mention} Thanks for the bug report!')

	user = await client.get_user(694446165197979670).send(f'Bug!\n{ctx.author.name}#{ctx.author.discriminator} Reported `{bug}`')
	return

@bug.error
async def bug_error(ctx, error):
	if isinstance(error, commandOnCooldown):
		await ctx.send('Cooldown Activated! Please try again in {:.2}s'.format(error.retry_after))

@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def nick(ctx, *, nick):

	await ctx.author.edit(nick=nick)

	await ctx.send(f'{ctx.author.mention}, nick has been set to {nick}')

@client.command(aliases = ['nickreset', 'unnick', 'unick'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def resetnick(ctx):

	await ctx.author.edit(nick=None)

	await ctx.send(f'{ctx.author.mention}, Your nick has been resetted')

@nick.error
async def changename_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		await ctx.send(' {} Cooldown activated! Please try again in {:.2}s'.format(ctx.author.mention, error.retry_after))
	else:
		await ctx.send(error)
		print(error)

@resetnick.error
async def resetnick_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		await ctx.send(' {} Cooldown activated! Please try again in {:.2}s'.format(ctx.author.mention, error.retry_after))
	else:
		await ctx.send(error)
		print(error)

@client.command()
async def invite(ctx):
    await ctx.send(f'{ctx.author.mention}, here! https://discord.com/api/oauth2/authorize?client_id=744429893198282832&permissions=8&scope=bot')

keep_alive()
token = os.environ.get("TOKEN")
client.run(token)
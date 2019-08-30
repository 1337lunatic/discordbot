'''primary source for what is written is this > https://www.youtube.com/playlist?list=PLW3GfRiBCHOhfVoiDZpSz8SM_HybXRPzZ
This is what i've mainly used as of 20.8.2019

"start" and "end" means that something starts or ends'''
import discord
import logging
import os
from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix = '.') #Prefix for commands
status = cycle(['.help for help', 'yeet that boi'])

@client.event
async def on_ready(): #on_ready DOESNT take anything in, but because this is in a Cog, it needs to take in "self"
	change_status.start()
	print('We have logged in as {0.user}'.format(client))

#Logs DEBUG
logger = logging.getLogger('discord') #Sets what program needs to get logged
logger.setLevel(logging.DEBUG) #Sets the level of what gets logged. Debug is the default value	
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w') #Sets the file
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')) #Formats it. other than that idk
logger.addHandler(handler) #adds a handler


@tasks.loop(seconds=50) #loop for status
async def change_status():
	await client.change_presence(activity=discord.Game(next(status)))


async def yote(ctx): #used to check if the user has perms to give role to self
	await ctx.send('hej.')
	member = ctx.message.author
	permissions = ctx.channel.permissions_for(member)
	if getattr(permissions, 'manage_messages', False):
		return True
	else:
		return False


@client.command()
async def role(ctx, role):
	member = ctx.message.author
	test = discord.utils.get(member.guild.roles, name=role)
	if await yote(ctx):
		await member.add_roles(test)
		await ctx.send(f'Role *{role}* added')
	else:
		await ctx.send('you cannot')


@client.event #prints whenever a member joins the server
async def on_member_join(member):
	await member.send('Welcome') #sends a message to user that joined the discordserver

@client.event
async def on_member_remove(member): #Member gets kicked, banned, leaves
	print(f'{member} has left a server') #prints to terminal


#This is used to load and unload cogs.
for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

@client.command()#loads a cog  
async def load(ctx, extension): #takes files in that ends with .py from the cogs folder.
	client.load_extension(f'cogs.{extension}')
	await ctx.send(f'{extension.capitalize()} loaded!') #.capitalize makes the first letter capitalized

@client.command()#unloads a cog
async def unload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')
	await ctx.send(f'{extension.capitalize()} unloaded!')

@client.command()#reloads a cog
async def reload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')
	client.load_extension(f'cogs.{extension}')
	await ctx.send(f'{extension.capitalize()} reloaded!') 


client.run('key')

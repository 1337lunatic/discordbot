import discord
import random
from discord.ext import commands

class botrespond(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def ping(self, ctx): #ctx means context
		await ctx.send(f'pong! {round(self.client.latency * 1000)}ms') #prints latency.

	@commands.command()
	async def yeet(self, ctx):
		await ctx.send('yeet!')

	@commands.command()
	async def dab(self, ctx):
		await ctx.send('***dab***') #no regrets


	@commands.command(aliases=['8ball']) #Aliases can be used to have multiple ways of calling the "_8ball"
	async def _8ball(self, ctx, *, question): # asteriks(*) is used to take in multiple arguements as one arguement from the array. - Underscore is in front of 8ball because python syntax cannot have a number in the beginning of a function
		responses = ['probably', #Array
					'meh',
					'no',
					'beep',
				 	'absolutely not.',
				 	'Don\'t ask me that'] #Backslash is used to character escape - This means use backslash to use characters plainly that otherwise would be used differently
		await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}') #Copies question from user and prints it, makes a newline, and then prints answer to text channel.
		

def setup(client):
	client.add_cog(botrespond(client))

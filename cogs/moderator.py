import discord
from discord.ext import commands

class moderator(commands.Cog):
	def __init__(self, client):
		self.client = client

	#used to delete the last x amount of messages. typically used in moderation bots - start
	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def clear(self, ctx, amount : int): #sets the amount default value to 5
		if amount <= 150: #if the amount entered is less than the limit = purge
			await ctx.channel.purge(limit=amount) # https://discordpy.readthedocs.io/en/latest/api.html#discord.TextChannel.purge documentation for purge
		else: #if amount is more than limit = deny purge
			await ctx.send('You cannot delete more than 150 messages')
			
	@clear.error #error if the user doesnt specify the amount
	async def clear_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('Please specify an amount of messages to delete')

	#kick and ban, typically used for moderation bots - Start
	@commands.command()
	async def kick(self, ctx, member : discord.Member, *, reason=None): #uses the discord module to use member.kick()
		await member.kick(reason=reason) 
		await ctx.send(f'kicked {member.mention}#')

	@commands.command() #ban hammer
	async def ban(self, ctx, member : discord.Member, *, reason=None):
		await member.ban(reason=reason) 
		await ctx.send(f'banned {member.mention}#')


	@commands.command()# unban hammer
	async def unban(self, ctx, *, member):
		banned_users = await ctx.guild.bans()
		member_name, member_discriminator = member.split('#') #splits member_name and member_discriminator with a hashtag

		for ban_entry in banned_users: #finds entries from the server 
			user = ban_entry.user #pulls banned users from the entry, and sets that as user

			if (user.name, user.discriminator) == (member_name, member_discriminator): #checks if the user is the actual user i want unbanned
				await ctx.guild.unban(user) #unbans user 
				await ctx.send(f'Unbanned {user.mention}') #prints to chat "Unbanned {user}
				return #exits the if statement


def setup(client):
	client.add_cog(moderator(client))
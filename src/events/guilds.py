import discord

from datetime import datetime as dt

from .. import utils

'''
 - on_guild_channel_create
 - on_guild_channel_delete
 - on_guild_role_create
 - on_guild_role_delete
 - guild_join
 - guild_remove
'''

async def channel_create(channel:discord.abc.GuildChannel):
	try:
		if channel.guild is None:
			return # ignore DMs
		
		log_channel = utils.discord_bot.get_channel(utils.stdout_channel_id)
		if log_channel is None:
			return

		embed = discord.Embed(
			title=f"Channel Created in {channel.guild.name}: {channel.mention}",
			colour=0x00ff00
		)
		embed.add_field(name="Type", value=channel.type)
		embed.add_field(name="Category", value=channel.category.mention if channel.category else "None")
		embed.add_field(name="Position", value=channel.position)

		embed.timestamp = dt.now(utils.timezone_here)
		await log_channel.send(embed=embed)
	except Exception as e:
		print(f"channel_create: {e}")

async def channel_delete(channel:discord.abc.GuildChannel):
	try:
		if channel.guild is None:
			return # ignore DMs
		
		log_channel = utils.discord_bot.get_channel(utils.stdout_channel_id)
		if log_channel is None:
			return

		embed = discord.Embed(
			title=f"Channel Deleted in {channel.guild.name}: `{channel.name}`",
			colour=0xff0000
		)
		embed.add_field(name="Type", value=channel.type)
		embed.add_field(name="Category", value=channel.category.mention if channel.category else "None")
		embed.add_field(name="Position", value=channel.position)

		embed.timestamp = dt.now(utils.timezone_here)
		await log_channel.send(embed=embed)
	except Exception as e:
		print(f"channel_delete: {e}")

async def role_create(role:discord.Role):
	try:
		if role.guild is None:
			return # ignore DMs
		
		log_channel = utils.discord_bot.get_channel(utils.stdout_channel_id)
		if log_channel is None:
			return

		embed = discord.Embed(
			title=f"Role Created {role.name}",
			colour=0x00ff00
		)
		embed.add_field(name="Permissions", value="\n".join([permission[0] for permission in role.permissions if permission[1]]))

		embed.timestamp = dt.now(utils.timezone_here)
		await log_channel.send(embed=embed)
	except Exception as e:
		print(f"role_create: {e}")

async def role_delete(role:discord.Role):
	try:
		if role.guild is None:
			return # ignore DMs
		
		log_channel = utils.discord_bot.get_channel(utils.stdout_channel_id)
		if log_channel is None:
			return

		embed = discord.Embed(
			title=f"Role Deleted {role.name}",
			colour=0xff0000
		)
		embed.add_field(name="Permissions", value="\n".join([permission[0] for permission in role.permissions if permission[1]]))

		embed.timestamp = dt.now(utils.timezone_here)
		await log_channel.send(embed=embed)
	except Exception as e:
		print(f"role_delete: {e}")

async def guild_join(guild:discord.Guild):
	try:
		log_channel = utils.discord_bot.get_channel(utils.stdout_channel_id)
		if log_channel is None:
			return

		embed = discord.Embed(
			title=f"Bot Added to Guild: {guild.name}",
			colour=0x00ff00
		)
		embed.add_field(name="Guild ID", value=guild.id, inline=False)
		embed.add_field(name="Member Count", value=guild.member_count, inline=False)
		embed.add_field(name="Owner", value=guild.owner.mention if guild.owner else "Unknown", inline=False)

		embed.timestamp = dt.now(utils.timezone_here)
		await log_channel.send(embed=embed)
	except Exception as e:
		print(f"guild_join: {e}")

async def guild_remove(guild:discord.Guild):
	try:
		log_channel = utils.discord_bot.get_channel(utils.stdout_channel_id)
		if log_channel is None:
			return

		embed = discord.Embed(
			title=f"Bot Removed from Guild: {guild.name}",
			colour=0xff0000
		)
		embed.add_field(name="Guild ID", value=guild.id, inline=False)
		embed.add_field(name="Member Count", value=guild.member_count, inline=False)
		embed.add_field(name="Owner", value=guild.owner.mention if guild.owner else "Unknown", inline=False)

		embed.timestamp = dt.now(utils.timezone_here)
		await log_channel.send(embed=embed)
	except Exception as e:
		print(f"guild_remove: {e}")
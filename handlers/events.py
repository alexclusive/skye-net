from discord.errors import Forbidden
import discord
from datetime import datetime as dt
import re

import handlers.utils as utils_module
import handlers.database as database_module
import handlers.helpers.bot_ping as bot_ping_module
import handlers.helpers.triggers as triggers_module
import handlers.helpers.spotify as spotify_module

async def message(message:discord.Message):
	try:
		if message.author == utils_module.discord_bot.user:
			return

		message_sent = False
		if utils_module.discord_bot.user in message.mentions:
			await bot_ping_module.handle_bot_ping(message)
			message_sent = True
	except Exception as e:
		print(f"on_message: openai interaction {e}")

	try:
		spotify_tracks = re.findall(r"https?://open\.spotify\.com/track/[a-zA-Z0-9]+", message.content)
		for link in spotify_tracks:
			embed = spotify_module.get_spotify_track_embed(link)
			if embed:
				await message.reply(embed=embed)
				message_sent = True

		spotify_album = re.findall(r"https?://open\.spotify\.com/album/[a-zA-Z0-9]+", message.content)
		for link in spotify_album:
			embed = spotify_module.get_spotify_album_embed(link)
			if embed:
				await message.reply(embed=embed)
				message_sent = True

		spotify_playlist = re.findall(r"https?://open\.spotify\.com/playlist/[a-zA-Z0-9]+", message.content)
		for link in spotify_playlist:
			embed = spotify_module.get_spotify_playlist_embed(link)
			if embed:
				await message.reply(embed=embed)
				message_sent = True
	
	except Exception as e:
		print(f"on_message: spotify embed {e}")

	try:
		opted_out_users = database_module.get_all_opt_out_users()
		if int(message.author.id) in opted_out_users:
			return
		
		await triggers_module.handle_reactions(message, utils_module.all_emojis)
		if not message_sent:
			await triggers_module.handle_triggers(message, utils_module.all_emojis)
	except Forbidden as e:
		if e.code == 90001: # blocked
			print(f"on_message: I was blocked by user {message.author} :(")
		else:
			print(f"on_message: reactions/triggers {e}")
	except Exception as e:
		print(f"on_message: reactions/triggers {e}")

async def message_deleted(message:discord.Message):
	try:
		if message.author == utils_module.discord_bot.user:
			return
		if message.guild is None:
			return # ignore DMs
		
		log_channel = message.guild.get_channel(utils_module.message_log_channel_id)
		if log_channel is None:
			log_channel = utils_module.get_default_log_channel()
			if log_channel is None:
				return

		embed = discord.Embed(
			title=f"Message Deleted in {message.channel.mention}",
			colour=0xff0000
		)
		if message.content:
			embed.add_field(name="Content", value=message.content, inline=False)
		if message.attachments:
			embed.add_field(name="Attachments", value="\n".join([attachment.url for attachment in message.attachments]), inline=False)
			
		embed.set_author(name=message.author.name, icon_url=message.author.display_avatar.url)
		embed.timestamp = message.created_at
		await log_channel.send(embed=embed)
	except Exception as e:
		print(f"on_message_delete: {e}")

async def channel_create(channel:discord.abc.GuildChannel):
	try:
		if channel.guild is None:
			return # ignore DMs
		
		log_channel = channel.guild.get_channel(utils_module.guild_log_channel_id)
		if log_channel is None:
			log_channel = utils_module.get_default_log_channel()
			if log_channel is None:
				return

		embed = discord.Embed(
			title=f"Channel Created {channel.mention}",
			colour=0x00ff00
		)
		embed.add_field(name="Type", value=channel.type)
		embed.add_field(name="Category", value=channel.category.mention if channel.category else "None")
		embed.add_field(name="Position", value=channel.position)

		embed.timestamp = dt.now(utils_module.timezone_syd)
		await log_channel.send(embed=embed)
	except Exception as e:
		print(f"channel_create: {e}")

async def channel_delete(channel:discord.abc.GuildChannel):
	try:
		if channel.guild is None:
			return # ignore DMs
		
		log_channel = channel.guild.get_channel(utils_module.guild_log_channel_id)
		if log_channel is None:
			log_channel = utils_module.get_default_log_channel()
			if log_channel is None:
				return

		embed = discord.Embed(
			title=f"Channel Deleted {channel.mention}",
			colour=0xff0000
		)
		embed.add_field(name="Type", value=channel.type)
		embed.add_field(name="Category", value=channel.category.mention if channel.category else "None")
		embed.add_field(name="Position", value=channel.position)

		embed.timestamp = dt.now(utils_module.timezone_syd)
		await log_channel.send(embed=embed)
	except Exception as e:
		print(f"channel_delete: {e}")

async def role_create(role:discord.Role):
	try:
		if role.guild is None:
			return # ignore DMs
		
		log_channel = role.guild.get_channel(utils_module.guild_log_channel_id)
		if log_channel is None:
			log_channel = utils_module.get_default_log_channel()
			if log_channel is None:
				return

		embed = discord.Embed(
			title=f"Role Created {role.mention}",
			colour=0x00ff00
		)
		embed.add_field(name="Permissions", value="\n".join([permission[0] for permission in role.permissions if permission[1]]))

		embed.timestamp = dt.now(utils_module.timezone_syd)
		await log_channel.send(embed=embed)
	except Exception as e:
		print(f"role_create: {e}")

async def role_delete(role:discord.Role):
	try:
		if role.guild is None:
			return # ignore DMs
		
		log_channel = role.guild.get_channel(utils_module.guild_log_channel_id)
		if log_channel is None:
			log_channel = utils_module.get_default_log_channel()
			if log_channel is None:
				return

		embed = discord.Embed(
			title=f"Role Deleted {role.mention}",
			colour=0xff0000
		)
		embed.add_field(name="Permissions", value="\n".join([permission[0] for permission in role.permissions if permission[1]]))

		embed.timestamp = dt.now(utils_module.timezone_syd)
		await log_channel.send(embed=embed)
	except Exception as e:
		print(f"role_delete: {e}")

async def member_join(member:discord.Member):
	try:
		if member.guild is None:
			return # ignore DMs
		
		log_channel = member.guild.get_channel(utils_module.member_log_channel_id)
		if log_channel is None:
			log_channel = utils_module.get_default_log_channel()
			if log_channel is None:
				return

		embed = discord.Embed(
			title=f"Member Join {member.mention}",
			colour=0x0000ff
		)
		embed.add_field(name="Joined At", value=member.joined_at)
		embed.add_field(name="Created At", value=member.created_at)
		embed.add_field(name="Roles", value="\n".join([role.mention for role in member.roles]))

		embed.set_author(name=member.name, icon_url=member.display_avatar.url)
		embed.timestamp = dt.now(utils_module.timezone_syd)	  
		await log_channel.send(embed=embed)
	except Exception as e:
		print(f"member_join: {e}")

async def member_remove(member:discord.Member):
	try:
		if member.guild is None:
			return # ignore DMs
		
		log_channel = member.guild.get_channel(utils_module.member_log_channel_id)
		if log_channel is None:
			log_channel = utils_module.get_default_log_channel()
			if log_channel is None:
				return

		embed = discord.Embed(
			title=f"Member Remove {member.mention}",
			colour=0xff0000
		)
		embed.add_field(name="Joined At", value=member.joined_at)
		embed.add_field(name="Created At", value=member.created_at)
		embed.add_field(name="Roles", value="\n".join([role.mention for role in member.roles]))
		embed.add_field(name="Left At", value=dt.now(utils_module.timezone_syd))

		embed.set_author(name=member.name, icon_url=member.display_avatar.url)
		embed.timestamp = dt.now(utils_module.timezone_syd)
		await log_channel.send(embed=embed)
	except Exception as e:
		print(f"member_remove: {e}")

async def member_update(before:discord.Member, after:discord.Member):
	try:
		if after.guild is None:
			return # ignore DMs
		
		log_channel = after.guild.get_channel(utils_module.member_log_channel_id)
		if log_channel is None:
			log_channel = utils_module.get_default_log_channel()
			if log_channel is None:
				return

		embed = discord.Embed(
			title=f"Member Updated: {after.nick}",
			colour=0x0000ff
		)
		if before.nick != after.nick:
			embed.add_field(name="Nickname", value=f"*Before:* {before.nick}\n*After:* {after.nick}")
		if before.roles != after.roles:
			role_added = None
			role_removed = None
			for role in before.roles:
				if role not in after.roles:
					role_removed = role
					break
			for role in after.roles:
				if role not in before.roles:
					role_added = role
					break
			if role_added:
				embed.add_field(name="Role Added", value=role_added.mention)
			if role_removed:
				embed.add_field(name="Role Removed", value=role_removed.mention)
		if before.display_avatar != after.display_avatar:
			embed.add_field(name="Avatar", value="")
			embed.set_thumbnail(url=after.display_avatar.url)

		if not embed.fields:
			return

		embed.set_author(name=before.name, icon_url=before.display_avatar.url)
		embed.timestamp = dt.now(utils_module.timezone_syd)
		await log_channel.send(embed=embed)
	except Exception as e:
		print(f"member_update: {e}")

async def member_ban(member:discord.Member):
	try:
		if member.guild is None:
			return # ignore DMs
		
		log_channel = member.guild.get_channel(utils_module.member_log_channel_id)
		if log_channel is None:
			log_channel = utils_module.get_default_log_channel()
			if log_channel is None:
				return

		embed = discord.Embed(
			title=f"Member Banned {member.mention}",
			colour=0xff0000
		)
		embed.add_field(name="Joined At", value=member.joined_at)
		embed.add_field(name="Created At", value=member.created_at)
		embed.add_field(name="Roles", value="\n".join([role.mention for role in member.roles]))
		embed.add_field(name="Banned At", value=dt.now(utils_module.timezone_syd))

		embed.set_author(name=member.name, icon_url=member.display_avatar.url)
		embed.timestamp = dt.now(utils_module.timezone_syd)
		await log_channel.send(embed=embed)
	except Exception as e:
		print(f"member_ban: {e}")
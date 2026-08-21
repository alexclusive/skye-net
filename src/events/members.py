import discord

from datetime import datetime as dt

from .. import utils

'''
 - on_member_join
 - on_member_remove
 - on_member_update
 - on_member_ban
'''

joined = "Joined At"
created = "Created At"

async def member_join(member:discord.Member):
	try:
		if member.guild is None:
			return # ignore DMs
		
		log_channel = utils.discord_bot.get_channel(utils.stdout_channel_id)
		if log_channel is None:
			return

		embed = discord.Embed(
			title=f"Member Join {member.mention}",
			colour=0x0000ff
		)
		embed.add_field(name=joined, value=utils.get_timestamp_formatted(member.joined_at.timestamp()), inline=False)
		embed.add_field(name=created, value=utils.get_timestamp_formatted(member.created_at.timestamp()), inline=False)
		embed.add_field(name="Roles", value="\n".join([role.name for role in member.roles]), inline=False)

		embed.set_author(name=member.name, icon_url=member.display_avatar.url)
		embed.timestamp = dt.now(utils.timezone_here)	  
		await log_channel.send(embed=embed)
	except Exception as e:
		print(f"member_join: {e}")

async def member_remove(member:discord.Member):
	try:
		if member.guild is None:
			return # ignore DMs
		
		log_channel = utils.discord_bot.get_channel(utils.stdout_channel_id)
		if log_channel is None:
			return
			
		leave_type = "left"
		try:
			# Check audit logs to see kicks and bans (requires View Audit Log permission)
			async for entry in member.guild.audit_logs(limit=5, action=discord.AuditLogAction.kick):
				if entry.target.id == member.id:
					leave_type = "was kicked from"
					break
			if leave_type == "left":
				async for entry in member.guild.audit_logs(limit=5, action=discord.AuditLogAction.ban):
					if entry.target.id == member.id:
						leave_type = "was banned from"
						break
		except discord.errors.Forbidden:
			# No permission to view audit logs, check the ban list (requires Ban Members permission)
			try:
				banned_users = await member.guild.bans()
				for ban_entry in banned_users:
					if ban_entry.user.id == member.id:
						leave_type = "was banned from"
						break
			except Exception as _:
				# No permission to view bans
				pass
		except Exception as e:
			print(f"member_remove: error checking audit logs {e}")

		embed = discord.Embed(
			title = f"{member.guild.name}: {member.name} ({member.display_name}) {leave_type} the server",
			colour=0xff0000,
		)
		embed.add_field(name="", value=f"{member.mention}", inline=False)
		embed.add_field(name=joined, value=utils.get_timestamp_formatted(member.joined_at.timestamp()), inline=False)
		embed.add_field(name=created, value=utils.get_timestamp_formatted(member.created_at.timestamp()), inline=False)
		embed.add_field(name="Left At", value=utils.get_timestamp_now_formatted(), inline=False)
		embed.add_field(name="Roles", value="\n".join([role.name for role in member.roles]), inline=False)

		embed.set_author(name=member.name, icon_url=member.display_avatar.url)
		embed.set_thumbnail(url=member.display_avatar.url)
		embed.timestamp = dt.now(utils.timezone_here)
		await log_channel.send(embed=embed)
	except Exception as e:
		print(f"member_remove: {e}")

async def member_update(before:discord.Member, after:discord.Member):
	try:
		if after.guild is None:
			return # ignore DMs
		
		log_channel = utils.discord_bot.get_channel(utils.stdout_channel_id)
		if log_channel is None:
			return
			
		display_name = after.nick
		if display_name is None:
			display_name = after.name

		embed = discord.Embed(
			title=f"Member Updated: {display_name}",
			colour=0x0000ff
		)
		
		if before.nick != after.nick:
			embed.add_field(name="Nickname", value=f"*Before:* {before.nick}\n*After:* {after.nick}", inline=False)

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
				embed.add_field(name="Role Added", value=role_added.name, inline=False)
			if role_removed:
				embed.add_field(name="Role Removed", value=role_removed.name, inline=False)

		if before.display_avatar != after.display_avatar:
			embed.add_field(name="Avatar", value="", inline=False)
			embed.set_thumbnail(url=after.display_avatar.url)

		if not embed.fields:
			return
		
		embed.add_field(name="", value=f"{after.mention}", inline=False)

		embed.set_author(name=before.name, icon_url=before.display_avatar.url)
		embed.timestamp = dt.now(utils.timezone_here)
		await log_channel.send(embed=embed)
	except Exception as e:
		print(f"member_update: {e}")

async def member_ban(member:discord.Member):
	try:
		if member.guild is None:
			return # ignore DMs
		
		log_channel = utils.discord_bot.get_channel(utils.stdout_channel_id)
		if log_channel is None:
			return

		embed = discord.Embed(
			title=f"Member Banned {member.mention}",
			colour=0xff0000
		)
		embed.add_field(name="", value=f"{member.mention}", inline=False)
		embed.add_field(name=joined, value=utils.get_timestamp_formatted(member.joined_at.timestamp()), inline=False)
		embed.add_field(name=created, value=utils.get_timestamp_formatted(member.created_at.timestamp()), inline=False)
		embed.add_field(name="Banned At", value=utils.get_timestamp_now_formatted(), inline=False)
		embed.add_field(name="Roles", value="\n".join([role.name for role in member.roles]), inline=False)
		embed.add_field(name="Banned By", value=member.guild.me.mention, inline=False)

		embed.set_author(name=member.name, icon_url=member.display_avatar.url)
		embed.set_thumbnail(url=member.display_avatar.url)
		embed.timestamp = dt.now(utils.timezone_here)
		await log_channel.send(embed=embed)
	except Exception as e:
		print(f"member_ban: {e}")
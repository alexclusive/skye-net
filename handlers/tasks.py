from datetime import datetime as dt
import discord

import handlers.utils as utils_module
import handlers.database as database_module

async def daily_tasks():
	'''
		Get last time daily tasks were run from database (if not exist or more than 1 day ago, run daily tasks)
		Go through list of each guild member
			If they have the welcomed role and do not have the trusted role:
				Get the time they joined the server
				If they have been in the server for more than utils_module.trusted_time_days days:
					Add the trusted role to the member
	'''
	run_task = False

	last_daily_task_time = database_module.get_last_daily_task_time()
	if not last_daily_task_time:
		run_task = True
	else:
		time_now = dt.now()
		time_diff = time_now - last_daily_task_time
		if time_diff.days >= 1:
			run_task = True

	if run_task:
		print(f"daily_tasks: Last run {last_daily_task_time}, running now")
		guild = utils_module.discord_bot.get_guild(utils_module.guild_id)
		if not utils_module.guild_id:
			print("daily_tasks: Guild not found.")
			return
		
		welcomed_role = guild.get_role(utils_module.welcomed_role_id)
		if not welcomed_role:
			print("daily_tasks: Welcomed role not found.")
			return
		
		trusted_role = guild.get_role(utils_module.trusted_role_id)
		if not trusted_role:
			print("daily_tasks: Trusted role not found.")
			return
		
		print("daily_tasks: Adding trusted roles")
		await add_trusted_roles(guild, welcomed_role, trusted_role)
		database_module.insert_daily_task_time()

async def add_trusted_roles(guild:discord.Guild, welcomed_role:discord.Role, trusted_role:discord.Role):
	time_now = dt.now()
	for member in guild.members:
		if welcomed_role in member.roles and trusted_role not in member.roles:
			days_in_server = (time_now - member.joined_at).days
			if days_in_server > utils_module.trusted_time_days:
				await member.add_roles(trusted_role)
				print(f"Added {trusted_role.name} role to {member.name}")
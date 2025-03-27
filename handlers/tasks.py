from datetime import datetime as dt
from datetime import timezone, time
from discord.ext import tasks

import handlers.utils as utils_module
import handlers.database as database_module

task_start_time = time(19, 0) # utc time

async def tasks_on_ready():
	if not add_trusted_roles_task.is_running():
		add_trusted_roles_task.start()

@tasks.loop(time=task_start_time)
async def add_trusted_roles_task():
	'''
		Get last time daily tasks were run from database (if not exist or more than 1 day ago, run daily tasks)
		Go through list of each guild member
			If they have the welcomed role and do not have the trusted role:
				Get the time they joined the server
				If they have been in the server for more than utils_module.trusted_time_days days:
					Add the trusted role to the member
	'''
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
	
	try:
		time_now = dt.now(timezone.utc)
		for member in guild.members:
			if welcomed_role in member.roles and trusted_role not in member.roles:
				days_in_server = (time_now - member.joined_at).days
				if days_in_server > utils_module.trusted_time_days:
					await member.add_roles(trusted_role)
					print(f"Added <@{trusted_role.id}> role to @{member.id}")
	except Exception as e:
		print(f"add_trusted_roles: {e}")

	database_module.insert_daily_task_time()
import datetime

import handlers.utils as utils_module

async def daily_tasks():
	'''
		Go through list of all users in the server and if they have been in the server for over one month,
		give them a role (utils_module.trusted_role) if they have the welcomed_role.
	'''
	return
	guild = utils_module.discord_bot.get_guild(utils_module.guild_id)
	if not utils_module.guild_id:
		print("daily_tasks: Guild not found.")
		return
	
	welcomed_role = guild.get_role(utils_module.welcomed_role_id)
	if not welcomed_role:
		print("daily_tasks: Role not found.")
		return
	
	trusted_role = guild.get_role(utils_module.trusted_role_id)
	if not trusted_role:
		print("daily_tasks: Role not found.")
		return
	
	for member in guild.members:
		time_joined = member.joined_at
		if time_joined and welcomed_role in member.roles:
			time_now = datetime.datetime.now()
			days_in_server = (time_now - time_joined).days
			if days_in_server > utils_module.trusted_days:
				await member.add_roles(trusted_role)
				print(f"Added {trusted_role.name} role to {member.name}.")
from datetime import datetime as dt
from datetime import timezone, time, timedelta
from discord.ext import tasks
from discord import AuditLogEntry
import asyncio

import handlers.utils as utils_module
import handlers.database as database_module

trusted_roles_start_time = time(19, 0) # utc time
audit_log_start_time = time(20, 0) # utc time

async def tasks_on_ready():
	if not add_trusted_roles_task.is_running():
		add_trusted_roles_task.start()
	if not audit_log_task.is_running():
		audit_log_task.start()

@tasks.loop(time=trusted_roles_start_time)
async def add_trusted_roles_task():
	'''
		Get last time daily tasks were run from database (if not exist or more than 1 day ago, run daily tasks)
		Go through list of each guild member
			If they have the welcomed role and do not have the trusted role:
				Get the time they joined the server
				If they have been in the server for more than utils_module.trusted_time_days days:
					Add the trusted role to the member
	'''
	print("Running add_trusted_roles_task...")

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

@tasks.loop(time=audit_log_start_time)
async def audit_log_task():
	'''
		Get a list of all audit logs from the last 24 hours.
		Go through each audit log entry
			If the action was performed by any user with the bot role:
				Ignore the action
			If the action was any of the following, ignore the action:
				- any channel updates (deleted, created, updated)
				- any event updates (deleted, created, updated)
				- any thread updates (deleted, created, updated)
				- any emoji updates (deleted, created, updated)
				- any integration updates (deleted, created, updated)
				- any sticker updates (deleted, created, updated)
				- any soundboard updates (deleted, created, updated)
				- any stage updates (deleted, created, updated)
				- any voice channel status update (deleted, created)
				- disconnect member
				- add bot
			If the action was performed by any user with the admin role:
				Add to a list of audit logs from admins
		Go through list of audit logs from admins
			Sort the list by date
			For each member with the admin role (that has an item recorded)
				Go through the list of audit logs from admins
					If the action was performed by the member:
						Print the action with details on the action
	'''
	print("Running audit_log_task...")

	guild = utils_module.discord_bot.get_guild(utils_module.guild_id)
	if not utils_module.guild_id:
		print("audit_log_task: Guild not found.")
		return

	bot_role = guild.get_role(utils_module.bot_role_id)
	if not bot_role:
		print("audit_log_task: Bot role not found.")
		return

	admin_role = guild.get_role(utils_module.admin_role_id)
	if not admin_role:
		print("audit_log_task: Admin role not found.")
		return

	try:
		time_now = dt.now(timezone.utc)
		time_24_hours_ago = time_now - timedelta(days=1)
		audit_logs = [entry async for entry in guild.audit_logs(after=time_24_hours_ago)]

		admin_logs:list[AuditLogEntry] = []
		ignored_actions = [
			"channel_create", "channel_delete", "channel_update",
			"event_create", "event_delete", "event_update",
			"thread_create", "thread_delete", "thread_update",
			"emoji_create", "emoji_delete", "emoji_update",
			"integration_create", "integration_delete", "integration_update",
			"sticker_create", "sticker_delete", "sticker_update",
			"soundboard_create", "soundboard_delete", "soundboard_update",
			"stage_create", "stage_delete", "stage_update",
			"voice_channel_create", "voice_channel_delete",
			"member_disconnect", "bot_add"
		]
		
		for entry in audit_logs:
			if bot_role in entry.user.roles:
				continue
			if entry.action.name in ignored_actions:
				continue
			if admin_role in entry.user.roles:
				admin_logs.append(entry)
		
		admin_logs.sort(key=lambda log: log.created_at)

		for admin in [member for member in guild.members if admin_role in member.roles]:
			this_admin_logs = [log for log in admin_logs if log.user == admin]
			if len(this_admin_logs) == 0:
				continue
			details = [f"Audit logs for admin: {admin.name}:"]
			for log in this_admin_logs:
				timestamp = int(log.created_at.timestamp())
				detail_text = f"\n- `{log.action.name}` on {log.target} at <t:{timestamp}:f> (<t:{timestamp}:R>)"
				if log.reason:
					detail_text += f"\nDetails: {log.reason}"
				details.append(detail_text)
			print("".join(details))
			await asyncio.sleep(0.2) # Avoid rate limiting

	except Exception as e:
		print(f"audit_log_task: {e}")
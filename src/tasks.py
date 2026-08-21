import asyncio
import bs4
import csv
import io
import os
import urllib.request

from datetime import datetime as dt
from datetime import timezone, time, timedelta
from discord import AuditLogEntry
from discord.ext import tasks

from . import database_module as database
from . import logger
from . import utils
from .handlers import facts

running_task_log_string = "Running task."

# UTC times
backup_logs_start_time = time(0, 0)
trusted_roles_start_time = time(19, 0)
audit_log_start_time = time(20, 0)

csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database", "train_info.csv")

def tasks_on_ready():
	logger.log(logger.LOG_SETUP, "Ensuring tasks are running.")
	if not backup_logs_task.is_running():
		backup_logs_task.start()

	if not add_trusted_roles_task.is_running():
		add_trusted_roles_task.start()
	if not audit_log_task.is_running():
		audit_log_task.start()
	if not read_train_info_task.is_running():
		read_train_info_task.start()

	facts.read_csv_train_info()

@tasks.loop(time=backup_logs_start_time)
async def backup_logs_task():
	'''
		Backup the logs from utils_module.log_file_path to a dated file in the same directory
		Stucture should be:
			<log_file_path>/YYYY/MM/DD.log
	'''
	logger.log(logger.LOG_SETUP, running_task_log_string)
	try:
		# make year and month directories if they don't exist
		now = dt.now(utils.timezone_here)
		year_dir = now.strftime("%Y")
		month_dir = now.strftime("%m")
		full_path = os.path.join(os.path.dirname(utils.log_file_path), year_dir, month_dir)

		if not os.path.exists(full_path):
			os.makedirs(full_path)
			
		day_file = now.strftime("%d.log")
		full_path = os.path.join(full_path, day_file)

		copy_success = logger.copy_log_file(full_path)
		if copy_success:
			logger.clear_log_file()
			logger.log(logger.LOG_SETUP, f"Logs backed up to {full_path}")
		else:
			logger.log(logger.LOG_INFO, "Couldn't copy log file.")
	except Exception as e:
		logger.log(logger.LOG_INFO, f"Error backing up logs: {e}")

@tasks.loop(time=trusted_roles_start_time)
async def add_trusted_roles_task():
	'''
		Get last time daily tasks were run from database (if not exist or more than 1 day ago, run daily tasks)
		Go through list of each guild member
			If they have the welcomed role and do not have the trusted role:
				Get the time they joined the server
				If they have been in the server for more than utils.trusted_time_days days:
					Add the trusted role to the member
	'''
	logger.log(logger.LOG_SETUP, running_task_log_string)

	guild = utils.discord_bot.get_guild(utils.guild_id)
	if not utils.guild_id:
		logger.log(logger.LOG_SETUP, "Guild not found.")
		return
	
	welcomed_role = guild.get_role(utils.welcomed_role_id)
	if not welcomed_role:
		logger.log(logger.LOG_SETUP, "Welcomed role not found.")
		return
	
	trusted_role = guild.get_role(utils.trusted_role_id)
	if not trusted_role:
		logger.log(logger.LOG_SETUP, "Trusted role not found.")
		return
	
	trusted_added = 0
	welcomed_added = 0

	try:
		time_now = dt.now(timezone.utc)
		for member in guild.members:
			if welcomed_role in member.roles and trusted_role not in member.roles:
				days_in_server = (time_now - member.joined_at).days
				if days_in_server > utils.trusted_time_days:
					await member.add_roles(trusted_role)
					print(f"Added {trusted_role.name} role to {member.name} ({member.nick})")
					trusted_added += 1
					logger.log(logger.LOG_EXTRA_DETAIL, f"Added <@{trusted_role.id}> role to @{member.id}")
			elif welcomed_role not in member.roles and trusted_role not in member.roles:
				days_in_server = (time_now - member.joined_at).days
				if days_in_server > (utils.trusted_time_days // 2):
					await member.add_roles(welcomed_role)
					print(f"Added {welcomed_role.name} role to {member.name} ({member.nick})")
					welcomed_added += 1
					logger.log(logger.LOG_EXTRA_DETAIL, f"Added {welcomed_role.name} role to {member.name} ({member.nick}, {member.id})")
	except Exception as e:
		print(f"add_trusted_roles: {e}")

	database.insert_daily_task_time()
	logger.log(logger.LOG_SETUP, f"Added {trusted_added} trusted roles and {welcomed_added} welcomed roles.")

@tasks.loop(time=audit_log_start_time)
async def audit_log_task(days_to_check:int=1):
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
	logger.log(logger.LOG_SETUP, running_task_log_string)

	guild = utils.discord_bot.get_guild(utils.guild_id)
	if not utils.guild_id:
		logger.log(logger.LOG_SETUP, "Guild not found.")
		return

	bot_role = guild.get_role(utils.bot_role_id)
	if not bot_role:
		logger.log(logger.LOG_SETUP, "Bot role not found.")
		return

	admin_role = guild.get_role(utils.admin_role_id)
	if not admin_role:
		logger.log(logger.LOG_SETUP, "Admin role not found.")
		return

	try:
		time_now = dt.now(timezone.utc)
		time_24_hours_ago = time_now - timedelta(days=days_to_check)
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
			if entry.user is None:
				continue
			if entry.action.name in ignored_actions:
				continue
			
			acting_member = guild.get_member(entry.user.id)
			if acting_member is None:
				try:
					acting_member = await guild.fetch_member(entry.user.id)
				except Exception:
					continue
				
			if bot_role in acting_member.roles:
				continue
			if admin_role in acting_member.roles:
				admin_logs.append(entry)

		admin_logs.sort(key=lambda log: log.created_at)
		logger.log(logger.LOG_DETAIL, f"Found {len(admin_logs)} admin logs.")

		for admin in [member for member in guild.members if admin_role in member.roles]:
			# log.user may be a User object; compare by id to be safe
			this_admin_logs = [log for log in admin_logs if log.user and getattr(log.user, 'id', None) == admin.id]
			if len(this_admin_logs) == 0:
				continue
			details = [f"Audit logs for admin: {admin.name}:"]
			for log in this_admin_logs:
				logger.log(logger.LOG_INFO, f"Checking logs for admin {admin.name}.")
				timestamp = int(log.created_at.timestamp())
				detail_text = f"\n- `{log.action.name}` on {log.target} at <t:{timestamp}:f> (<t:{timestamp}:R>)"
				if log.action.value:
					detail_text += f"\nValue: {log.action.value}"
				if log.reason:
					detail_text += f"\nDetails: {log.reason}"
				details.append(detail_text)
			print("".join(details))
			await asyncio.sleep(0.2) # Avoid rate limiting
			
		logger.log(logger.LOG_EXTRA_DETAIL, "Checked all admin logs.")

	except Exception as e:
		print(f"audit_log_task: {e}")

@tasks.loop(hours=7 * 24) # Once a week after first run
async def read_train_info_task():
	'''
		Read train information from the nswtrains fandom page https://nswtrains.fandom.com/wiki/List_of_Sydney_Trains/NSW_TrainLink_fleets
		1) Get the html table from the website
		2) Convert the html table into a csv file (train_info.csv)
		3) Read the csv into local data structure
	'''
	logger.log(logger.LOG_SETUP, running_task_log_string)

	try:
		url = "https://nswtrains.fandom.com/wiki/List_of_Sydney_Trains/NSW_TrainLink_fleets"
		request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

		with urllib.request.urlopen(request) as response:
			soup = bs4.BeautifulSoup(response.read(), "html.parser")

		table = soup.find("table", class_="wikitable")
		if table is None:
			logger.log(logger.LOG_SETUP, f"Unable to find train info table from {url}")
			print("Could not find a wikitable on the wiki page")
			return

		html = str(table)
		logger.log(logger.LOG_INFO, f"Successfully grabbed html table from {url}")

		soup = bs4.BeautifulSoup(html, "html.parser")
		table = soup.find("table", class_="wikitable")
		if table is None:
			logger.log(logger.LOG_SETUP, "Unable to parse table for train info")
			return

		def clean_text(cell):
			return " ".join(cell.get_text(" ", strip=True).replace("\u00a0", " ").split())

		rows = [row for row in table.select("tbody > tr") if not row.select("th")]
		records = []
		carried_over = {}

		for row in rows:
			cells = iter(row.select("td"))
			record = []
			column = 0

			while True:
				if column in carried_over:
					rows_left, text = carried_over[column]
					if rows_left == 1:
						del carried_over[column]
					else:
						carried_over[column][0] -= 1
				else:
					cell = next(cells, None)
					if cell is None:
						break
					text = clean_text(cell)
					rowspan = int(cell.get("rowspan", 1))
					if rowspan > 1:
						carried_over[column] = [rowspan - 1, text]

				record.append(text)
				column += 1

			while len(record) < 5:
				record.append("")
			records.append(record[:5])

		output = io.StringIO(newline="")
		writer = csv.writer(output, lineterminator="\n")
		writer.writerows(records)
		csv_data = output.getvalue()

		with open(utils.csv_file, "w", encoding="utf-8", newline="") as file:
			file.write(csv_data)

		logger.log(logger.LOG_INFO, "Successfully parsed html into csv")
	except Exception as e:
		logger.log(logger.LOG_INFO, f"Error reading train info: {e}")

	facts.read_csv_train_info()

@read_train_info_task.before_loop
async def before_read_train_info_task():
	# Run Sundays 21:00UTC
	await utils.discord_bot.wait_until_ready()
	now = dt.now(timezone.utc)
	next_run = now.replace(hour=21, minute=0, second=0, microsecond=0)
	days_until_sunday = (6 - now.weekday()) % 7
	next_run += timedelta(days=days_until_sunday)
	if next_run <= now:
		next_run += timedelta(days=7)
	await asyncio.sleep((next_run - now).total_seconds())
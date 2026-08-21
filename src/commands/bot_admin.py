import discord
import os
import platform
import signal
import sys

from .. import commands_module as commands
from .. import logger
from .. import tasks
from .. import utils
from ..handlers import machine as machine_handler

'''
 - die [Owner]
 - set_debug_level [Owner]
 - send_as_bot [Owner]
 - info [Owner]
 - force_trusted_roles [Owner]
 - force_audit_log [Owner]
 - force_reread_train_info [Owner]
 - run_test [Owner]
'''

@utils.discord_bot.tree.command(description="[Owner] Shutdown the bot")
@discord.app_commands.default_permissions()
@commands.owner_only()
async def die(interaction:discord.Interaction):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_owner(interaction):
		await interaction.followup.send(commands.nice_try)
		return
	
	try:
		logger.log(logger.LOG_SETUP, "Shutting down...")
		await interaction.followup.send("Going to sleep... Goodnight!")
		await utils.discord_bot.close()
		utils.received_shutdown = True

		if platform.system() == "Windows":
			os.kill(os.getpid(), signal.SIGTERM)
		else:
			os.kill(os.getpid(), signal.SIGKILL)
	except Exception as e:
		print(f"Error shutting down bot: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@discord.app_commands.describe(
	level="Debug level (0-3)"
)
@utils.discord_bot.tree.command(description="[Owner] Set debug level (0-3)")
@discord.app_commands.default_permissions()
@commands.owner_only()
async def set_debug_level(interaction:discord.Interaction, level:int=0):
	await interaction.response.defer(ephemeral=True)
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_owner(interaction):
		await interaction.followup.send(commands.nice_try)
		return
	
	try:
		if level < logger.LOG_SETUP or level > logger.LOG_EXTRA_DETAIL:
			await interaction.followup.send(f"Debug level must be between {logger.LOG_SETUP} and {logger.LOG_EXTRA_DETAIL}")
			return
		logger.debug_level = level
		await interaction.followup.send(f"Debug level set to {level}")
	except Exception as e:
		print(f"Error setting debug level: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@discord.app_commands.describe(
	channel_id="Channel ID to send to",
	server_id="Server ID to send to",
	message="Message content"
)
@utils.discord_bot.tree.command(description="[Owner] Send message as Skye-net")
@discord.app_commands.default_permissions()
@commands.owner_only()
async def send_as_bot(interaction:discord.Interaction, channel_id:str, server_id:str, message:str):
	await interaction.response.defer(ephemeral=True)
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_owner(interaction):
		await interaction.followup.send(commands.nice_try)
		return

	server = utils.discord_bot.get_guild(int(server_id))
	if not server:
		await interaction.followup.send("Invalid server ID", ephemeral=True)
		return
	channel = server.get_channel(int(channel_id))
	if not channel:
		await interaction.followup.send("Invalid channel ID", ephemeral=True)
		return
	
	try:
		await channel.send(message)
		await interaction.followup.send(f"Message sent to {channel.mention}:\n{message}")
	except Exception as e:
		logger.log(logger.LOG_INFO, f"Error sending message as bot: {e}")
		await interaction.followup.send(f"Error sending message: {e}")

@utils.discord_bot.tree.command(description="[Owner] Get bot info and system specs")
@discord.app_commands.default_permissions()
@commands.owner_only()
async def info(interaction:discord.Interaction):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_owner(interaction):
		await interaction.followup.send(commands.nice_try)
		return

	python_version = sys.version.split()[0]
	discord_version = discord.__version__

	system_os = platform.platform()
	system_uname = platform.uname()
	system_arch = platform.machine()
	system_processor = platform.processor()

	cpu_usage = machine_handler.get_cpu_usage()
	memory_usage = machine_handler.get_memory_usage()
	swap_memory_usage = machine_handler.get_swap_memory_usage()
	drive_usage = machine_handler.get_disk_usage()
	
	discord_info = f"Number of Servers: {len(utils.discord_bot.guilds)}\n"
	code_info = f"[GitHub Repository](https://github.com/alexclusive/skye-net)\nPython Version: {python_version}\nDiscord.py Version: {discord_version}"
	system_info = f"OS: {system_os}\nSystem: {system_uname.system}\nNode Name: {system_uname.node}\nRelease: {system_uname.release}\nVersion: {system_uname.version}\nArchitecture: {system_arch}\nProcessor: {system_processor}"
	nas_info = f"CPU Usage: {cpu_usage}\nMemory Usage: {memory_usage}\nSwap Usage: {swap_memory_usage}"
	drive_info = f"{drive_usage}"

	embed = discord.Embed(title="Bot Info", colour=0xffffff)
	embed.add_field(name="Discord Info", value=discord_info, inline=False)
	embed.add_field(name="Code Info", value=code_info, inline=False)
	embed.add_field(name="System Specs", value=system_info, inline=False)
	embed.add_field(name="System Info", value=nas_info, inline=False)
	embed.add_field(name="Drive Info", value=drive_info, inline=False)

	owner = await utils.discord_bot.fetch_user(utils.owner_id)
	embed.set_footer(text=f"Owner: {owner} ({owner.id})")
	
	await interaction.followup.send(embed=embed)

@utils.discord_bot.tree.command(description="[Owner] Force trusted roles task")
@discord.app_commands.default_permissions()
@commands.owner_only()
async def force_trusted_roles(interaction:discord.Interaction):
	await interaction.response.defer(ephemeral=True)
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_owner(interaction):
		await interaction.followup.send(commands.nice_try)
		return

	try:
		await tasks.add_trusted_roles_task()
		await interaction.followup.send("Forced trusted roles task")
	except Exception as e:
		print(f"Error forcing trusted roles: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@discord.app_commands.describe(
	days_to_check="Number of days to check back in the audit log (default 1)"
)
@utils.discord_bot.tree.command(description="[Owner] Force audit log check")
@discord.app_commands.default_permissions()
@commands.owner_only()
async def force_audit_log(interaction:discord.Interaction, days_to_check:int=1):
	await interaction.response.defer(ephemeral=True)
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_owner(interaction):
		await interaction.followup.send(commands.nice_try)
		return

	try:
		await tasks.audit_log_task(days_to_check)
		await interaction.followup.send("Forced audit log task")
	except Exception as e:
		print(f"Error forcing audit log: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@utils.discord_bot.tree.command(description="[Owner] Reread train info html")
@discord.app_commands.default_permissions()
@commands.owner_only()
async def force_reread_train_info(interaction:discord.Interaction):
	await interaction.response.defer(ephemeral=True)
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_owner(interaction):
		await interaction.followup.send(commands.nice_try)
		return

	try:
		await tasks.read_train_info_task()
		await interaction.followup.send("Finished rereading train info html and updating train sets")
	except Exception as e:
		print(f"Error forcing reread train info: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@utils.discord_bot.tree.command(description="[Owner] Run a test command")
@discord.app_commands.default_permissions() # No perms, set up in on_ready
@commands.owner_only()
async def run_test(interaction:discord.Interaction):
	await interaction.response.defer(ephemeral=True)
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_owner(interaction):
		await interaction.followup.send(commands.nice_try)
		return

	try:
		# Put test command here, so you don't have to restart discord every time to test a new function
		await interaction.followup.send("Test command DONE")
	except Exception as e:
		print(f"Error running test: {e}")
		await interaction.followup.send(commands.something_went_wrong)

commands.owner_commands_names.append("die")
commands.owner_commands_names.append("set_debug_level")
commands.owner_commands_names.append("send_as_bot")
commands.owner_commands_names.append("info")
commands.owner_commands_names.append("force_trusted_roles")
commands.owner_commands_names.append("force_audit_log")
commands.owner_commands_names.append("force_reread_train_info")
commands.owner_commands_names.append("run_test")
commands.owner_commands.append(die)
commands.owner_commands.append(set_debug_level)
commands.owner_commands.append(send_as_bot)
commands.owner_commands.append(info)
commands.owner_commands.append(force_trusted_roles)
commands.owner_commands.append(force_audit_log)
commands.owner_commands.append(force_reread_train_info)
commands.owner_commands.append(run_test)
import discord

from .. import commands_module as commands
from .. import database_module as database
from .. import logger
from .. import utils

'''
 - set_prompt
 - block_user [Admin]
 - unblock_user [Admin]
 - get_blockned_users [Owner]
'''

@discord.app_commands.describe(
	prompt="New prompt"
)
@utils.discord_bot.tree.command(description="Set the bot's prompt")
async def set_prompt(interaction:discord.Interaction, prompt:str):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)

	try:
		utils.set_current_prompt(prompt)
		database.insert_prompt(prompt, interaction.user.id)
		await interaction.followup.send(f"Prompt set to '{prompt}'")
	except Exception as e:
		print(f"Error setting prompt: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@discord.app_commands.describe(
	user_id="User ID to block from bot interactions"
)
@utils.discord_bot.tree.command(description="[Admin] Block a user from certain bot interactions")
@discord.app_commands.default_permissions(administrator=True)
@commands.admin_only()
async def block_user(interaction:discord.Interaction, user_id:discord.User):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_admin(interaction):
		await interaction.followup.send(commands.nice_try)
		return

	try:
		database.block_user(user_id)
		await interaction.followup.send(f"User {user_id} blocked")
	except Exception as e:
		print(f"Error blocking user: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@discord.app_commands.describe(
	user_id="User ID to unblock from bot interactions"
)
@utils.discord_bot.tree.command(description="[Admin] Unblock a user from certain bot interactions")
@discord.app_commands.default_permissions(administrator=True)
@commands.admin_only()
async def unblock_user(interaction:discord.Interaction, user_id:discord.User):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_admin(interaction):
		await interaction.followup.send(commands.nice_try)
		return

	try:
		database.unblock_user(user_id)
		await interaction.followup.send(f"User {user_id} unblockned")
	except Exception as e:
		print(f"Error unblockning user: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@utils.discord_bot.tree.command(description="[Owner] Get users blockned from certain bot interactions")
@discord.app_commands.default_permissions(administrator=True)
@commands.owner_only()
async def get_blockned_users(interaction:discord.Interaction):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_owner(interaction):
		await interaction.followup.send(commands.nice_try)
		return

	try:
		blockned_users = database.get_all_blocked_users()
		await interaction.followup.send(f"Blocked users: {blockned_users}")
	except Exception as e:
		print(f"Error getting blockned users: {e}")
		await interaction.followup.send(commands.something_went_wrong)
		
commands.owner_commands_names.append("get_blockned_users")
commands.owner_commands.append(get_blockned_users)
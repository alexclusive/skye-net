import discord

from .. import commands_module as commands
from .. import database_module as database
from .. import logger
from .. import utils

'''
 - set_prompt
'''

@discord.app_commands.describe(
	prompt="New prompt"
)
@utils.discord_bot.tree.command(description="Set the bot's prompt")
async def set_prompt(interaction:discord.Interaction, prompt:str):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	
	if database.is_user_blocked(interaction.user.id):
		await interaction.followup.send(commands.must_be_guild_member)
		logger.log(logger.LOG_DETAIL, f"User {interaction.user.display_name}({interaction.user.id}) is blocked from using this command, aborting")
		return

	try:
		utils.set_current_prompt(prompt)
		database.insert_prompt(prompt, interaction.user.id)
		await interaction.followup.send(f"Prompt set to '{prompt}'")
	except Exception as e:
		print(f"Error setting prompt: {e}")
		await interaction.followup.send(commands.something_went_wrong)
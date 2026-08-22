import discord

from .. import commands_module as commands
from .. import database_module as database
from .. import logger
from .. import utils
from ..handlers import etymology as etymology_handler

'''
 - ping
 - etymology
'''

@utils.discord_bot.tree.command(description="Check the bot's ping")
async def ping(interaction:discord.Interaction):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	try:
		latency = round(utils.discord_bot.latency * 1000)
		await interaction.followup.send(f"Ponged your ping in {latency}ms")
	except Exception as e:
		print(f"Error getting ping: {e}")
		logger.log(logger.LOG_INFO, f"Error getting ping: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@discord.app_commands.describe(
	argument="Word or phrase to check the etymology of"
)
@utils.discord_bot.tree.command(description="Get the etymology of a word")
async def etymology(interaction:discord.Interaction, argument:str):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	
	if database.is_user_blocked(interaction.user.id):
		await interaction.followup.send(commands.must_be_guild_member)
		logger.log(logger.LOG_DETAIL, f"User {interaction.user.display_name}({interaction.user.id}) is blocked from using this command, aborting")
		return
	
	try:
		logger.log(logger.LOG_EXTRA_DETAIL, f"Getting etymology for {argument}")
		await interaction.followup.send(etymology_handler.get_etymology(argument))
	except Exception as e:
		print(f"Error getting etymology: {e}")
		logger.log(logger.LOG_INFO, f"Error getting etymology: {e}")
		await interaction.followup.send(commands.something_went_wrong)
import discord

from .. import commands_module as commands
from .. import logger
from .. import utils

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
		await interaction.followup.send(commands.something_went_wrong)

@discord.app_commands.describe(
	argument="Word or phrase to check the etymology of"
)
@utils.discord_bot.tree.command(description="Get the etymology of a word")
async def etymology(interaction:discord.Interaction, argument:str):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	try:
		await interaction.followup.send(etymology.get_etymology(argument))
	except Exception as e:
		print(f"Error getting etymology: {e}")
		await interaction.followup.send(commands.something_went_wrong)
import discord

from .. import commands_module as commands
from .. import database_module as database
from .. import logger
from .. import utils
from ..handlers import facts as facts_handler

'''
 - number_fact
 - update_number_fact [Admin]
 - append_number_fact [Admin]
 - remove_number_fact [Admin]
'''

@discord.app_commands.describe(
	number="Number to find a fun fact about"
)
@utils.discord_bot.tree.command(description="Get a fun fact about a number")
async def number_fact(interaction:discord.Interaction, number:int):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	
	if database.is_user_blocked(interaction.user.id):
		await interaction.followup.send(commands.must_be_guild_member)
		logger.log(logger.LOG_DETAIL, f"User {interaction.user.display_name}({interaction.user.id}) is blocked from using this command, aborting")
		return
	
	try:
		logger.log(logger.LOG_EXTRA_DETAIL, f"Getting fact for {number}")
		facts_response = facts_handler.get_facts(number)
		await interaction.followup.send(facts_response)
	except Exception as e:
		print(f"Error getting number fact: {e}")
		logger.log(logger.LOG_INFO, f"Error getting number fact: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@discord.app_commands.describe(
	number="Number to update the fun fact for"
)
@utils.discord_bot.tree.command(description="[Admin] Update the fun fact for a number")
@discord.app_commands.default_permissions(administrator=True)
@commands.admin_only()
async def update_number_fact(interaction:discord.Interaction, number:int, fact:str):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_admin(interaction):
		await interaction.followup.send(commands.nice_try)
		return

	try:
		logger.log(logger.LOG_DETAIL, f"Updating fact for {number} to '{fact}'")
		database.update_number_fact(number, fact)
		await interaction.followup.send(f"Fact for number {number} updated to {fact}")
	except Exception as e:
		print(f"Error updating number fact: {e}")
		logger.log(logger.LOG_INFO, f"Error updating number fact: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@discord.app_commands.describe(
	number="Number to append the fun fact for"
)
@utils.discord_bot.tree.command(description="[Admin] Append to the fun fact for a number")
@discord.app_commands.default_permissions(administrator=True)
@commands.admin_only()
async def append_number_fact(interaction:discord.Interaction, number:int, fact:str):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_admin(interaction):
		await interaction.followup.send(commands.nice_try)
		return

	try:
		logger.log(logger.LOG_DETAIL, f"Appending '{fact}' to number {number}")
		database.append_number_fact(number, fact)
		await interaction.followup.send(f"Fact appended for number {number}! Fact is now: {database.get_number_fact(number)}")
	except Exception as e:
		print(f"Error appending number fact: {e}")
		logger.log(logger.LOG_INFO, f"Error appending number fact: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@discord.app_commands.describe(
	number="Number to remove the fun fact for"
)
@utils.discord_bot.tree.command(description="[Admin] Remove the fun fact for a number")
@discord.app_commands.default_permissions(administrator=True)
@commands.admin_only()
async def remove_number_fact(interaction:discord.Interaction, number:int):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_admin(interaction):
		await interaction.followup.send(commands.nice_try)
		return

	try:
		logger.log(logger.LOG_DETAIL, f"Deleting fact for number {number}")
		fact = database.remove_number_fact(number)
		if fact is None:
			logger.log(logger.LOG_DETAIL, f"Number {number} didn't have a fact to delete")
			await interaction.followup.send(f"Fact for number {number} not found")
		else:
			await interaction.followup.send(f"Fact removed for number {number}\n{fact}")
	except Exception as e:
		print(f"Error removing number fact: {e}")
		logger.log(logger.LOG_INFO, f"Error removing number fact: {e}")
		await interaction.followup.send(commands.something_went_wrong)
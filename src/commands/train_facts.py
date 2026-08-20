import discord

from .. import commands_module as commands
from .. import database_module as database
from .. import logger
from .. import utils

'''
 - train_fact
 - enter_train_fact [Admin]
 - remove_train_fact [Admin]
 - get_train_facts [Admin]
'''

@utils.discord_bot.tree.command(description="Train fun-fact")
async def train_fact(interaction:discord.Interaction):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not utils.is_owner(interaction):
		await interaction.followup.send(commands.nice_try)
		return
	
	try:
		fact = database.get_random_train_fact()
		if fact is None:
			await interaction.followup.send("No train facts found :(")
			return
		embed = discord.Embed(title="Train Fact", description=fact, colour=0xffffff)
		await interaction.followup.send(embed=embed)
	except Exception as e:
		print(f"Error getting train fact: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@discord.app_commands.describe(
	fact="New train fact to add"
)
@utils.discord_bot.tree.command(description="[Admin] Enter train fact")
@discord.app_commands.default_permissions(administrator=True)
@commands.admin_only()
async def enter_train_fact(interaction:discord.Interaction, fact:str):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_owner(interaction):
		await interaction.followup.send(commands.nice_try)
		return
	
	try:
		database.insert_train_fact(fact)
		await interaction.followup.send("Train fact entered")
	except Exception as e:
		print(f"Error entering train fact: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@discord.app_commands.describe(
	fact_num="Train fact to remove"
)
@utils.discord_bot.tree.command(description="[Admin] Remove train fact")
@discord.app_commands.default_permissions(administrator=True)
@commands.admin_only()
async def remove_train_fact(interaction:discord.Interaction, fact_num:int):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_owner(interaction):
		await interaction.followup.send(commands.nice_try)
		return
	
	try:
		fact = database.remove_train_fact(fact_num)
		if fact is None:
			await interaction.followup.send(f"Fact {fact_num} not found")
		else:
			await interaction.followup.send(f"Train fact removed\n{fact}")
	except Exception as e:
		print(f"Error removing train fact: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@utils.discord_bot.tree.command(description="[Admin] Get the list of train facts")
@discord.app_commands.default_permissions(administrator=True)
@commands.admin_only()
async def get_train_facts(interaction:discord.Interaction):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_owner(interaction):
		await interaction.followup.send(commands.nice_try)
		return
	
	try:
		facts_embed = database.get_all_train_facts()
		await interaction.followup.send(embed=facts_embed)
	except Exception as e:
		print(f"Error getting train facts: {e}")
		await interaction.followup.send(commands.something_went_wrong)
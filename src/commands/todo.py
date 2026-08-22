import discord

from .. import commands_module as commands
from .. import database_module as database
from .. import logger
from .. import utils

'''
 - get_todo [Owner]
 - add_todo [Owner]
 - remove_todo [Owner]
'''

@utils.discord_bot.tree.command(description="[Owner] Get to do list")
@discord.app_commands.default_permissions() # No perms, set up in on_ready
@commands.owner_only()
async def get_todo(interaction:discord.Interaction):
	await interaction.response.defer(ephemeral=True)
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_owner(interaction):
		await interaction.followup.send(commands.nice_try)
		return
	
	try:
		logger.log(logger.LOG_EXTRA_DETAIL, "Getting to-do")
		todo_items = database.get_all_todo_items()
		if len(todo_items) != 0:
			embed = discord.Embed(title="Todo List", colour=0xffffff)
			embed.description = ""
			for item in todo_items:
				embed.description += f"{item[0]}- {item[1]}\n"
			await interaction.followup.send(embed=embed)
		else:
			await interaction.followup.send("Todo List Empty")
	except Exception as e:
		print(f"Error getting to do list: {e}")
		logger.log(logger.LOG_INFO, f"Error getting to do list: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@discord.app_commands.describe(
	item="The to do item to add"
)
@utils.discord_bot.tree.command(description="[Owner] Add to do item")
@discord.app_commands.default_permissions() # No perms, set up in on_ready
@commands.owner_only()
async def add_todo(interaction:discord.Interaction, item:str):
	await interaction.response.defer(ephemeral=True)
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_owner(interaction):
		await interaction.followup.send(commands.nice_try)
		return
	
	try:
		logger.log(logger.LOG_EXTRA_DETAIL, f"Inserting item into to-do list: {item}")
		database.insert_todo_item(item)
		await interaction.followup.send(f"Todo added: {item}")
	except Exception as e:
		print(f"Error adding to do item: {e}")
		logger.log(logger.LOG_INFO, f"Error adding to do item: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@discord.app_commands.describe(
	item_num="The to do item number to remove"
)
@utils.discord_bot.tree.command(description="[Owner] Remove to do item")
@discord.app_commands.default_permissions() # No perms, set up in on_ready
@commands.owner_only()
async def remove_todo(interaction:discord.Interaction, item_num:int):
	await interaction.response.defer(ephemeral=True)
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_owner(interaction):
		await interaction.followup.send(commands.nice_try)
		return
	
	try:
		logger.log(logger.LOG_EXTRA_DETAIL, f"Removing to-do item number {item_num}")
		database.remove_todo_item(item_num)
		await interaction.followup.send(f"Todo {item_num} removed")
	except Exception as e:
		print(f"Error removing to do item: {e}")
		logger.log(logger.LOG_INFO, f"Error removing to do item: {e}")
		await interaction.followup.send(commands.something_went_wrong)

commands.owner_commands_names.append("get_todo")
commands.owner_commands_names.append("add_todo")
commands.owner_commands_names.append("remove_todo")
commands.owner_commands.append(get_todo)
commands.owner_commands.append(add_todo)
commands.owner_commands.append(remove_todo)
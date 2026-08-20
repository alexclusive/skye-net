import discord

from .. import commands_module as commands
from .. import database_module as database
from .. import logger
from .. import utils
from ..handlers import bingo as bingo_handler

'''
 - create_bingo_card
 - get_bingo_card
 - get_bingo_card_items
 - reset_bingo_card
 - create_bingo_template [Admin]
 - update_bingo_template [Admin]
 - delete_bingo_template [Admin]
 - get_bingo_templates [Admin]
 - get_all_bingo_templates [Owner]
'''

@discord.app_commands.describe(
	bingo_name="Name of the bingo to get a card for"
)
@utils.discord_bot.tree.command(description="Create a bingo card (new card)")
async def create_bingo_card(interaction:discord.Interaction, bingo_name:str):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	
	if not utils.is_user_in_guild(interaction):
		await interaction.followup.send(commands.must_be_guild_member)
		logger.log(logger.LOG_DETAIL, f"User {interaction.user.display_name}({interaction.user.id}) is not in guild, aborting command")
		return
	
	try:
		database.delete_bingo_card(interaction.guild.id, bingo_name, interaction.user.id)
		await get_bingo_card(interaction, bingo_name)
	except Exception as e:
		print(f"Error creating bingo card: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@discord.app_commands.describe(
	bingo_name="Name of the bingo to get a card for"
)
@utils.discord_bot.tree.command(description="Get a bingo card (same card as last call if available)")
async def get_bingo_card(interaction:discord.Interaction, bingo_name:str):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	
	if not utils.is_user_in_guild(interaction):
		await interaction.followup.send(commands.must_be_guild_member)
		logger.log(logger.LOG_DETAIL, f"User {interaction.user.display_name}({interaction.user.id}) is not in guild, aborting command")
		return
	
	try:
		bingo_card = bingo_handler.get_bingo_card(interaction.guild.id, bingo_name, interaction.user.id)
		embed, view = bingo_card
		# view may be None if the card could not be generated (e.g. template missing)
		if view is not None:
			await interaction.followup.send(embed=embed, view=view)
		else:
			await interaction.followup.send(embed=embed)
	except Exception as e:
		print(f"Error getting bingo card: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@discord.app_commands.describe(
	bingo_name="Name of the bingo to get card item list for"
)
@utils.discord_bot.tree.command(description="Get the list of your bingo card items")
async def get_bingo_card_items(interaction:discord.Interaction, bingo_name:str):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	
	if not utils.is_user_in_guild(interaction):
		await interaction.followup.send(commands.must_be_guild_member)
		logger.log(logger.LOG_DETAIL, f"User {interaction.user.display_name}({interaction.user.id}) is not in guild, aborting command")
		return
	
	try:		
		embed = bingo_handler.get_bingo_card_items_embed(interaction.guild.id, bingo_name, interaction.user.id)
		await interaction.followup.send(embed=embed)
	except Exception as e:
		print(f"Error getting bingo card items: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@discord.app_commands.describe(
	bingo_name="Name of the bingo to reset your card for"
)
@utils.discord_bot.tree.command(description="Reset a bingo card")
async def reset_bingo_card(interaction:discord.Interaction, bingo_name:str):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)

	if not utils.is_user_in_guild(interaction):
		await interaction.followup.send(commands.must_be_guild_member)
		logger.log(logger.LOG_DETAIL, f"User {interaction.user.display_name}({interaction.user.id}) is not in guild, aborting command")
		return
	
	try:
		bingo_handler.reset_bingo_card(interaction.guild.id, bingo_name, interaction.user.id)
		await get_bingo_card(interaction, bingo_name)
	except Exception as e:
		print(f"Error resetting bingo card: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@discord.app_commands.describe(
	bingo_name="Name to give the new bingo",
	free_space="Give a free space in the middle of the bingo?",
	items_csv="CSV of items for bingo",
	items_message_id="Message ID of message with items for bingo (separated by new lines)"
)
@utils.discord_bot.tree.command(description="[Admin] Create a bingo template")
@discord.app_commands.default_permissions(administrator=True)
@commands.admin_only()
async def create_bingo_template(interaction:discord.Interaction, bingo_name:str, free_space:bool=True, items_csv:str="", items_message_id:str=""):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_admin(interaction):
		await interaction.followup.send(commands.nice_try)
		return
	
	try:
		items = await get_bingo_items(interaction, items_csv, items_message_id)
		await create_bingo_template(interaction, bingo_name, free_space, items)
	except Exception as e:
		print(f"Error creating bingo template: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@discord.app_commands.describe(
	bingo_name="Name of the bingo to update",
	items_csv="CSV of items for bingo",
	items_message_id="Message ID of message with items for bingo (separated by new lines)"
)
@utils.discord_bot.tree.command(description="[Admin] Update a bingo template")
@discord.app_commands.default_permissions(administrator=True)
@commands.admin_only()
async def update_bingo_template(interaction:discord.Interaction, bingo_name:str, items_csv:str="", items_message_id:str=""):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_admin(interaction):
		await interaction.followup.send(commands.nice_try)
		return
	
	try:
		items = await get_bingo_items(interaction, items_csv, items_message_id)
		await update_bingo_template(interaction, bingo_name, items)
	except Exception as e:
		print(f"Error updating bingo template: {e}")
		await interaction.followup.send(commands.something_went_wrong)

async def get_bingo_items(interaction:discord.Interaction, items_csv:str, items_message_id:str) -> list:
	if len(items_csv) == 0 and len(items_message_id) == 0:
		await interaction.followup.send("You must provide either a CSV of items or a message ID.")
		return []

	if len(items_csv) > 0 and len(items_message_id) > 0:
		await interaction.followup.send("You must provide either a CSV of items or a message ID, not both.")
		return []

	if len(items_csv) > 0:
		return items_csv.split(",")

	if len(items_message_id) > 0:
		try:
			message = await utils.discord_bot.get_channel(interaction.channel_id).fetch_message(items_message_id)
			return message.content.split("\n")
		except discord.NotFound:
			await interaction.followup.send(f"Message with ID {items_message_id} not found. Make sure the message is in the same channel as this command and the bot has access to the channel.")

	return []		

@discord.app_commands.describe(
	bingo_name="Name of the bingo to delete"
)
@utils.discord_bot.tree.command(description="[Admin] Delete a bingo template")
@discord.app_commands.default_permissions(administrator=True)
@commands.admin_only()
async def delete_bingo_template(interaction:discord.Interaction, bingo_name:str):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_admin(interaction):
		await interaction.followup.send(commands.nice_try)
		return
	
	try:
		deleted = bingo_handler.delete_bingo_template(interaction.guild.id, bingo_name)
		if deleted:
			await interaction.followup.send(f"Bingo template '{bingo_name}' deleted successfully.")
		else:
			await interaction.followup.send(f"Failed to delete bingo template '{bingo_name}'. It may not exist.")
	except Exception as e:
		print(f"Error deleting bingo template: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@utils.discord_bot.tree.command(description="[Admin] Get bingo templates for this guild")
@discord.app_commands.default_permissions() # No perms, set up in on_ready
@commands.admin_only()
async def get_bingo_templates(interaction:discord.Interaction):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_admin(interaction):
		await interaction.followup.send(commands.nice_try)
		return
	
	try:
		templates_embed = bingo_handler.get_bingo_templates_for_guild(interaction.guild.id)
		if templates_embed is None:
			await interaction.followup.send("No bingo templates found for this guild")
			return
	
		await interaction.followup.send(embed=templates_embed)
	except Exception as e:
		print(f"Error getting bingo templates: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@utils.discord_bot.tree.command(description="[Owner] Get all bingo templates")
@discord.app_commands.default_permissions() # No perms, set up in on_ready
@commands.owner_only()
async def get_all_bingo_templates(interaction:discord.Interaction):
	await interaction.response.defer(ephemeral=True)
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_owner(interaction):
		await interaction.followup.send(commands.nice_try)
		return
	
	try:
		templates_embed = bingo_handler.get_all_bingo_templates()
		if templates_embed is None:
			await interaction.followup.send("No bingo templates found")
			return
	
		await interaction.followup.send(embed=templates_embed)
	except Exception as e:
		print(f"Error getting all bingo templates: {e}")
		await interaction.followup.send(commands.something_went_wrong)


commands.owner_commands_names.append("get_all_bingo_templates")
commands.owner_commands.append(get_all_bingo_templates)
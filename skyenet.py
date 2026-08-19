import sys
import asyncio
import discord
import psutil

import handlers.utils as utils_module
import handlers.logger as logger_module
import handlers.commands as commands_module
import handlers.database as database_module
import handlers.events as events_module
import handlers.tasks as tasks_module

import handlers.helpers.spotify as spotify_module

from handlers.logger import LOG_SETUP, LOG_INFO, LOG_DETAIL, LOG_EXTRA_DETAIL

command_called_log_string = "Command called"
event_triggered_log_string = "Event triggered"
something_went_wrong = "Something went wrong :("
must_be_guild_member = "You must be a server member to use this command."

owner_commands = ["die", "set_debug_level", "force_trusted_roles", "force_audit_log", "get_todo", "add_todo", "remove_todo", "info", "send_as_bot",  "get_opt_out_users", "get_all_bingo_templates", "get_bingo_templates"]

'''
	Commands
	[Owner] is for just the bot owner
	[Admin] is for anyone with administrator permissions
'''
def owner_only():
	def predicate(interaction:discord.Interaction) -> bool:
		return utils_module.is_owner(interaction)
	return discord.app_commands.check(predicate)

def admin_only():
	def predicate(interaction:discord.Interaction) -> bool:
		return utils_module.is_admin(interaction)
	return discord.app_commands.check(predicate)

# Owner Only Commands
@utils_module.discord_bot.tree.command(description="[Owner] Run a test command")
@discord.app_commands.default_permissions() # No perms, set up in on_ready
@owner_only()
async def run_test(interaction:discord.Interaction):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		# Put test command here, so you don't have to restart discord every time to test a new function
		commands_module.train_info_module.print_all_train_set_names()
		await interaction.followup.send("No test command set up - DONE")
	except Exception as e:
		print(f"Error running test: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="[Owner] Shutdown the bot")
@discord.app_commands.default_permissions() # No perms, set up in on_ready
@owner_only()
async def die(interaction:discord.Interaction):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.die(interaction)
	except Exception as e:
		print(f"Error shutting down bot: {e}")
		await interaction.followup.send(something_went_wrong)

@discord.app_commands.describe(
	level="Debug level (0-3)"
)
@utils_module.discord_bot.tree.command(description="[Owner] Set debug level (0-3)")
@discord.app_commands.default_permissions() # No perms, set up in on_ready
@owner_only()
async def set_debug_level(interaction:discord.Interaction, level:int=0):
	await interaction.response.defer(ephemeral=True)
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		if not 0 <= level <= 3:
			await interaction.followup.send("Debug level must be between 0 and 3")
			return
		await commands_module.set_debug_level(interaction, level)
	except Exception as e:
		print(f"Error setting debug level: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="[Owner] Force trusted roles task")
@discord.app_commands.default_permissions() # No perms, set up in on_ready
@owner_only()
async def force_trusted_roles(interaction:discord.Interaction):
	await interaction.response.defer(ephemeral=True)
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.force_trusted_roles(interaction)
	except Exception as e:
		print(f"Error forcing trusted roles: {e}")
		await interaction.followup.send(something_went_wrong)

@discord.app_commands.describe(
	days_to_check="Number of days to check back in the audit log (default 1)"
)
@utils_module.discord_bot.tree.command(description="[Owner] Force audit log check")
@discord.app_commands.default_permissions() # No perms, set up in on_ready
@owner_only()
async def force_audit_log(interaction:discord.Interaction, days_to_check:int=1):
	await interaction.response.defer(ephemeral=True)
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.force_audit_log(interaction, days_to_check)
	except Exception as e:
		print(f"Error forcing audit log: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="[Owner] Reread train info html")
@discord.app_commands.default_permissions() # No perms, set up in on_ready
@owner_only()
async def reread_train_info(interaction:discord.Interaction):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.reread_train_info_html(interaction)
	except Exception as e:
		print(f"Error rereading train info: {e}")
		await interaction.followup.send(something_went_wrong)

# To Do List
@utils_module.discord_bot.tree.command(description="[Owner] Get to do list")
@discord.app_commands.default_permissions() # No perms, set up in on_ready
@owner_only()
async def get_todo(interaction:discord.Interaction):
	await interaction.response.defer(ephemeral=True)
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.get_todo(interaction)
	except Exception as e:
		print(f"Error getting to do list: {e}")
		await interaction.followup.send(something_went_wrong)

@discord.app_commands.describe(
	item="The to do item to add"
)
@utils_module.discord_bot.tree.command(description="[Owner] Add to do item")
@discord.app_commands.default_permissions() # No perms, set up in on_ready
@owner_only()
async def add_todo(interaction:discord.Interaction, item:str):
	await interaction.response.defer(ephemeral=True)
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.add_todo(interaction, item)
	except Exception as e:
		print(f"Error adding to do item: {e}")
		await interaction.followup.send(something_went_wrong)

@discord.app_commands.describe(
	item_num="The to do item number to remove"
)
@utils_module.discord_bot.tree.command(description="[Owner] Remove to do item")
@discord.app_commands.default_permissions() # No perms, set up in on_ready
@owner_only()
async def remove_todo(interaction:discord.Interaction, item_num:int):
	await interaction.response.defer(ephemeral=True)
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.remove_todo(interaction, item_num)
	except Exception as e:
		print(f"Error removing to do item: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="[Owner] Get bot info and system specs")
@discord.app_commands.default_permissions() # No perms, set up in on_ready
@owner_only()
async def info(interaction:discord.Interaction):
	logger_module.log(LOG_DETAIL, command_called_log_string)
	await interaction.response.defer()
	await commands_module.get_bot_info(interaction)

@discord.app_commands.describe(
	channel_id="Channel ID to send to",
	server_id="Server ID to send to",
	message="Message content"
)
@utils_module.discord_bot.tree.command(description="[Owner] Send message as Skye-net")
@discord.app_commands.default_permissions() # No perms, set up in on_ready
@owner_only()
async def send_as_bot(interaction:discord.Interaction, channel_id:str, server_id:str, message:str):
	logger_module.log(LOG_DETAIL, command_called_log_string)
	await interaction.response.defer(ephemeral=True)
	server = utils_module.discord_bot.get_guild(int(server_id))
	if not server:
		await interaction.followup.send("Invalid server ID", ephemeral=True)
		return
	channel = server.get_channel(int(channel_id))
	if not channel:
		await interaction.followup.send("Invalid channel ID", ephemeral=True)
		return
	await commands_module.send_as_bot(interaction, channel, message)

# Open AI
@utils_module.discord_bot.tree.command(description="[Admin] Get users banned from certain bot interactions")
@discord.app_commands.default_permissions(administrator=True)
@admin_only()
async def get_banned_users(interaction:discord.Interaction):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.get_banned_users(interaction)
	except Exception as e:
		print(f"Error getting banned users: {e}")
		await interaction.followup.send(something_went_wrong)

@discord.app_commands.describe(
	user_id="User ID to ban from bot interactions"
)
@utils_module.discord_bot.tree.command(description="[Admin] Ban a user from certain bot interactions")
@discord.app_commands.default_permissions(administrator=True)
@admin_only()
async def ban_user(interaction:discord.Interaction, user:discord.User):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.ban_user(interaction, user)
	except Exception as e:
		print(f"Error banning user: {e}")
		await interaction.followup.send(something_went_wrong)

@discord.app_commands.describe(
	user_id="User ID to unban from bot interactions"
)
@utils_module.discord_bot.tree.command(description="[Admin] Unban a user from certain bot interactions")
@discord.app_commands.default_permissions(administrator=True)
@admin_only()
async def unban_user(interaction:discord.Interaction, user:discord.User):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.unban_user(interaction, user)
	except Exception as e:
		print(f"Error unbanning user: {e}")
		await interaction.followup.send(something_went_wrong)

@discord.app_commands.describe(
	prompt="New prompt"
)
@utils_module.discord_bot.tree.command(description="Set the bot's prompt")
async def set_prompt(interaction:discord.Interaction, prompt:str):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.set_prompt(interaction, prompt)
	except Exception as e:
		print(f"Error setting prompt: {e}")
		await interaction.followup.send(something_went_wrong)

# Reaction Opt-in / Opt-out
@utils_module.discord_bot.tree.command(description="[Owner] Get list of user IDs that have opted out of reactions")
@discord.app_commands.default_permissions() # No perms, set up in on_ready
@owner_only()
async def get_opt_out_users(interaction:discord.Interaction):
	await interaction.response.defer(ephemeral=True)
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.get_opt_out_users(interaction)
	except Exception as e:
		print(f"Error getting opt-out users: {e}")
		await interaction.followup.send(something_went_wrong)

@discord.app_commands.describe(
	user_id="User ID to opt out from bot reactions"
)
@utils_module.discord_bot.tree.command(description="[Admin] Opt a user out of reactions")
@discord.app_commands.default_permissions(administrator=True)
@admin_only()
async def opt_out_user(interaction:discord.Interaction, user_id:int):
	await interaction.response.defer(ephemeral=True)
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.force_opt_out_reactions(interaction, user_id)
	except Exception as e:
		print(f"Error forcing opt out of reactions: {e}")
		await interaction.followup.send(something_went_wrong)

@discord.app_commands.describe(
	user_id="User ID to opt in to bot reactions"
)
@utils_module.discord_bot.tree.command(description="[Admin] Opt a user in to reactions")
@discord.app_commands.default_permissions(administrator=True)
@admin_only()
async def opt_in_user(interaction:discord.Interaction, user_id:int):
	await interaction.response.defer(ephemeral=True)
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.force_opt_in_reactions(interaction, user_id)
	except Exception as e:
		print(f"Error forcing opt in of reactions: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="Opt out of the bot's reactions")
async def opt_out(interaction:discord.Interaction):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.opt_out_reactions(interaction)
	except Exception as e:
		print(f"Error getting opt out reactions: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="Opt in to the bot's reactions")
async def opt_in(interaction:discord.Interaction):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.opt_in_reactions(interaction)
	except Exception as e:
		print(f"Error getting opt in reactions: {e}")
		await interaction.followup.send(something_went_wrong)

# Bingo
@utils_module.discord_bot.tree.command(description="[Owner] Get all bingo templates")
@discord.app_commands.default_permissions() # No perms, set up in on_ready
@owner_only()
async def get_all_bingo_templates(interaction:discord.Interaction):
	await interaction.response.defer(ephemeral=True)
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.get_all_bingo_templates(interaction)
	except Exception as e:
		print(f"Error getting all bingo templates: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="[Admin] Get bingo templates for this guild")
@discord.app_commands.default_permissions() # No perms, set up in on_ready
@owner_only()
async def get_bingo_templates(interaction:discord.Interaction):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.get_bingo_templates_for_guild(interaction)
	except Exception as e:
		print(f"Error getting bingo templates: {e}")
		await interaction.followup.send(something_went_wrong)

@discord.app_commands.describe(
	bingo_name="Name to give the new bingo",
	free_space="Give a free space in the middle of the bingo?",
	items_csv="CSV of items for bingo",
	items_message_id="Message ID of message with items for bingo (separated by new lines)"
)
@utils_module.discord_bot.tree.command(description="[Admin] Create a bingo template")
@discord.app_commands.default_permissions(administrator=True)
@admin_only()
async def create_bingo_template(interaction:discord.Interaction, bingo_name:str, free_space:bool=True, items_csv:str="", items_message_id:str=""):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		if len(items_csv) == 0 and len(items_message_id) == 0:
			await interaction.followup.send("You must provide either a CSV of items or a message ID.")
			return
		if len(items_csv) > 0 and len(items_message_id) > 0:
			await interaction.followup.send("You must provide either a CSV of items or a message ID, not both.")
			return
		if len(items_csv) > 0:
			await commands_module.create_bingo_template_through_csv(interaction, bingo_name, free_space, items_csv)
		elif len(items_message_id) > 0:
			try:
				message = await utils_module.discord_bot.get_channel(interaction.channel_id).fetch_message(items_message_id)
				await commands_module.create_bingo_template_through_message(interaction, bingo_name, free_space, message)
			except discord.NotFound:
				await interaction.followup.send(f"Message with ID {items_message_id} not found. Make sure the message is in the same channel as this command and the bot has access to the channel.")
				return
	except Exception as e:
		print(f"Error creating bingo template: {e}")
		await interaction.followup.send(something_went_wrong)

@discord.app_commands.describe(
	bingo_name="Name of the bingo to delete"
)
@utils_module.discord_bot.tree.command(description="[Admin] Delete a bingo template")
@discord.app_commands.default_permissions(administrator=True)
@admin_only()
async def delete_bingo_template(interaction:discord.Interaction, bingo_name:str):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.delete_bingo_template(interaction, bingo_name)
	except Exception as e:
		print(f"Error deleting bingo template: {e}")
		await interaction.followup.send(something_went_wrong)

@discord.app_commands.describe(
	bingo_name="Name of the bingo to update",
	items_csv="CSV of items for bingo",
	items_message_id="Message ID of message with items for bingo (separated by new lines)"
)
@utils_module.discord_bot.tree.command(description="[Admin] Update a bingo template")
@discord.app_commands.default_permissions(administrator=True)
@admin_only()
async def update_bingo_template(interaction:discord.Interaction, bingo_name:str, items_csv:str="", items_message_id:str=""):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		if len(items_csv) == 0 and len(items_message_id) == 0:
			await interaction.followup.send("You must provide either a CSV of items or a message ID.")
			return
		if len(items_csv) > 0 and len(items_message_id) > 0:
			await interaction.followup.send("You must provide either a CSV of items or a message ID, not both.")
			return
		if len(items_csv) > 0:
			await commands_module.update_bingo_template_through_csv(interaction, bingo_name, items_csv)
		elif len(items_message_id) > 0:
			try:
				message = await utils_module.discord_bot.get_channel(interaction.channel_id).fetch_message(items_message_id)
				await commands_module.update_bingo_template_through_message(interaction, bingo_name, message)
			except discord.NotFound:
				await interaction.followup.send(f"Message with ID {items_message_id} not found. Make sure the message is in the same channel as this command and the bot has access to the channel.")
				return
	except Exception as e:
		print(f"Error updating bingo template: {e}")
		await interaction.followup.send(something_went_wrong)

@discord.app_commands.describe(
	bingo_name="Name of the bingo to get a card for"
)
@utils_module.discord_bot.tree.command(description="Get a bingo card (same card as last call if available)")
async def get_bingo_card(interaction:discord.Interaction, bingo_name:str):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	if not utils_module.is_user_in_guild(interaction):
		await interaction.followup.send(must_be_guild_member)
		logger_module.log(LOG_DETAIL, f"User {interaction.user.display_name}({interaction.user.id}) is not in guild, aborting command")
		return
	try:
		await commands_module.get_bingo_card(interaction, bingo_name)
	except Exception as e:
		print(f"Error getting bingo card: {e}")
		await interaction.followup.send(something_went_wrong)

@discord.app_commands.describe(
	bingo_name="Name of the bingo to get a card for"
)
@utils_module.discord_bot.tree.command(description="Create a bingo card (new card)")
async def create_bingo_card(interaction:discord.Interaction, bingo_name:str):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	if not utils_module.is_user_in_guild(interaction):
		await interaction.followup.send(must_be_guild_member)
		logger_module.log(LOG_DETAIL, f"User {interaction.user.display_name}({interaction.user.id}) is not in guild, aborting command")
		return
	try:
		await commands_module.create_bingo_card(interaction, bingo_name)
	except Exception as e:
		print(f"Error creating bingo card: {e}")
		await interaction.followup.send(something_went_wrong)

@discord.app_commands.describe(
	bingo_name="Name of the bingo to reset your card for"
)
@utils_module.discord_bot.tree.command(description="Reset a bingo card")
async def reset_bingo_card(interaction:discord.Interaction, bingo_name:str):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	if not utils_module.is_user_in_guild(interaction):
		await interaction.followup.send(must_be_guild_member)
		logger_module.log(LOG_DETAIL, f"User {interaction.user.display_name}({interaction.user.id}) is not in guild, aborting command")
		return
	try:
		await commands_module.reset_bingo_card(interaction, bingo_name)
	except Exception as e:
		print(f"Error resetting bingo card: {e}")
		await interaction.followup.send(something_went_wrong)

@discord.app_commands.describe(
	bingo_name="Name of the bingo to get card item list for"
)
@utils_module.discord_bot.tree.command(description="Get the list of your bingo card items")
async def get_bingo_card_items(interaction:discord.Interaction, bingo_name:str):
	await interaction.response.defer(ephemeral=True)
	logger_module.log(LOG_DETAIL, command_called_log_string)
	if not utils_module.is_user_in_guild(interaction):
		await interaction.followup.send(must_be_guild_member)
		logger_module.log(LOG_DETAIL, f"User {interaction.user.display_name}({interaction.user.id}) is not in guild, aborting command")
		return
	try:		
		await commands_module.get_bingo_card_items(interaction, bingo_name)
	except Exception as e:
		print(f"Error getting bingo card items: {e}")
		await interaction.followup.send(something_went_wrong)

# Train Facts
@discord.app_commands.describe(
	fact="New train fact to add"
)
@utils_module.discord_bot.tree.command(description="[Admin] Enter train fact")
@discord.app_commands.default_permissions(administrator=True)
@admin_only()
async def enter_train_fact(interaction:discord.Interaction, fact:str):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.enter_train_fact(interaction, fact)
	except Exception as e:
		print(f"Error entering train fact: {e}")
		await interaction.followup.send(something_went_wrong)

@discord.app_commands.describe(
	fact_num="Train fact to remove"
)
@utils_module.discord_bot.tree.command(description="[Admin] Remove train fact")
@discord.app_commands.default_permissions(administrator=True)
@admin_only()
async def remove_train_fact(interaction:discord.Interaction, fact_num:int):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.remove_train_fact(interaction, fact_num)
	except Exception as e:
		print(f"Error removing train fact: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="[Admin] Get the list of train facts")
@discord.app_commands.default_permissions(administrator=True)
@admin_only()
async def get_train_facts(interaction:discord.Interaction):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.get_train_facts(interaction)
	except Exception as e:
		print(f"Error getting train facts: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="Train fun-fact")
async def train_fact(interaction:discord.Interaction):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.train_fact(interaction)
	except Exception as e:
		print(f"Error getting train fact: {e}")
		await interaction.followup.send(something_went_wrong)

# Train Game
@discord.app_commands.describe(
	number="The starting number for the game - four digits",
	target="The target number to reach - default 10",
	strict_mode="Only use basic operations (+-*/), and do not permutate the numbers - default False"
)
@utils_module.discord_bot.tree.command(description="Train game - get to [target] using (+-*/) and optionally (^%)")
async def train_game(
	interaction:discord.Interaction,
	number:str,
	target:int = 10,
	strict_mode:bool = False,
):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.train_game(interaction, number, target, strict_mode)
	except Exception as e:
		print(f"Error getting train game: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="Train game - explanation of rules")
async def train_game_rules(interaction:discord.Interaction):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.train_game_rules(interaction)
	except Exception as e:
		print(f"Error getting train game rules: {e}")
		await interaction.followup.send(something_went_wrong)

# Number Facts
@discord.app_commands.describe(
	number="Number to update the fun fact for"
)
@utils_module.discord_bot.tree.command(description="[Admin] Update the fun fact for a number")
@discord.app_commands.default_permissions(administrator=True)
@admin_only()
async def update_number_fact(interaction:discord.Interaction, number:int, fact:str):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.update_number_fact(interaction, number, fact)
	except Exception as e:
		print(f"Error updating number fact: {e}")
		await interaction.followup.send(something_went_wrong)

@discord.app_commands.describe(
	number="Number to append the fun fact for"
)
@utils_module.discord_bot.tree.command(description="[Admin] Append to the fun fact for a number")
@discord.app_commands.default_permissions(administrator=True)
@admin_only()
async def append_number_fact(interaction:discord.Interaction, number:int, fact:str):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.append_number_fact(interaction, number, fact)
	except Exception as e:
		print(f"Error appending number fact: {e}")
		await interaction.followup.send(something_went_wrong)

@discord.app_commands.describe(
	number="Number to remove the fun fact for"
)
@utils_module.discord_bot.tree.command(description="[Admin] Remove the fun fact for a number")
@discord.app_commands.default_permissions(administrator=True)
@admin_only()
async def remove_number_fact(interaction:discord.Interaction, number:int):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.remove_number_fact(interaction, number)
	except Exception as e:
		print(f"Error removing number fact: {e}")
		await interaction.followup.send(something_went_wrong)

@discord.app_commands.describe(
	number="Number to find a fun fact about"
)
@utils_module.discord_bot.tree.command(description="Get a fun fact about a number")
async def number_fact(interaction:discord.Interaction, number:int):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.number_fact(interaction, number)
	except Exception as e:
		print(f"Error getting number fact: {e}")
		await interaction.followup.send(something_went_wrong)

# Misc
@utils_module.discord_bot.tree.command(description="Check the bot's ping")
async def ping(interaction:discord.Interaction):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.ping(interaction)
	except Exception as e:
		print(f"Error getting ping: {e}")
		await interaction.followup.send(something_went_wrong)

@discord.app_commands.describe(
	argument="Word or phrase to check the etymology of"
)
@utils_module.discord_bot.tree.command(description="Get the etymology of a word")
async def etymology(interaction:discord.Interaction, argument:str):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.etymology(interaction, argument)
	except Exception as e:
		print(f"Error getting etymology: {e}")
		await interaction.followup.send(something_went_wrong)

'''
	Events
'''
async def ensure_correct_permissions():
	for guild in utils_module.discord_bot.guilds:
		for cmd in await utils_module.discord_bot.tree.fetch_commands(guild=guild):
			if cmd.name in owner_commands:
				perm = discord.app_commands.PermissionOverwrite(
					id=utils_module.owner_id,
					type=discord.app_commands.PermissionType.user,
					permission=True
				)
				await cmd.edit_permissions(guild=guild, permissions=[perm])

	die.dm_permission = False
	set_debug_level.dm_permission = False
	force_trusted_roles.dm_permission = False
	force_audit_log.dm_permission = False
	get_todo.dm_permission = False
	add_todo.dm_permission = False
	remove_todo.dm_permission = False
	info.dm_permission = False
	send_as_bot.dm_permission = False

@utils_module.discord_bot.event
async def on_ready():
	logger_module.log(LOG_DETAIL, event_triggered_log_string)
	await utils_module.discord_bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.CustomActivity("Skye-net is watching...", type=discord.ActivityType.watching))
	await utils_module.discord_bot.tree.sync()
	await ensure_correct_permissions() # gotta be after sync, cause sync updates which guilds we're in
	print(f"{utils_module.discord_bot.user} is ready and online :P")
	_ = psutil.cpu_percent(percpu=True) # first call is always 0.0, so call it once to get actual data next time
	tasks_module.tasks_on_ready()

@utils_module.discord_bot.event
async def on_message(message):
	logger_module.log(LOG_EXTRA_DETAIL, event_triggered_log_string + f" by {message.author} in {message.channel}")
	await events_module.message(message)

@utils_module.discord_bot.event
async def on_message_delete(message):
	logger_module.log(LOG_DETAIL, event_triggered_log_string + f" by {message.author} in {message.channel}")
	await events_module.message_deleted(message)

@utils_module.discord_bot.event
async def on_guild_channel_create(channel:discord.abc.GuildChannel):
	logger_module.log(LOG_DETAIL, event_triggered_log_string + f" in {channel.guild.name}")
	await events_module.channel_create(channel)

@utils_module.discord_bot.event
async def on_guild_channel_delete(channel:discord.abc.GuildChannel):
	logger_module.log(LOG_DETAIL, event_triggered_log_string + f" in {channel.guild.name}")
	await events_module.channel_delete(channel)

@utils_module.discord_bot.event
async def on_guild_role_create(role:discord.Role):
	logger_module.log(LOG_DETAIL, event_triggered_log_string + f" in {role.guild.name}")
	await events_module.role_create(role)

@utils_module.discord_bot.event
async def on_guild_role_delete(role:discord.Role):
	logger_module.log(LOG_DETAIL, event_triggered_log_string + f" in {role.guild.name}")
	await events_module.role_delete(role)

@utils_module.discord_bot.event
async def on_member_join(member:discord.Member):
	logger_module.log(LOG_DETAIL, event_triggered_log_string + f" in {member.guild.name}")
	await events_module.member_join(member)

@utils_module.discord_bot.event
async def on_member_remove(member:discord.Member):
	logger_module.log(LOG_DETAIL, event_triggered_log_string + f" in {member.guild.name}")
	await events_module.member_remove(member)

@utils_module.discord_bot.event
async def on_member_update(before:discord.Member, after:discord.Member):
	# nickname / roles / guild avatar
	logger_module.log(LOG_DETAIL, event_triggered_log_string)
	await events_module.member_update(before, after)

@utils_module.discord_bot.event
async def on_member_ban(member:discord.Member):
	logger_module.log(LOG_DETAIL, f"Event triggered in {member.guild.name}")
	await events_module.member_ban(member)

'''
	Discord handling
'''
def _log_send_exception(task:asyncio.Task) -> None:
	try:
		task.result()
	except Exception as e:
		logger_module.log(LOG_INFO, f"Discord send failed: {e}")

async def _send_message_async(channel:discord.abc.Messageable, message:str) -> None:
	try:
		await channel.send(message)
	except discord.HTTPException as e:
		if getattr(e, 'code', None) == 32:
			await asyncio.sleep(0.5)
			await channel.send(message)
		else:
			raise

def send_message(channel:discord.abc.Messageable, message:str) -> None:
	if len(message) > 2000:  # discord won't allow longer than 2000 characters, so split it up
		for i in range(0, len(message), 2000):
			chunk = message[i:i+2000]
			task = asyncio.ensure_future(_send_message_async(channel, chunk))
			task.add_done_callback(_log_send_exception)
	else:
		task = asyncio.ensure_future(_send_message_async(channel, message))
		task.add_done_callback(_log_send_exception)

def send_output_to_discord(message:str):
	message = message.strip()
	if message:
		channel = utils_module.discord_bot.get_channel(utils_module.stdout_channel_id)
		if channel:
			send_message(channel, message)

async def run_bot():
	logger_module.set_log_file(utils_module.log_file_path)
	database_module.init_db()
	logger_module.set_debug_level(database_module.get_debug_level())
	utils_module.set_current_prompt(database_module.get_most_recent_prompt())
	utils_module.fill_banned_users()
	utils_module.fill_emojis()
	spotify_module.setup_spotify_credentials()
	sys.stdout.write = send_output_to_discord
	sys.stderr.write = send_output_to_discord

	try:
		logger_module.log(LOG_SETUP, "Starting bot...")
		await utils_module.discord_bot.start(utils_module.token)
	except Exception as e:
		logger_module.log(LOG_SETUP, "Shutting down bot...")
		if not utils_module.received_shutdown: # Probably won't happen cause shutdown shouldn't raise exception
			await utils_module.discord_bot.close()
		print(f"Error: {e}")
		raise e

try:
	asyncio.run(run_bot())
except KeyboardInterrupt:
	pass
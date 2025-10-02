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

# Generic Owner Only Commands
@utils_module.discord_bot.tree.command(description="[Owner] Shutdown the bot")
@owner_only()
async def die(interaction:discord.Interaction):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.die(interaction)
	except Exception as e:
		print(f"Error shutting down bot: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="[Owner] Set debug level (0-3)")
@owner_only()
async def set_debug_level(interaction:discord.Interaction, level:int):
	await interaction.response.defer(ephemeral=True)
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.set_debug_level(interaction, level)
	except Exception as e:
		print(f"Error setting debug level: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="[Owner] Force trusted roles task")
@owner_only()
async def force_trusted_roles(interaction:discord.Interaction):
	await interaction.response.defer(ephemeral=True)
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await interaction.response.defer(ephemeral=True)
		await commands_module.force_trusted_roles(interaction)
	except Exception as e:
		print(f"Error forcing trusted roles: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="[Owner] Force audit log check")
@owner_only()
async def force_audit_log(interaction:discord.Interaction, days_to_check:int=1):
	await interaction.response.defer(ephemeral=True)
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.force_audit_log(interaction, days_to_check)
	except Exception as e:
		print(f"Error forcing audit log: {e}")
		await interaction.followup.send(something_went_wrong)

# To Do List
@utils_module.discord_bot.tree.command(description="[Owner] Get to do list")
@owner_only()
async def get_todo(interaction:discord.Interaction):
	await interaction.response.defer(ephemeral=True)
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.get_todo(interaction)
	except Exception as e:
		print(f"Error getting to do list: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="[Owner] Add to do item")
@owner_only()
async def add_todo(interaction:discord.Interaction, item:str):
	await interaction.response.defer(ephemeral=True)
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.add_todo(interaction, item)
	except Exception as e:
		print(f"Error adding to do item: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="[Owner] Remove to do item")
@owner_only()
async def remove_todo(interaction:discord.Interaction, item_num:int):
	await interaction.response.defer(ephemeral=True)
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.remove_todo(interaction, item_num)
	except Exception as e:
		print(f"Error removing to do item: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="[Owner] Get bot info - Checking disk usage can be slow on some machines")
@owner_only()
async def info(interaction:discord.Interaction, check_disk_usage:bool=True):
	logger_module.log(LOG_DETAIL, command_called_log_string)
	await interaction.response.defer(ephemeral=True)
	await commands_module.get_bot_info(interaction, check_disk_usage)

@utils_module.discord_bot.tree.command(description="[Owner] Send message as Skye-net")
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
@utils_module.discord_bot.tree.command(description="[Admin] Get openai banned users")
@admin_only()
async def get_banned_users(interaction:discord.Interaction):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.get_banned_users(interaction)
	except Exception as e:
		print(f"Error getting banned users: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="[Admin] Ban a user from openai interactions")
@admin_only()
async def ban_user(interaction:discord.Interaction, user:discord.User):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.ban_user(interaction, user)
	except Exception as e:
		print(f"Error banning user: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="[Admin] Unban a user from openai interactions")
@admin_only()
async def unban_user(interaction:discord.Interaction, user:discord.User):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.unban_user(interaction, user)
	except Exception as e:
		print(f"Error unbanning user: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="Reset the bot's prompt")
async def reset_prompt(interaction:discord.Interaction):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.reset_prompt(interaction)
	except Exception as e:
		print(f"Error resetting prompt: {e}")
		await interaction.followup.send(something_went_wrong)

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
@owner_only()
async def get_opt_out_users(interaction:discord.Interaction):
	await interaction.response.defer(ephemeral=True)
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await interaction.response.defer(ephemeral=True)
		await commands_module.get_opt_out_users(interaction)
	except Exception as e:
		print(f"Error getting opt-out users: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="[Admin] Opt a user out of reactions")
@admin_only()
async def opt_out_user(interaction:discord.Interaction, user_id:int):
	await interaction.response.defer(ephemeral=True)
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.force_opt_out_reactions(interaction, user_id)
	except Exception as e:
		print(f"Error forcing opt out of reactions: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="[Admin] Opt a user in to reactions")
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
@owner_only()
async def get_bingo_templates(interaction:discord.Interaction):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.get_bingo_templates_for_guild(interaction)
	except Exception as e:
		print(f"Error getting bingo templates: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="[Admin] Create a bingo template")
@owner_only()
async def create_bingo_template(interaction:discord.Interaction, bingo_name:str, free_space:bool, items_csv:str="", items_message_id:str=""):
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
				await interaction.followup.send(f"Message with ID {items_message_id} not found. Make sure the message is in the same channel as this command.")
				return
	except Exception as e:
		print(f"Error creating bingo template: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="[Admin] Delete a bingo template")
@owner_only()
async def delete_bingo_template(interaction:discord.Interaction, bingo_name:str):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.delete_bingo_template(interaction, bingo_name)
	except Exception as e:
		print(f"Error deleting bingo template: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="Get a bingo card")
@owner_only()
async def get_bingo_card(interaction:discord.Interaction, bingo_name:str):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.get_bingo_card(interaction, bingo_name)
	except Exception as e:
		print(f"Error getting bingo card: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="Reset a bingo card")
@owner_only()
async def reset_bingo_card(interaction:discord.Interaction, bingo_name:str):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.reset_bingo_card(interaction, bingo_name)
	except Exception as e:
		print(f"Error resetting bingo card: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="Recreate a bingo card (new items)")
@owner_only()
async def recreate_bingo_card(interaction:discord.Interaction, bingo_name:str):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.recreate_bingo_card(interaction, bingo_name)
	except Exception as e:
		print(f"Error recreating bingo card: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="Get the list of your bingo card items")
@owner_only()
async def get_bingo_card_items(interaction:discord.Interaction, bingo_name:str):
	await interaction.response.defer(ephemeral=True)
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.get_bingo_card_items(interaction, bingo_name)
	except Exception as e:
		print(f"Error getting bingo card items: {e}")
		await interaction.followup.send(something_went_wrong)

# Train Facts
@utils_module.discord_bot.tree.command(description="[Admin] Enter train fact")
@admin_only()
async def enter_train_fact(interaction:discord.Interaction, fact:str):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.enter_train_fact(interaction, fact)
	except Exception as e:
		print(f"Error entering train fact: {e}")
		await interaction.followup.send(something_went_wrong)

@utils_module.discord_bot.tree.command(description="[Admin] Remove train fact")
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
@utils_module.discord_bot.tree.command(description="Train game - get to [target] using (+-*/) and optionally (^%)")
async def train_game(
	interaction:discord.Interaction,
	number:int,  # The starting number for the game - four digits
	target:int = 10,  # The target number to reach - default 10
	use_power:str = "True",  # Allow usage of the power (^) operation - default True
	use_modulo:str = "True",  # Allow usage of the modulo (%) operation - default True
):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		use_power_bool = "true" in use_power.lower()
		use_modulo_bool = "true" in use_modulo.lower()
		await commands_module.train_game(interaction, number, target, use_power_bool, use_modulo_bool)
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

@utils_module.discord_bot.tree.command(description="Get the etymology of a word")
async def etymology(interaction:discord.Interaction, argument:str):
	await interaction.response.defer()
	logger_module.log(LOG_DETAIL, command_called_log_string)
	try:
		await commands_module.etymology(interaction, argument)
	except Exception as e:
		print(f"Error getting etymology: {e}")
		await interaction.followup.send(something_went_wrong)
























# # Stickers
# @utils_module.discord_bot.tree.command(description="[Owner] Get a list of all stickers in all guilds")
# @owner_only()
# async def get_all_stickers(interaction:discord.Interaction):
# 	await interaction.response.defer(ephemeral=True)
# 	logger_module.log(LOG_DETAIL, command_called_log_string)
# 	try:
# 		await commands_module.get_stickers(interaction)
# 	except Exception as e:
# 		print(f"Error getting stickers: {e}")
# 		await interaction.followup.send(something_went_wrong)

# @utils_module.discord_bot.tree.command(description="[Admin] Get a list of all stickers for this guild")
# @admin_only()
# async def get_stickers(interaction:discord.Interaction):
# 	await interaction.response.defer(ephemeral=True)
# 	logger_module.log(LOG_DETAIL, command_called_log_string)
# 	try:
# 		await commands_module.get_stickers_for_guild(interaction)
# 	except Exception as e:
# 		print(f"Error getting stickers: {e}")
# 		await interaction.followup.send(something_went_wrong)

# @utils_module.discord_bot.tree.command(description="[Admin] Add a sticker")
# @admin_only()
# async def add_sticker(interaction:discord.Interaction, sticker_id:str):
# 	await interaction.response.defer(ephemeral=True)
# 	logger_module.log(LOG_DETAIL, command_called_log_string)
# 	try:
# 		await commands_module.add_sticker(interaction, sticker_id)
# 	except Exception as e:
# 		print(f"Error adding sticker: {e}")
# 		await interaction.followup.send(something_went_wrong)

# @utils_module.discord_bot.tree.command(description="[Admin] Remove a sticker")
# @admin_only()
# async def remove_sticker(interaction:discord.Interaction, sticker_id:str):
# 	await interaction.response.defer(ephemeral=True)
# 	logger_module.log(LOG_DETAIL, command_called_log_string)
# 	try:
# 		await commands_module.remove_sticker(interaction, sticker_id)
# 	except Exception as e:
# 		print(f"Error removing sticker: {e}")
# 		await interaction.followup.send(something_went_wrong)

# # Logging
# @utils_module.discord_bot.tree.command(description="[Admin] Get logging channels")
# @admin_only()
# async def get_logging_channels(interaction:discord.Interaction):
# 	await interaction.response.defer()
# 	logger_module.log(LOG_DETAIL, command_called_log_string)
# 	try:
# 		await commands_module.get_log_channels(interaction)
# 	except Exception as e:
# 		print(f"Error getting log channels: {e}")
# 		await interaction.followup.send(something_went_wrong)

# @utils_module.discord_bot.tree.command(description="[Admin] Set logging channel")
# @admin_only()
# async def set_logging_channel(interaction:discord.Interaction, message_channel:discord.TextChannel=None, member_channel:discord.TextChannel=None, role_channel:discord.TextChannel=None):
# 	await interaction.response.defer()
# 	logger_module.log(LOG_DETAIL, command_called_log_string)
# 	try:
# 		await commands_module.set_log_channels(interaction, message_channel, member_channel, role_channel)
# 	except Exception as e:
# 		print(f"Error setting log channels: {e}")
# 		await interaction.followup.send(something_went_wrong)

# @utils_module.discord_bot.tree.command(description="[Admin] Get important roles")
# @admin_only()
# async def get_roles(interaction:discord.Interaction):
# 	await interaction.response.defer()
# 	logger_module.log(LOG_DETAIL, command_called_log_string)
# 	try:
# 		await commands_module.get_important_roles(interaction)
# 	except Exception as e:
# 		print(f"Error getting important roles: {e}")
# 		await interaction.followup.send(something_went_wrong)

# @utils_module.discord_bot.tree.command(description="[Admin] Set important roles")
# @admin_only()
# async def set_roles(interaction:discord.Interaction, welcomed:discord.Role=None, trusted:discord.Role=None, trusted_time_days:int=14):
# 	await interaction.response.defer()
# 	logger_module.log(LOG_DETAIL, command_called_log_string)
# 	try:
# 		await commands_module.set_important_roles(interaction, welcomed, trusted, trusted_time_days)
# 	except Exception as e:
# 		print(f"Error setting important roles: {e}")
# 		await interaction.followup.send(something_went_wrong)

# # Reaction Triggers
# @utils_module.discord_bot.tree.command(description="[Admin] Get the list of reactions")
# @admin_only()
# async def get_reactions(interaction:discord.Interaction):
# 	await interaction.response.defer()
# 	logger_module.log(LOG_DETAIL, command_called_log_string)
# 	try:
# 		await commands_module.get_reactions(interaction)
# 	except Exception as e:
# 		print(f"Error getting reactions: {e}")
# 		await interaction.followup.send(something_went_wrong)

# @utils_module.discord_bot.tree.command(description="[Admin] Insert a reaction trigger")
# @admin_only()
# async def insert_reaction(interaction:discord.Interaction, trigger:str, emoji_1:str, emoji_2:str="", emoji_3:str=""):
# 	await interaction.response.defer()
# 	logger_module.log(LOG_DETAIL, command_called_log_string)
# 	try:
# 		await commands_module.insert_reaction(interaction, trigger, emoji_1, emoji_2, emoji_3)
# 	except Exception as e:
# 		print(f"Error inserting reaction: {e}")
# 		await interaction.followup.send(something_went_wrong)

# @utils_module.discord_bot.tree.command(description="[Admin] Remove a reaction trigger")
# @admin_only()
# async def remove_reaction(interaction:discord.Interaction, trigger:str):
# 	await interaction.response.defer()
# 	logger_module.log(LOG_DETAIL, command_called_log_string)
# 	try:
# 		await commands_module.remove_reaction(interaction, trigger)
# 	except Exception as e:
# 		print(f"Error removing reaction: {e}")
# 		await interaction.followup.send(something_went_wrong)

'''
	Events
'''
@utils_module.discord_bot.event
async def on_ready():
	logger_module.log(LOG_DETAIL, event_triggered_log_string)
	await utils_module.discord_bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.CustomActivity("Skye-net is watching...", type=discord.ActivityType.watching))
	await utils_module.discord_bot.tree.sync()
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
def send_message(channel:discord.abc.Messageable, message:str) -> None:
	if len(message) > 2000:  # discord won't allow longer than 2000 characters, so split it up
		for i in range(0, len(message), 2000):
			chunk = message[i:i+2000]
			_ = asyncio.ensure_future(channel.send(chunk))
	else:
		_ = asyncio.ensure_future(channel.send(message))

def send_output_to_discord(message:str):
	message = message.strip()
	if message:
		channel = utils_module.discord_bot.get_channel(utils_module.stdout_channel_id)
		if channel:
			try: # catch error code 32: broken pipe
				send_message(channel, message)
			except discord.HTTPException as e:
				if e.code == 32:
					asyncio.sleep(0.5) # wait for a bit and try again
					send_message(channel, message)

async def run_bot():
	utils_module.current_prompt = database_module.get_most_recent_prompt()
	logger_module.set_log_file(utils_module.log_file_path)
	logger_module.set_debug_level(database_module.get_debug_level())
	database_module.init_db()
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
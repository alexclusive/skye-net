import os
import sys
import platform
import signal
import discord

import handlers.utils as utils_module
import handlers.logger as logger_module
import handlers.database as database_module
import handlers.tasks as tasks_module
import handlers.helpers.train_game as train_game_module
import handlers.helpers.etymology as etymology_module

from handlers.logger import LOG_SETUP, LOG_INFO, LOG_DETAIL, LOG_EXTRA_DETAIL

nice_try = "Guess you're not cool enough for this one :)"

# Owner
async def die(interaction:discord.Interaction):
	if not utils_module.is_owner(interaction):
		await interaction.followup.send(nice_try)
		return
	logger_module.log(LOG_SETUP, "Shutting down...")
	await interaction.followup.send("Going to sleep... Goodnight!")
	await utils_module.discord_bot.close()
	utils_module.received_shutdown = True
	
	if platform.system() == "Windows":
		os.kill(os.getpid(), signal.SIGTERM)
	else:
		os.kill(os.getpid(), signal.SIGKILL)

# Owner
async def set_debug_level(interaction:discord.Interaction, level:int):
	if not utils_module.is_owner(interaction):
		await interaction.followup.send(nice_try)
		return
	if level < LOG_SETUP or level > LOG_EXTRA_DETAIL:
		await interaction.followup.send("Debug level must be between 0 and 3")
		return
	logger_module.debug_level = level
	await interaction.followup.send(f"Debug level set to {level}")

# Admin
async def get_opt_out_users(interaction:discord.Interaction):
	if not utils_module.is_owner(interaction):
		await interaction.followup.send(nice_try)
		return
	opted_out_users = database_module.get_all_opt_out_users()
	await interaction.followup.send(f"Opted out users: {opted_out_users}")
	print(f"{interaction.user.name} requested opted out users: {opted_out_users}")

# Admin
async def force_trusted_roles(interaction:discord.Interaction):
	if not utils_module.is_owner(interaction):
		await interaction.followup.send(nice_try)
		return
	await tasks_module.add_trusted_roles_task()
	await interaction.followup.send("Forced daily tasks")

# Admin
async def force_audit_log(interaction:discord.Interaction, days_to_check:int=1):
	if not utils_module.is_owner(interaction):
		await interaction.followup.send(nice_try)
		return
	await tasks_module.audit_log_task(days_to_check)
	await interaction.followup.send("Forced audit tasks")

# Admin
async def enter_train_fact(interaction:discord.Interaction, fact:str):
	if not utils_module.is_admin(interaction):
		await interaction.followup.send(nice_try)
		return
	database_module.insert_train_fact(fact)
	await interaction.followup.send("Train fact entered")

# Admin
async def remove_train_fact(interaction:discord.Interaction, fact_num:int):
	if not utils_module.is_admin(interaction):
		await interaction.followup.send(nice_try)
		return
	fact = database_module.remove_train_fact(fact_num)
	if fact is None:
		await interaction.followup.send(f"Fact {fact_num} not found")
	else:
		await interaction.followup.send(f"Train fact removed\n{fact}")

# Admin
async def get_train_facts(interaction:discord.Interaction):
	if not utils_module.is_admin(interaction):
		await interaction.followup.send(nice_try)
		return
	facts_embed = database_module.get_all_train_facts()
	await interaction.followup.send(embed=facts_embed)

# Admin
async def get_reactions(interaction:discord.Interaction):
	if not utils_module.is_admin(interaction):
		await interaction.followup.send(nice_try)
		return
	reactions = database_module.get_all_reactions()
	await interaction.followup.send(f"Reactions: {reactions}")

# Admin
async def insert_reaction(interaction:discord.Interaction, trigger:str, emoji_1:str, emoji_2:str="", emoji_3:str=""):
	if not utils_module.is_admin(interaction):
		await interaction.followup.send(nice_try)
		return
	database_module.insert_reaction(trigger, emoji_1, emoji_2, emoji_3)
	await interaction.followup.send(f"Reaction inserted for trigger '{trigger}': {emoji_1} {emoji_2} {emoji_3}")

# Admin
async def remove_reaction(interaction:discord.Interaction, trigger:str):
	if not utils_module.is_admin(interaction):
		await interaction.followup.send(nice_try)
		return
	reaction = database_module.remove_reaction(trigger)
	if reaction is None:
		await interaction.followup.send(f"Reaction for trigger '{trigger}' not found")
	else:
		emoji_1, emoji_2, emoji_3 = reaction
		await interaction.followup.send(f"Reaction removed for trigger '{trigger}': {emoji_1} {emoji_2} {emoji_3}")

# Admin
async def get_log_channels(interaction:discord.Interaction):
	if not utils_module.is_admin(interaction):
		await interaction.followup.send(nice_try)
		return
	log_channels = database_module.get_logging_channels(interaction.guild_id)
	if log_channels is None:
		await interaction.followup.send("No log channels found")
	else:
		message, member, guild = log_channels
		await interaction.followup.send(f"Log channels:\nMessages: {message}\nMembers: {member}\nGuild: {guild}")

# Admin
async def set_log_channels(interaction:discord.Interaction, message:discord.TextChannel=None, member:discord.TextChannel=None, guild:discord.TextChannel=None):
	if not utils_module.is_admin(interaction):
		await interaction.followup.send(nice_try)
		return
	database_module.insert_logging_channels(interaction.guild_id, message, member, guild)
	response = ""
	if message:
		response += f"Messages logging channel set to {message}\n"
	if member:
		response += f"Members logging channel set to {member}\n"
	if guild:
		response += f"Guild logging channel set to {guild}\n"
	
	if len(response) == 0:
		await interaction.followup.send("No logging channels set")
	else:
		await interaction.followup.send(response)

# Admin
async def get_banned_users(interaction:discord.Interaction):
	if not utils_module.is_admin(interaction):
		await interaction.followup.send(nice_try)
		return
	banned_users = database_module.get_all_banned_users()
	await interaction.followup.send(f"Banned users: {banned_users}")

# Admin
async def ban_user(interaction:discord.Interaction, user_id:int):
	if not utils_module.is_admin(interaction):
		await interaction.followup.send(nice_try)
		return
	database_module.ban_user(user_id)
	await interaction.followup.send(f"User {user_id} banned")

# Admin
async def unban_user(interaction:discord.Interaction, user_id:int):
	if not utils_module.is_admin(interaction):
		await interaction.followup.send(nice_try)
		return
	database_module.unban_user(user_id)
	await interaction.followup.send(f"User {user_id} unbanned")

# Admin
async def get_important_roles(interaction:discord.Interaction):
	if not utils_module.is_admin(interaction):
		await interaction.followup.send(nice_try)
		return
	important_roles = database_module.get_important_roles(interaction.guild_id)
	if important_roles is None:
		await interaction.followup.send("No important roles found")
	else:
		welcomed, trusted, trusted_days = important_roles
		await interaction.followup.send(f"Important roles:\nWelcomed: {welcomed}\nTrusted: {trusted}\nTrusted days: {trusted_days}")

# Admin
async def set_important_roles(interaction:discord.Interaction, welcomed:discord.Role, trusted:discord.Role, trusted_days:int):
	if not utils_module.is_admin(interaction):
		await interaction.followup.send(nice_try)
		return
	database_module.insert_important_roles(interaction.guild_id, welcomed, trusted, trusted_days)
	await interaction.followup.send(f"Important roles set\nWelcomed: {welcomed}\nTrusted: {trusted}\nTrusted days: {trusted_days}")

# Admin
async def get_todo(interaction:discord.Interaction):
	if not utils_module.is_admin(interaction):
		await interaction.followup.send(nice_try)
		return
	todo = database_module.get_all_todo_items()
	embed = discord.Embed(title="Todo List", colour=0xffffff)
	embed.description = ""
	for item in todo:
		embed.description += f"{item[0]}- {item[1]}\n"
	if len(embed.description):
		await interaction.followup.send(embed=embed)
	else:
		await interaction.followup.send("Todo List Empty")

# Admin
async def add_todo(interaction:discord.Interaction, todo:str):
	if not utils_module.is_admin(interaction):
		await interaction.followup.send(nice_try)
		return
	database_module.insert_todo_item(todo)
	await interaction.followup.send(f"Todo added: {todo}")

# Admin
async def remove_todo(interaction:discord.Interaction, todo_id:int):
	if not utils_module.is_admin(interaction):
		await interaction.followup.send(nice_try)
		return
	database_module.remove_todo_item(todo_id)
	await interaction.followup.send(f"Todo {todo_id} removed")

async def ping(interaction:discord.Interaction):
	latency = round(utils_module.discord_bot.latency * 1000)
	await interaction.followup.send(f"Ponged your ping in {latency}ms")

async def train_game(interaction:discord.Interaction, number, target, use_power, use_modulo):
	try:
		target = int(target)
		number_str = str(number)
		if len(number_str) != 4:
			await interaction.followup.send("`" + number_str + "` is not valid for the train game. Please give a four digit number (0000-9999).")
			return
		a = int(number_str[0]) # these will raise an exception if they can't convert
		b = int(number_str[1])
		c = int(number_str[2])
		d = int(number_str[3])
	except Exception as e:
		print(f"Train game: error converting. {e}")
		await utils_module.error_message(interaction)
		return
	await train_game_module.attempt_train_game(interaction, number, a, b, c, d, target, use_power, use_modulo)

async def train_game_rules(interaction:discord.Interaction):
	rules = "In each car for every train, there is a four digit number.\n"
	rules += "We break down the number into four separate digits, and perform simple arithmetic operations to reach a specified target.\n"
	rules += "In general, the target number is 10 (but you can also use any other positive integer).\n"
	rules += "By default, the operations are: addition (+), subtraction (-), multiplication (*), and division (/).\n"
	rules += "Optionally, you can also use power/exponentiation (^), and modulo (%).\n"

	embed = discord.Embed(title="Train Game Rules", colour=0xffffff, description=rules)

	await interaction.followup.send(embed=embed)

async def train_fact(interaction:discord.Interaction):
	fact = database_module.get_random_train_fact()
	if fact is None:
		await interaction.followup.send("No train facts found :(")
	embed = discord.Embed(title="Train Fact", description=fact, colour=0xffffff)
	await interaction.followup.send(embed=embed)

async def reset_prompt(interaction:discord.Interaction):
	utils_module.current_prompt = utils_module.initial_prompt
	await interaction.followup.send("Prompt reset")

async def set_prompt(interaction:discord.Interaction, new_prompt):
	utils_module.current_prompt = new_prompt
	database_module.insert_prompt(new_prompt, interaction.user.id)
	await interaction.followup.send(f"Prompt set to '{new_prompt}'")

async def etymology(interaction:discord.Interaction, argument):
	await interaction.followup.send(etymology_module.get_etymology(argument))

async def opt_out_reactions(interaction:discord.Interaction):
	database_module.opt_out(interaction.user.id)
	await interaction.followup.send("You have opted out of reactions")

async def opt_in_reactions(interaction:discord.Interaction):
	database_module.opt_in(interaction.user.id)
	await interaction.followup.send("You have opted in to reactions")
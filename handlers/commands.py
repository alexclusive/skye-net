import os
import sys
import platform
import signal
import discord

import handlers.utils as utils_module
import handlers.database as database_module
import handlers.tasks as tasks_module
import handlers.helpers.train_game as train_game_module
import handlers.helpers.etymology as etymology_module

nice_try = "Guess you're not cool enough for this one :)"

# Owner
async def die(interaction:discord.Interaction):
	if not utils_module.is_owner(interaction):
		await interaction.followup.send(nice_try)
		return
	await interaction.followup.send("Going to sleep... Goodnight!")
	await utils_module.discord_bot.close()
	
	if platform.system() == "Windows":
		os.kill(os.getpid(), signal.SIGTERM)
	else:
		os.kill(os.getpid(), signal.SIGKILL)

# Owner
async def restart(interaction:discord.Interaction):
	if not utils_module.is_owner(interaction):
		await interaction.followup.send(nice_try)
		return
	await interaction.followup.send("Restarting the bot...", ephemeral=True)

	try:
		await utils_module.discord_bot.close()
		os.execl(sys.executable, sys.executable, *sys.argv)
	except Exception as e:
		await interaction.followup.send(f"Failed to restart: {e}")

# Admin
async def delete_message_by_id(interaction:discord.Interaction, id):
	if not utils_module.is_admin(interaction):
		await interaction.followup.send(nice_try)
		return
	try:
		channel = interaction.channel
		message = await channel.fetch_message(id)
		await message.delete()
		await interaction.followup.send("Deleted", ephemeral=True)
	except Exception as e:
		await interaction.followup.send(e)

# Admin
async def get_opt_out_users(interaction:discord.Interaction):
	if not utils_module.is_admin(interaction):
		await interaction.followup.send(nice_try)
		return
	opted_out_users = database_module.get_all_opt_out_users()
	await interaction.followup.send(f"Opted out users: {opted_out_users}")

# Admin
async def force_daily_tasks(interaction:discord.Interaction):
	if not utils_module.is_admin(interaction):
		await interaction.followup.send(nice_try)
		return
	await tasks_module.daily_tasks(force=True)
	await interaction.followup.send("Forced daily tasks")

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
	rules = "Train game rules:\n"
	rules += "In each car for every train, there is a four digit number.\n"
	rules += "We break down the number into four separate digits, and perform simple arithmetic operations to reach a specified target.\n"
	rules += "In general, the target number is 10 (but you can also use any other positive integer).\n"
	rules += "By default, the operations are: addition (+), subtraction (-), multiplication (*), and division (/).\n"
	rules += "Optionally, you can also use power/exponentiation (^), and modulo (%).\n"

	await interaction.followup.send(rules)

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
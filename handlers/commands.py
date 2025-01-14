import os
import sys
import platform
import signal
import discord

import handlers.utils as utils_module
import helpers.train_game as train_game_module

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
	train_game_module.attempt_train_game(interaction, number, a, b, c, d, target, use_power, use_modulo)

async def train_game_rules(interaction:discord.Interaction):
	rules = "Train game rules:\n"
	rules += "In each car for every train, there is a four digit number.\n"
	rules += "We break down the number into four separate digits, and perform simple arithmetic operations to reach a specified target.\n"
	rules += "In general, the target number is 10 (but you can also use any other positive integer).\n"
	rules += "By default, the operations are: addition (+), subtraction (-), multiplication (*), and division (/).\n"
	rules += "Optionally, you can also use power/exponentiation (^), and modulo (%).\n"

	await interaction.followup.send(rules)

async def train_fact(interaction:discord.Interaction):
	await interaction.followup.send("TODO, sorry!")

async def reset_prompt(interaction:discord.Interaction):
	utils_module.current_prompt = utils_module.initial_prompt
	await interaction.followup.send("Prompt reset")

async def set_prompt(interaction:discord.Interaction, new_prompt):
	utils_module.current_prompt = new_prompt
	await interaction.followup.send(f"Prompt set to '{new_prompt}'")
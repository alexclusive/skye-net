import sys
import asyncio
import threading
import discord

import handlers.utils as utils_module
import handlers.commands as commands_module
import handlers.database as database_module
import handlers.messages as messages_module
import handlers.tasks as tasks_module

'''
	Commands
	[Owner] is for just the bot owner
	[Admin] is for anyone with administrator permissions
'''
@utils_module.discord_bot.tree.command(description="[Owner] Shutdown the bot")
async def kill(interaction:discord.Interaction):
	await interaction.response.defer()
	await commands_module.die(interaction)
	
@utils_module.discord_bot.tree.command(name="restart", description="[Owner] Restart the bot")
async def restart(interaction:discord.Interaction):
	await interaction.response.defer(ephemeral=True)
	await commands_module.restart(interaction)

@utils_module.discord_bot.tree.command(description="[Admin] Delete a message by ID")
async def delete_message_by_id(interaction:discord.Interaction, id:str):
	await interaction.response.defer(ephemeral=True)
	await commands_module.delete_message_by_id(interaction, id)

@utils_module.discord_bot.tree.command(description="[Admin] Get list of user IDs that have opted out of reactions")
async def get_opt_out_users(interaction:discord.Interaction):
	await interaction.response.defer(ephemeral=True)
	await commands_module.get_opt_out_users(interaction)

@utils_module.discord_bot.tree.command(description="[Admin] Force daily tasks")
async def force_daily_tasks(interaction:discord.Interaction):
	await interaction.response.defer()
	await commands_module.force_daily_tasks(interaction)

@utils_module.discord_bot.tree.command(description="Check the bot's ping")
async def ping(interaction:discord.Interaction):
	await interaction.response.defer()
	await commands_module.ping(interaction)

@utils_module.discord_bot.tree.command(description="Train game - get to [target] using (+-*/) and optionally (^%)")
async def train_game(
	interaction:discord.Interaction,
	number:int,  # The starting number for the game - four digits
	target:int = 10,  # The target number to reach - default 10
	use_power:str = "True",  # Allow usage of the power (^) operation - default True
	use_modulo:str = "True",  # Allow usage of the modulo (%) operation - default True
):
	use_power_bool = "true" in use_power.lower()
	use_modulo_bool = "true" in use_modulo.lower()
	await interaction.response.defer()
	await commands_module.train_game(interaction, number, target, use_power_bool, use_modulo_bool)

@utils_module.discord_bot.tree.command(description="Train game - explanation of rules")
async def train_game_rules(interaction:discord.Interaction):
	await interaction.response.defer()
	await commands_module.train_game_rules(interaction)

@utils_module.discord_bot.tree.command(description="Train fun-fact")
async def train_fact(interaction:discord.Interaction):
	await interaction.response.defer()
	await commands_module.train_fact(interaction)

@utils_module.discord_bot.tree.command(description="Reset the bot's prompt")
async def reset_prompt(interaction:discord.Interaction):
	await interaction.response.defer()
	await commands_module.reset_prompt(interaction)

@utils_module.discord_bot.tree.command(description="Set the bot's prompt")
async def set_prompt(interaction:discord.Interaction, prompt:str):
	await interaction.response.defer()
	await commands_module.set_prompt(interaction, prompt)

# etymology: argument is the word to get etymology for, plus an optional 'tree' argument to print the tree
@utils_module.discord_bot.tree.command(description="Get the etymology of a word")
async def etymology(interaction:discord.Interaction, argument:str):
	await interaction.response.defer()
	await commands_module.etymology(interaction, argument)

@utils_module.discord_bot.tree.command(description="Opt out of the bot's reactions")
async def opt_out(interaction:discord.Interaction):
	await interaction.response.defer()
	await commands_module.opt_out_reactions(interaction)

@utils_module.discord_bot.tree.command(description="Opt in to the bot's reactions")
async def opt_in(interaction:discord.Interaction):
	await interaction.response.defer()
	await commands_module.opt_in_reactions(interaction)

'''
	Events
'''
@utils_module.discord_bot.event
async def on_ready():
	await utils_module.discord_bot.change_presence(activity=discord.Game(name="!help"))
	await utils_module.discord_bot.tree.sync()
	print(f"{utils_module.discord_bot.user} is ready and online :P")
	asyncio.create_task(daily_thread_function())

@utils_module.discord_bot.event
async def on_message(message):
	await messages_module.message(message)

'''
	Threading
'''
async def daily_thread_function():
	while True:
		await tasks_module.daily_tasks()
		await asyncio.sleep(60*60*24) # 1 day

'''
	Discord handling
'''
def send_output_to_discord(message):
	message = message.strip()
	if message:
		channel = utils_module.discord_bot.get_channel(utils_module.stdout_channel)
		if channel:
			if len(message) > 2000: # discord won't allow longer than 2000 characters, so split it up
				for i in range(0, len(message), 2000):
					chunk = message[i:i+2000]
					asyncio.ensure_future(channel.send(chunk))
			else:
				asyncio.ensure_future(channel.send(message))

async def run_bot():
	sys.stdout.write = send_output_to_discord
	sys.stderr.write = send_output_to_discord

	utils_module.fill_banned_users()
	utils_module.fill_emojis()
	database_module.init_db()
	utils_module.current_prompt = database_module.get_most_recent_prompt()

	try:
		await utils_module.discord_bot.start(utils_module.token)
	except KeyboardInterrupt:
		pass

asyncio.run(run_bot())
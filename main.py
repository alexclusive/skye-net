import os
import sys
import asyncio
import discord
import threading

from assets.core_utils import discord_bot, token, stdout_channel, connect_rich_presence
import assets.events as events
from assets.cmds import cmd_misc, cmd_owner

@discord_bot.event
async def on_ready():
	await discord_bot.tree.sync()
	print(f"{discord_bot.user} is ready and online!")

'''
	Slash commands that can be used by the owner
'''
@discord_bot.tree.command(description="[Owner] Shutdown the bot")
async def kill(interaction:discord.Interaction):
	await interaction.response.defer()
	await cmd_owner.die(interaction)
	
@discord_bot.tree.command(name="restart", description="[Owner] Restart the bot")
async def restart(interaction:discord.Interaction):
	await interaction.response.defer(ephemeral=True)
	await cmd_owner.restart(interaction)

@discord_bot.tree.command(description="[Owner] Delete a message by ID")
async def delete_message_by_id(interaction:discord.Interaction, id:str):
	await interaction.response.defer(ephemeral=True)  # Defer the response
	await cmd_owner.delete_message_by_id(interaction, id)  # Call the handler for the actual deletion

'''
	Slash commands that can be used by anyone
'''
@discord_bot.tree.command(description="Check the bot's ping")
async def ping(interaction:discord.Interaction):
	await interaction.response.defer()
	await cmd_misc.ping(interaction)

# explain train game

@discord_bot.tree.command(description="Train game - get to [target] using (+-*/) and optionally (^%)")
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
	await cmd_misc.train_game(interaction, number, target, use_power_bool, use_modulo_bool)

@discord_bot.tree.command(description="Reset the bot's prompt")
async def reset_prompt(interaction:discord.Interaction):
	await interaction.response.defer()
	await events.reset_prompt(interaction)

@discord_bot.tree.command(description="Set the bot's prompt")
async def set_prompt(interaction:discord.Interaction, prompt:str):
	await interaction.response.defer()
	await events.set_prompt(interaction, prompt)

'''
	Discord events
'''
@discord_bot.event
async def on_message(message):
	await events.message(message)

'''
	Discord handling
'''
def send_output_to_discord(message):
	message = message.strip()
	if message:
		channel = discord_bot.get_channel(stdout_channel)
		if channel: # write to stdout_channel
			if len(message) > 2000: # discord won't allow longer than 2000 characters, so split it up
				for i in range(0, len(message), 2000):
					chunk = message[i:i+2000]
					asyncio.ensure_future(channel.send(chunk))
			else:
				asyncio.ensure_future(channel.send(message))

async def run_bot():
  fill_banned_users()
	sys.stdout.write = send_output_to_discord
	sys.stderr.write = send_output_to_discord

	try:
		await connect_rich_presence()
		await discord_bot.start(token)
	except KeyboardInterrupt:
		pass

asyncio.run(run_bot())
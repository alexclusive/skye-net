import os
import sys
import asyncio
from discord.commands import Option

from assets.core_utils import discord_client, token, stdout_channel
import assets.events as events
from assets.cmds import cmd_misc, cmd_owner

@discord_client.event
async def on_ready():
	print(f"{discord_client.user} is ready and online!")

'''
	Slash commands that can be used by the owner
'''
@discord_client.slash_command(description="[Owner] Restart the bot")
async def restart(ctx):
	await ctx.defer(ephemeral=True)
	await cmd_owner.restart(ctx)

@discord_client.slash_command(description="[Owner] Delete a message by ID")
async def delete_message_by_id(ctx, id):
	await ctx.defer(ephemeral=True)
	await cmd_owner.delete_message_by_id(ctx, id)

'''
	Slash commands that can be used by anyone
'''
@discord_client.slash_command(description="Check the bot's ping")
async def ping(ctx):
	await ctx.defer()
	await cmd_misc.ping(ctx)

@discord_client.slash_command(description="Train game - get to [target] using (+-*/) and optionally (^%)")
async def train_game(
	ctx,
	number: Option(int, "The starting number for the game - four digits"), # type: ignore
	target: Option(int, "The target number to reach - integer - default 10", default=10), # type: ignore
	use_power: Option(bool, "Allow usage of the power (^) operation - True/False - default True", default=True), # type: ignore
	use_modulo: Option(bool, "Allow usage of the modulo (%) operation - True/False - default True", default=True), # type: ignore
):
	await ctx.defer()
	await cmd_misc.train_game(ctx, number, target, use_power, use_modulo)

@discord_client.slash_command(description="Reset the bot's prompt")
async def reset_prompt(ctx):
	await ctx.defer()
	await events.reset_prompt(ctx)

@discord_client.slash_command(description="Set the bot's prompt")
async def set_prompt(ctx, prompt):
	await ctx.defer()
	await events.set_prompt(ctx, prompt)

'''
	Discord events
'''
@discord_client.event
async def on_message(message):
	await events.message(message)

'''
	Discord handling
'''
def send_output_to_discord(message):
	message = message.strip()
	if message:
		channel = discord_client.get_channel(stdout_channel)
		if channel: # write to stdout_channel
			if len(message) > 2000: # discord won't allow longer than 2000 characters, so split it up
				for i in range(0, len(message), 2000):
					chunk = message[i:i+2000]
					asyncio.ensure_future(channel.send(chunk))
			else:
				asyncio.ensure_future(channel.send(message))

sys.stdout.write = send_output_to_discord
sys.stderr.write = send_output_to_discord

discord_client.run(token)
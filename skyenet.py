import asyncio
import discord
import sys

from src import commands_module as commands
from src import database_module as database
from src import events_module as events
from src import logger
from src import tasks
from src import utils
from src.handlers import spotify as spotify_handler

def _log_send_exception(task:asyncio.Task) -> None:
	try:
		task.result()
	except Exception as e:
		logger.log(logger.LOG_INFO, f"Discord send failed: {e}")

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
	if len(message) > 2000: # discord won't allow longer than 2000 characters, so split it up
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
		channel = utils.discord_bot.get_channel(utils.stdout_channel_id)
		if channel:
			send_message(channel, message)

async def run_bot():
	utils.init()
	spotify_handler.setup_spotify_credentials()
	sys.stdout.write = send_output_to_discord
	sys.stderr.write = send_output_to_discord

	try:
		logger.log(logger.LOG_SETUP, "Starting bot...")
		await utils.discord_bot.start(utils.token)
	except Exception as e:
		logger.log(logger.LOG_SETUP, "Shutting down bot...")
		if not utils.received_shutdown:
			await utils.discord_bot.close()
		print(f"Error: {e}")
		raise e

try:
	asyncio.run(run_bot())
except KeyboardInterrupt:
	pass
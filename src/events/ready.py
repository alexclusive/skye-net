import asyncio
import discord
import psutil

from .. import commands_module as commands
from .. import logger
from .. import tasks
from .. import utils

from ..commands import bingo
from ..commands import bot_admin
from ..commands import misc
from ..commands import number_facts
from ..commands import openAI
from ..commands import reactions
from ..commands import todo
from ..commands import train_facts
from ..commands import train_game

'''
 - on_ready
'''

last_terminator_presence = None
presence_update_lock = asyncio.Lock()

async def ready():
	try:
		logger.log(logger.LOG_SETUP, "Syncing discord bot tree")
		await utils.discord_bot.tree.sync() # need commands imported before we run this

		logger.log(logger.LOG_SETUP, "Updating command permissions")
		await commands.ensure_correct_permissions() # gotta be after sync, cause sync updates which guilds we're in

		_ = psutil.cpu_percent(percpu=True) # first call is always 0.0, so call it once to get actual data next time

		logger.log(logger.LOG_SETUP, "Starting up tasks")
		tasks.tasks_on_ready()

		print(f"{utils.discord_bot.user} is ready and online :P")
		await utils.discord_bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.CustomActivity("Skye-net is watching.", type=discord.ActivityType.watching))
	except Exception as e:
		logger.log(logger.LOG_INFO, f"Error in on_ready event: {e}")

async def status_update(after:discord.Member):
	activity = after.activity
	if after._user.id != utils.terminator_id:
		return

	presence = (after.status, type(activity), str(activity), getattr(activity, "name", None), getattr(activity, "details", None))
	global last_terminator_presence
	async with presence_update_lock:
		if presence == last_terminator_presence:
			return		
		last_terminator_presence = presence

		logger.log(logger.LOG_SETUP, "Shutting down...")
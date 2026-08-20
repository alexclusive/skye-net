import discord
import psutil

from .. import commands_module as commands
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

async def ready():
	await utils.discord_bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.CustomActivity("Skye-net is watching...", type=discord.ActivityType.watching))
	await utils.discord_bot.tree.sync()
	await commands.ensure_correct_permissions() # gotta be after sync, cause sync updates which guilds we're in
	print(f"{utils.discord_bot.user} is ready and online :P")
	_ = psutil.cpu_percent(percpu=True) # first call is always 0.0, so call it once to get actual data next time
	tasks.tasks_on_ready()
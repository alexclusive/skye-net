import discord

from . import logger
from . import utils
from .events import guilds as guild_events
from .events import members as member_events
from .events import messages as message_events
from .events import ready as ready_events

event_triggered_log_string = "Event triggered"

@utils.discord_bot.event
async def on_ready():
	logger.log(logger.LOG_DETAIL, event_triggered_log_string)
	await ready_events.ready()

@utils.discord_bot.event
async def on_message(message:discord.Message):
	logger.log(logger.LOG_EXTRA_DETAIL, event_triggered_log_string + f" by {message.author} in {message.channel}")
	await message_events.message(message)

@utils.discord_bot.event
async def on_message_delete(message:discord.Message):
	logger.log(logger.LOG_DETAIL, event_triggered_log_string + f" by {message.author} in {message.channel}")
	await message_events.message_deleted(message)

@utils.discord_bot.event
async def on_guild_channel_create(channel:discord.abc.GuildChannel):
	logger.log(logger.LOG_DETAIL, event_triggered_log_string + f" in {channel.guild.name}")
	await guild_events.channel_create(channel)

@utils.discord_bot.event
async def on_guild_channel_delete(channel:discord.abc.GuildChannel):
	logger.log(logger.LOG_DETAIL, event_triggered_log_string + f" in {channel.guild.name}")
	await guild_events.channel_delete(channel)

@utils.discord_bot.event
async def on_guild_role_create(role:discord.Role):
	logger.log(logger.LOG_DETAIL, event_triggered_log_string + f" in {role.guild.name}")
	await guild_events.role_create(role)

@utils.discord_bot.event
async def on_guild_role_delete(role:discord.Role):
	logger.log(logger.LOG_DETAIL, event_triggered_log_string + f" in {role.guild.name}")
	await guild_events.role_delete(role)

@utils.discord_bot.event
async def on_member_join(member:discord.Member):
	logger.log(logger.LOG_DETAIL, event_triggered_log_string + f" in {member.guild.name}")
	await member_events.member_join(member)

@utils.discord_bot.event
async def on_member_remove(member:discord.Member):
	logger.log(logger.LOG_DETAIL, event_triggered_log_string + f" in {member.guild.name}")
	await member_events.member_remove(member)

@utils.discord_bot.event
async def on_member_update(before:discord.Member, after:discord.Member):
	# nickname / roles / guild avatar
	logger.log(logger.LOG_DETAIL, event_triggered_log_string + f" in {after.guild.name}")
	await member_events.member_update(before, after)

@utils.discord_bot.event
async def on_member_ban(member:discord.Member):
	logger.log(logger.LOG_DETAIL, f"Event triggered in {member.guild.name}")
	await member_events.member_ban(member)

@utils.discord_bot.event
async def on_guild_join(guild:discord.Guild):
	logger.log(logger.LOG_DETAIL, event_triggered_log_string + f" in {guild.name}")
	await guild_events.guild_join(guild)

@utils.discord_bot.event
async def on_guild_remove(guild:discord.Guild):
	logger.log(logger.LOG_DETAIL, event_triggered_log_string + f" in {guild.name}")
	await guild_events.guild_remove(guild)
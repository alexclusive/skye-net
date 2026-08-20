import discord
import duckdb

from .. import logger
from .. import utils

'''
	logging_channels
		guild_id TEXT PRIMARY KEY,
		message_channel_id TEXT,
		member_channel_id TEXT,
		guild_channel_id TEXT,
		PRIMARY KEY (guild_id)
'''

def get_logging_channels(guild_id):
	'''
		Return the logging channels for a guild
	'''
	utils.database_conn = duckdb.connect(utils.database_name)
	result = utils.database_conn.execute("SELECT message_channel_id, member_channel_id, guild_channel_id FROM logging_channels WHERE guild_id = ?", (guild_id,)).fetchall()
	utils.database_conn.close()
	return result if result else None

def insert_logging_channels(guild_id, message_channel:discord.TextChannel=None, member_channel:discord.TextChannel=None, guild_channel:discord.TextChannel=None):
	'''
		Insert the logging channels for a guild
		If guild already exists, update the channels
		Only update the channels that are not None
	'''
	message_channel_id = message_channel.id if message_channel else None
	member_channel_id = member_channel.id if member_channel else None
	guild_channel_id = guild_channel.id if guild_channel else None
	
	logger.log(logger.LOG_INFO, f"Updating logging channels for guild {guild_id}. Message >{message_channel_id}<. Member >{member_channel_id}<. Guild >{guild_channel_id}<.")
	
	utils.database_conn = duckdb.connect(utils.database_name)
	result = utils.database_conn.execute("SELECT * FROM logging_channels WHERE guild_id = ?", (guild_id,)).fetchall()
	if result:
		if message_channel_id:
			utils.database_conn.execute("UPDATE logging_channels SET message_channel_id = ? WHERE guild_id = ?", (message_channel_id, guild_id))
		if member_channel_id:
			utils.database_conn.execute("UPDATE logging_channels SET member_channel_id = ? WHERE guild_id = ?", (member_channel_id, guild_id))
		if guild_channel_id:
			utils.database_conn.execute("UPDATE logging_channels SET guild_channel_id = ? WHERE guild_id = ?", (guild_channel_id, guild_id))
	else:
		utils.database_conn.execute("INSERT INTO logging_channels VALUES (?, ?, ?, ?)", (guild_id, message_channel_id, member_channel_id, guild_channel_id))

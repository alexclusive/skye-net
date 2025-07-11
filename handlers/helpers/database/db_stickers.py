import duckdb
import discord
from datetime import datetime
from typing import Optional

import handlers.utils as utils_module
import handlers.logger as logger_module

from handlers.logger import LOG_SETUP, LOG_INFO, LOG_DETAIL, LOG_EXTRA_DETAIL

'''
	stickers
		guild_id TEXT,
		sticker_id INTEGER,
		sticker_name TEXT,
		PRIMARY KEY (guild_id, sticker_id)
'''

def get_all_stickers():
	'''
		Return a dict[str, list] of guild_id: [sticker, ...]
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT guild_id, sticker_id FROM stickers").fetchall()
	utils_module.database_conn.close()
	if not result:
		return {}
	
	guild_stickers = {} # dict[str, list]
	for row in result:
		if row[0] not in guild_stickers:
			guild_stickers[row[0]] = [] # make new list for guild if not seen guild yet

		sticker = utils_module.discord_bot.get_sticker(int(row[1]))
		if sticker:
			guild_stickers[row[0]].append(sticker) # add sticker to guild's sticker list
	return guild_stickers

def get_all_stickers_for_guild(guild_id:int):
	'''
		Return a list of stickers in a guild
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT guild_id, sticker_id FROM stickers WHERE guild_id = ?", (guild_id,)).fetchall()
	utils_module.database_conn.close()
	if not result:
		return []
	
	stickers = []
	for row in result:
		sticker = utils_module.discord_bot.get_sticker(int(row[1]))
		if sticker:
			stickers.append(sticker)
		else:
			logger_module.log(LOG_INFO, f"Sticker with id {row[1]} not found in guild {guild_id}.")
	return stickers

def insert_sticker(guild_id:int, sticker_name:str, sticker_id:str):
	'''
		Insert a sticker into the database
		If the sticker already exists, update it
	'''
	try:
		logger_module.log(LOG_INFO, f"Inserting sticker >{sticker_name}< with id {sticker_id} for guild {guild_id}.")
		utils_module.database_conn = duckdb.connect(utils_module.database_name)
		utils_module.database_conn.execute("INSERT OR REPLACE INTO stickers VALUES (?, ?, ?)", (guild_id, sticker_id, sticker_name))
		utils_module.database_conn.close()
		logger_module.log(LOG_DETAIL, f"Inserted sticker >{sticker_name}< with id {sticker_id} for guild {guild_id}.")
	except Exception as e:
		print(f"Error inserting sticker: {e}")
		utils_module.database_conn.close()

def remove_sticker(guild_id:int, sticker_id:str):
	'''
		Remove a sticker from the database
	'''
	logger_module.log(LOG_INFO, f"Removing sticker with id {sticker_id} for guild {guild_id}.")
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("DELETE FROM stickers WHERE guild_id = ? AND sticker_id = ?", (guild_id, sticker_id))
	utils_module.database_conn.close()
	logger_module.log(LOG_DETAIL, f"Removed sticker with id {sticker_id} for guild {guild_id}.")
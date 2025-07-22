import duckdb
import discord
from random import shuffle
from datetime import datetime
from typing import Optional

import handlers.utils as utils_module
import handlers.logger as logger_module

from handlers.logger import LOG_SETUP, LOG_INFO, LOG_DETAIL, LOG_EXTRA_DETAIL

'''
	bingo_template
		guild_id TEXT,
		bingo_name TEXT,
		free_space BOOLEAN,
		items TEXT,
		PRIMARY KEY (guild_id, bingo_name)

	bingo_cards (
		guild_id TEXT,
		bingo_name TEXT,
		user_id TEXT,
		card_data TEXT,
		PRIMARY KEY (guild_id, bingo_name, user_id)
	)
'''

def get_all_bingo_templates() -> dict: # dict[list[tuple]]
	'''
		Get all bingo templates from the database
		Returns a dictionary with guild IDs as keys and a list of bingo templates as values.
	'''
	logger_module.log(LOG_INFO, "Getting all bingo templates.")
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT guild_id, bingo_name, free_space, items FROM bingo_template").fetchall()
	utils_module.database_conn.close()

	templates = {}
	for row in result:
		guild_id = row[0]
		template = row[1:]
		if guild_id not in templates:
			templates[guild_id] = []
		templates[guild_id].append(template)

	return templates

def get_all_bingo_templates_for_guild(guild_id:str) -> list: # list[tuple[str, bool, str]]
	'''
		Get all bingo templates for a specific guild
	'''
	logger_module.log(LOG_INFO, f"Getting all bingo templates for guild {guild_id}.")
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT bingo_name, free_space, items FROM bingo_template WHERE guild_id = ?", (guild_id,)).fetchall()
	utils_module.database_conn.close()
	return result

def does_bingo_template_exist(guild_id:str, bingo_name:str) -> bool:
	'''
		Check if a bingo template exists for a specific guild and bingo name
	'''
	bingo_name = bingo_name.lower()
	logger_module.log(LOG_INFO, f"Checking if bingo template '{bingo_name}' exists for guild {guild_id}.")
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT COUNT(*) FROM bingo_template WHERE guild_id = ? AND bingo_name = ?", (guild_id, bingo_name)).fetchone()
	utils_module.database_conn.close()
	return result[0] > 0

def get_shuffled_bingo_template_items(guild_id:str, bingo_name:str) -> list: # list[str]
	'''
		Get a list of 25 items for a bingo card
	'''
	bingo_name = bingo_name.lower()
	logger_module.log(LOG_INFO, f"Getting bingo template items for guild {guild_id} and bingo '{bingo_name}'.")
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT free_space, items FROM bingo_template WHERE guild_id = ? AND bingo_name = ?", (guild_id, bingo_name)).fetchone()
	utils_module.database_conn.close()

	if result:
		free_space = result[0]
		items = result[1]
		items_list = items.split("\n")
		shuffle(items_list)
		if free_space:
			# Add a free space in the middle of the bingo card
			items_list = items_list[:12] + ["FREE SPACE"] + items_list[12:]
		items_list = items_list[:25]  # Cut off any extra items
	if not result or len(items) < 25:
		return []
	return items_list

def create_bingo_template(guild_id:str, bingo_name:str, free_space:bool, items:str):
	'''
		Create a bingo template in the database
	'''
	bingo_name = bingo_name.lower()
	logger_module.log(LOG_INFO, f"Creating bingo template '{bingo_name}' for guild {guild_id}.")
	print(f"Putting bingo template '{bingo_name}' into the database for guild {guild_id}.")
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("INSERT INTO bingo_template (guild_id, bingo_name, free_space, items) VALUES (?, ?, ?, ?)", (guild_id, bingo_name, free_space, items))
	utils_module.database_conn.close()

def delete_bingo_template(guild_id:str, bingo_name:str):
	'''
		Delete a bingo template from the database
	'''
	bingo_name = bingo_name.lower()
	logger_module.log(LOG_INFO, f"Deleting bingo template '{bingo_name}' for guild {guild_id}.")
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("DELETE FROM bingo_template WHERE guild_id = ? AND bingo_name = ?", (guild_id, bingo_name))
	utils_module.database_conn.execute("DELETE FROM bingo_cards WHERE guild_id = ? AND bingo_name = ?", (guild_id, bingo_name))
	utils_module.database_conn.close()

def create_bingo_card(guild_id:str, bingo_name:str, user_id:str):
	'''
		Create a bingo card in the database
	'''
	bingo_name = bingo_name.lower()
	logger_module.log(LOG_INFO, f"Creating bingo card for user {user_id} in bingo '{bingo_name}' for guild {guild_id}.")
	card_items = get_shuffled_bingo_template_items(guild_id, bingo_name)
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("INSERT OR REPLACE INTO bingo_cards (guild_id, bingo_name, user_id, card_data) VALUES (?, ?, ?, ?)", (guild_id, bingo_name, user_id, "\n".join(card_items)))
	utils_module.database_conn.close()

def has_user_created_bingo_card(guild_id:str, bingo_name:str, user_id:str) -> bool:
	'''
		Check if a user has created a bingo card for a specific bingo in a guild
	'''
	bingo_name = bingo_name.lower()
	logger_module.log(LOG_INFO, f"Checking if user {user_id} has created a bingo card for bingo '{bingo_name}' in guild {guild_id}.")
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT COUNT(*) FROM bingo_cards WHERE guild_id = ? AND bingo_name = ? AND user_id = ?", (guild_id, bingo_name, user_id)).fetchone()
	utils_module.database_conn.close()
	return result[0] > 0

def get_bingo_card(guild_id:str, bingo_name:str, user_id:str) -> list: #list[str]
	'''
		Get a bingo card from the database
		Return a list of items in the bingo card.
	'''
	bingo_name = bingo_name.lower()
	logger_module.log(LOG_INFO, f"Getting bingo card for user {user_id} in bingo '{bingo_name}' for guild {guild_id}.")
	if not has_user_created_bingo_card(guild_id, bingo_name, user_id):
		logger_module.log(LOG_DETAIL, f"User {user_id} has not created a bingo card for bingo '{bingo_name}' in guild {guild_id}.")
		return []
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT card_data FROM bingo_cards WHERE guild_id = ? AND bingo_name = ? AND user_id = ?", (guild_id, bingo_name, user_id)).fetchone()
	utils_module.database_conn.close()
	if result:
		card_data = result[0]
		return card_data.split("\n")
	else:
		logger_module.log(LOG_DETAIL, f"No bingo card found for user {user_id} in bingo '{bingo_name}' for guild {guild_id}.")
		return []
	
def update_bingo_card(guild_id:str, bingo_name:str, user_id:str, card_data:list):
	'''
		Update a bingo card in the database
	'''
	bingo_name = bingo_name.lower()
	logger_module.log(LOG_INFO, f"Updating bingo card for user {user_id} in bingo '{bingo_name}' for guild {guild_id}.")
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("UPDATE bingo_cards SET card_data = ? WHERE guild_id = ? AND bingo_name = ? AND user_id = ?", ("\n".join(card_data), guild_id, bingo_name, user_id))
	utils_module.database_conn.close()
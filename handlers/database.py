import duckdb
import discord
from datetime import datetime
from typing import Optional

import handlers.utils as utils_module
import handlers.logger as logger_module
from handlers.logger import LOG_SETUP, LOG_INFO, LOG_DETAIL, LOG_EXTRA_DETAIL

from handlers.helpers.database.db_banned_users import *
from handlers.helpers.database.db_bingo import *
from handlers.helpers.database.db_daily_tasks import *
from handlers.helpers.database.db_debug_level import *
from handlers.helpers.database.db_important_roles import *
from handlers.helpers.database.db_logging_channels import *
from handlers.helpers.database.db_prompts import *
from handlers.helpers.database.db_reaction_opt_out import *
from handlers.helpers.database.db_reactions import *
from handlers.helpers.database.db_stickers import *
from handlers.helpers.database.db_todo import *
from handlers.helpers.database.db_train_facts import *

def init_db():
	set_up_tables()
	db_initial_setup()
	logger_module.log(LOG_SETUP, "Initialised database.")

def db_initial_setup():
	'''
		Set the initial prompt and debug level
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)

	utils_module.database_conn.execute("INSERT INTO prompts VALUES (?, ?, ?)", (datetime.now(), utils_module.ownerid, utils_module.initial_prompt))
	utils_module.database_conn.execute("INSERT OR REPLACE INTO debug_level VALUES (?)", (logger_module.debug_level,))

	utils_module.database_conn.close()

def set_up_tables():
	'''
		Create the database tables if they don't already exist.
		Tables:
			banned_users
			bingo_template
			bingo_cards
			daily_tasks
			debug_level
			important_roles
			logging_channels
			prompts
			react_opt_out
			reactions
			stickers
			todo
			train_facts
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)

	utils_module.database_conn.execute('''
	CREATE TABLE IF NOT EXISTS banned_users (
		user_id TEXT,
		PRIMARY KEY (user_id)
	)
	''')

	utils_module.database_conn.execute('''
	CREATE TABLE IF NOT EXISTS bingo_template (
		guild_id TEXT,
		bingo_name TEXT,
		free_space BOOLEAN,
		items TEXT,
		PRIMARY KEY (guild_id, bingo_name)
	)
	''')

	utils_module.database_conn.execute('''
	CREATE TABLE IF NOT EXISTS bingo_cards (
		guild_id TEXT,
		bingo_name TEXT,
		user_id TEXT,
		card_data TEXT,
		PRIMARY KEY (guild_id, bingo_name, user_id)
	)
	''')

	utils_module.database_conn.execute('''
	CREATE TABLE IF NOT EXISTS daily_tasks (
		datetime TIMESTAMP,
		PRIMARY KEY (datetime)
	)
	''')

	utils_module.database_conn.execute('''
	CREATE TABLE IF NOT EXISTS debug_level (
		level INTEGER,
		PRIMARY KEY (level)
	)
	''')

	utils_module.database_conn.execute('''
	CREATE TABLE IF NOT EXISTS important_roles (
		guild_id TEXT,
		welcomed_role_id TEXT,
		trusted_role_id TEXT,
		trusted_time_days INTEGER,
		PRIMARY KEY (guild_id)
	)
	''')

	utils_module.database_conn.execute('''
	CREATE TABLE IF NOT EXISTS logging_channels (
		guild_id TEXT,
		message_channel_id TEXT,
		member_channel_id TEXT,
		guild_channel_id TEXT,
		PRIMARY KEY (guild_id)
	)
	''')

	utils_module.database_conn.execute('''
	CREATE TABLE IF NOT EXISTS prompts (
		datetime TIMESTAMP,
		user_id TEXT,
		prompt TEXT,
		PRIMARY KEY (datetime, user_id)
	)
	''')

	utils_module.database_conn.execute('''
	CREATE TABLE IF NOT EXISTS react_opt_out (
		user_id TEXT,
		PRIMARY KEY (user_id)
	)
	''')

	utils_module.database_conn.execute('''
	CREATE TABLE IF NOT EXISTS reactions (
		trigger TEXT,
		emoji_id_1 TEXT,
		emoji_id_2 TEXT,
		emoji_id_3 TEXT,
		PRIMARY KEY (trigger)
	)
	''')

	utils_module.database_conn.execute('''
	CREATE TABLE IF NOT EXISTS stickers (
		guild_id TEXT,
		sticker_id INTEGER,
		sticker_name TEXT,
		PRIMARY KEY (guild_id, sticker_id)
	)
	''')

	utils_module.database_conn.execute('''
	CREATE TABLE IF NOT EXISTS todo (
		item_num INTEGER,
		todo TEXT,
		PRIMARY KEY (item_num)
	)
	''')

	utils_module.database_conn.execute('''
	CREATE TABLE IF NOT EXISTS train_facts (
		fact_num INTEGER,
		fact TEXT,
		PRIMARY KEY (fact_num)
	)
	''')
	
	utils_module.database_conn.close()
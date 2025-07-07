import duckdb
import discord
from datetime import datetime
from typing import Optional

import handlers.utils as utils_module
import handlers.logger as logger_module
from handlers.logger import LOG_SETUP, LOG_INFO, LOG_DETAIL, LOG_EXTRA_DETAIL

from handlers.helpers.database.db_banned_users import get_all_banned_users, ban_user, unban_user
from handlers.helpers.database.db_daily_tasks import get_last_daily_task_time, insert_daily_task_time
from handlers.helpers.database.db_debug_level import get_debug_level, set_debug_level
from handlers.helpers.database.db_important_roles import get_important_roles, insert_important_roles
from handlers.helpers.database.db_logging_channels import get_logging_channels, insert_logging_channels
from handlers.helpers.database.db_prompts import get_most_recent_prompt, insert_prompt
from handlers.helpers.database.db_reaction_opt_out import get_all_opt_out_users, opt_out, opt_in
from handlers.helpers.database.db_reactions import get_all_reactions, insert_reaction, remove_reaction
from handlers.helpers.database.db_stickers import get_all_stickers, get_all_stickers_for_guild, insert_sticker, remove_sticker
from handlers.helpers.database.db_todo import get_all_todo_items, insert_todo_item, remove_todo_item
from handlers.helpers.database.db_train_facts import get_random_train_fact, get_all_train_facts, insert_train_fact, remove_train_fact

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
	utils_module.database_conn.execute("INSERT INTO debug_level VALUES (?)", (logger_module.debug_level,))

	utils_module.database_conn.close()

def set_up_tables():
	'''
		Create the database tables if they don't already exist.
		Tables:
			banned_users
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
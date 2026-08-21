import duckdb

from . import logger
from . import utils
from .database.db_bingo import *
from .database.db_blocked_users import *
from .database.db_daily_tasks import *
from .database.db_debug_level import *
from .database.db_number_fact import *
from .database.db_prompts import *
from .database.db_reaction_opt_out import *
from .database.db_todo import *
from .database.db_train_facts import *

def init_db():
	set_up_tables()
	db_initial_setup()
	logger.log(logger.LOG_SETUP, "Initialised database.")

def db_initial_setup():
	'''
		Set the initial prompt and debug level
	'''
	utils.database_conn = duckdb.connect(utils.database_name)

	# utils.database_conn.execute("INSERT INTO prompts VALUES (?, ?, ?)", (datetime.now(), utils.owner_id, utils.initial_prompt))
	utils.database_conn.execute("INSERT OR REPLACE INTO debug_level VALUES (?)", (logger.debug_level,))

	utils.database_conn.close()

def set_up_tables():
	'''
		Create the database tables if they don't already exist.
		Tables:
			bingo_cards
			bingo_template
			blocked
			daily_tasks
			debug_level
			important_roles
			logging_channels
			number_facts
			prompts
			react_opt_out
			reactions
			todo
			train_facts
	'''
	utils.database_conn = duckdb.connect(utils.database_name)

	utils.database_conn.execute('''
	CREATE TABLE IF NOT EXISTS bingo_cards (
		guild_id TEXT,
		bingo_name TEXT,
		user_id TEXT,
		card_data TEXT,
		PRIMARY KEY (guild_id, bingo_name, user_id)
	)
	''')

	utils.database_conn.execute('''
	CREATE TABLE IF NOT EXISTS bingo_template (
		guild_id TEXT,
		bingo_name TEXT,
		free_space BOOLEAN,
		items TEXT,
		PRIMARY KEY (guild_id, bingo_name)
	)
	''')

	utils.database_conn.execute('''
	CREATE TABLE IF NOT EXISTS blocked_users (
		user_id TEXT,
		PRIMARY KEY (user_id)
	)
	''')

	utils.database_conn.execute('''
	CREATE TABLE IF NOT EXISTS daily_tasks (
		datetime TIMESTAMP,
		PRIMARY KEY (datetime)
	)
	''')

	utils.database_conn.execute('''
	CREATE TABLE IF NOT EXISTS debug_level (
		level INTEGER,
		PRIMARY KEY (level)
	)
	''')

	utils.database_conn.execute('''
	CREATE TABLE IF NOT EXISTS number_facts (
		number INTEGER,
		fact TEXT,
		PRIMARY KEY (number)
	)
	''')

	utils.database_conn.execute('''
	CREATE TABLE IF NOT EXISTS prompts (
		datetime TIMESTAMP,
		user_id TEXT,
		prompt TEXT,
		PRIMARY KEY (datetime, user_id)
	)
	''')

	utils.database_conn.execute('''
	CREATE TABLE IF NOT EXISTS react_opt_out (
		user_id TEXT,
		PRIMARY KEY (user_id)
	)
	''')

	utils.database_conn.execute('''
	CREATE TABLE IF NOT EXISTS todo (
		item_num INTEGER,
		todo TEXT,
		PRIMARY KEY (item_num)
	)
	''')

	utils.database_conn.execute('''
	CREATE TABLE IF NOT EXISTS train_facts (
		fact_num INTEGER,
		fact TEXT,
		PRIMARY KEY (fact_num)
	)
	''')
	
	utils.database_conn.close()
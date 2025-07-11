import duckdb
import discord
from datetime import datetime
from typing import Optional

import handlers.utils as utils_module
import handlers.logger as logger_module

from handlers.logger import LOG_SETUP, LOG_INFO, LOG_DETAIL, LOG_EXTRA_DETAIL

'''
	prompts
		datetime TIMESTAMP,
		user_id TEXT,
		prompt TEXT,
		PRIMARY KEY (datetime, user_id)
'''

def get_most_recent_prompt():
	'''
		Return the most recent prompt in the database
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT prompt FROM prompts ORDER BY datetime DESC LIMIT 1").fetchall()
	utils_module.database_conn.close()
	if result:
		return result[0][0]
	return None

def insert_prompt(prompt, user_id):
	'''
		Insert a new prompt into the database
	'''
	logger_module.log(LOG_INFO, f"User {user_id} added prompt >{prompt}<.")
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("INSERT INTO prompts VALUES (?, ?, ?)", (datetime.now(), int(user_id), prompt))
	utils_module.database_conn.close()
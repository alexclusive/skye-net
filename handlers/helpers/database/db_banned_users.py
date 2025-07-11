import duckdb
import discord
from datetime import datetime
from typing import Optional

import handlers.utils as utils_module
import handlers.logger as logger_module

from handlers.logger import LOG_SETUP, LOG_INFO, LOG_DETAIL, LOG_EXTRA_DETAIL

'''
	banned_users
		user_id TEXT,
		PRIMARY KEY (user_id)
'''

def get_all_banned_users():
	'''
		Return a list of all user_ids that have been banned
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT user_id FROM banned_users").fetchall()
	utils_module.database_conn.close()
	return [int(row[0]) for row in result]

def ban_user(user_id):
	'''
		Insert a user_id into the banned_users table
	'''
	logger_module.log(LOG_INFO, f"Adding user {user_id} to banned list.")
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("INSERT INTO banned_users VALUES (?)", (int(user_id),))
	utils_module.database_conn.close()

def unban_user(user_id):
	'''
		Remove a user_id from the banned_users table
	'''
	logger_module.log(LOG_INFO, f"Removing user {user_id} from banned list.")
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("DELETE FROM banned_users WHERE user_id = ?", (int(user_id),))
	utils_module.database_conn.close()
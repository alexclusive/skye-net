import duckdb
import discord
from datetime import datetime
from typing import Optional

import handlers.utils as utils_module
import handlers.logger as logger_module

from handlers.logger import LOG_SETUP, LOG_INFO, LOG_DETAIL, LOG_EXTRA_DETAIL

'''
	react_opt_out
		user_id TEXT,
		PRIMARY KEY (user_id)
'''

def get_all_opt_out_users():
	'''
		Return a list of all user_ids that have opted out of reactions
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT user_id FROM react_opt_out").fetchall()
	utils_module.database_conn.close()
	return [int(row[0]) for row in result]

def opt_out(user_id):
	'''
		Insert a user_id into the react_opt_out table
	'''
	logger_module.log(LOG_INFO, f"User {user_id} opted out of reactions.")
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("INSERT INTO react_opt_out VALUES (?)", (int(user_id),))
	utils_module.database_conn.close()

def opt_in(user_id):
	'''
		Remove a user_id from the react_opt_out table
	'''
	logger_module.log(LOG_INFO, f"User {user_id} opted in to reactions.")
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("DELETE FROM react_opt_out WHERE user_id = ?", (int(user_id),))
	utils_module.database_conn.close()
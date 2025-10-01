import duckdb
import discord
from datetime import datetime
from typing import Optional

import handlers.utils as utils_module
import handlers.logger as logger_module

from handlers.logger import LOG_SETUP, LOG_INFO, LOG_DETAIL, LOG_EXTRA_DETAIL

'''
	debug_level
		level INTEGER,
		PRIMARY KEY (level)
'''

def get_debug_level():
	'''
		Return the debug level
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT level FROM debug_level").fetchone()
	utils_module.database_conn.close()
	level = int(result[0]) if result else LOG_EXTRA_DETAIL
	if level < LOG_SETUP or level > LOG_EXTRA_DETAIL:
		level = LOG_EXTRA_DETAIL
	return level

def set_debug_level(level:int):
	'''
		Set the first entry in the debug_level table to the given level, whether it exists or not
	'''
	logger_module.log(LOG_INFO, f"Setting debug level to {level}.")
	if level < LOG_SETUP or level > LOG_EXTRA_DETAIL:
		level = LOG_EXTRA_DETAIL
		logger_module.log(LOG_INFO, f"Invalid debug level {level} set to {LOG_EXTRA_DETAIL}.")
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("INSERT OR REPLACE INTO debug_level VALUES (?)", (level,))
	utils_module.database_conn.close()
import duckdb

from .. import logger
from .. import utils

'''
	debug_level
		level INTEGER,
		PRIMARY KEY (level)
'''

def get_debug_level():
	'''
		Return the debug level
	'''
	logger.log(logger.LOG_INFO, "Getting debug level")
	utils.database_conn = duckdb.connect(utils.database_file)
	result = utils.database_conn.execute("SELECT level FROM debug_level").fetchone()
	utils.database_conn.close()
	level = int(result[0]) if result else logger.LOG_EXTRA_DETAIL
	if level < logger.LOG_SETUP or level > logger.LOG_EXTRA_DETAIL:
		level = logger.LOG_EXTRA_DETAIL
	return level

def set_debug_level(level:int):
	'''
		Set the first entry in the debug_level table to the given level, whether it exists or not
	'''
	logger.log(logger.LOG_INFO, f"Setting debug level to {level}")
	if level < logger.LOG_SETUP or level > logger.LOG_EXTRA_DETAIL:
		logger.log(logger.LOG_INFO, f"Invalid debug level {level}, setting to {logger.LOG_EXTRA_DETAIL}")
		level = logger.LOG_EXTRA_DETAIL
	utils.database_conn = duckdb.connect(utils.database_file)
	utils.database_conn.execute("INSERT OR REPLACE INTO debug_level VALUES (?)", (level,))
	utils.database_conn.close()
	logger.set_debug_level(level)
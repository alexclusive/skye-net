import duckdb
import discord
from datetime import datetime
from typing import Optional

import handlers.utils as utils_module
import handlers.logger as logger_module

from handlers.logger import LOG_SETUP, LOG_INFO, LOG_DETAIL, LOG_EXTRA_DETAIL

'''
	daily_tasks
		datetime TIMESTAMP,
		PRIMARY KEY (datetime)
'''

def get_last_daily_task_time() -> Optional[datetime]:
	'''
		Return the most recent datetime in the daily_tasks table
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT datetime FROM daily_tasks ORDER BY datetime DESC LIMIT 1").fetchall()
	utils_module.database_conn.close()
	if result:
		return result[0][0]
	return None

def insert_daily_task_time():
	'''
		Insert the current datetime into the daily_tasks table
	'''
	logger_module.log(LOG_INFO, f"Inserting daily task at {datetime.now()}.")
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("INSERT INTO daily_tasks VALUES (?)", (datetime.now(),))
	utils_module.database_conn.close()
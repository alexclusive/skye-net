import duckdb

from datetime import datetime as dt
from typing import Optional

from .. import logger
from .. import utils

'''
	daily_tasks
		datetime TIMESTAMP,
		PRIMARY KEY (datetime)
'''

def get_last_daily_task_time() -> Optional[dt]:
	'''
		Return the most recent datetime in the daily_tasks table
	'''
	logger.log(logger.LOG_INFO, "Getting last daily task time")
	utils.database_conn = duckdb.connect(utils.database_file)
	result = utils.database_conn.execute("SELECT datetime FROM daily_tasks ORDER BY datetime DESC LIMIT 1").fetchall()
	utils.database_conn.close()
	if result:
		return result[0][0]
	return None

def insert_daily_task_time():
	'''
		Insert the current datetime into the daily_tasks table
	'''
	logger.log(logger.LOG_INFO, f"Inserting daily task at {dt.now()}")
	utils.database_conn = duckdb.connect(utils.database_file)
	utils.database_conn.execute("INSERT INTO daily_tasks VALUES (?)", (dt.now(),))
	utils.database_conn.close()
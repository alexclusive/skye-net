import duckdb

from datetime import datetime

from .. import logger
from .. import utils

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
	logger.log(logger.LOG_INFO, "Getting most recent prompt")
	utils.database_conn = duckdb.connect(utils.database_file)
	result = utils.database_conn.execute("SELECT prompt FROM prompts ORDER BY datetime DESC LIMIT 1").fetchall()
	utils.database_conn.close()
	if result:
		return result[0][0]
	return None

def insert_prompt(prompt, user_id):
	'''
		Insert a new prompt into the database
	'''
	logger.log(logger.LOG_INFO, f"User {user_id} added prompt >{prompt}<")
	utils.database_conn = duckdb.connect(utils.database_file)
	utils.database_conn.execute("INSERT INTO prompts VALUES (?, ?, ?)", (datetime.now(), int(user_id), prompt))
	utils.database_conn.close()
import duckdb

from .. import logger
from .. import utils

'''
	blocked_users
		user_id TEXT,
		PRIMARY KEY (user_id)
'''

def get_all_blocked_users():
	'''
		Return a list of all user_ids that have been blocked
	'''
	logger.log(logger.LOG_INFO, "Getting all blocked users")
	utils.database_conn = duckdb.connect(utils.database_file)
	result = utils.database_conn.execute("SELECT user_id FROM blocked_users").fetchall()
	utils.database_conn.close()
	return [int(row[0]) for row in result]

def block_user(user_id):
	'''
		Insert a user_id into the blocked_users table
	'''
	logger.log(logger.LOG_INFO, f"Adding user {user_id} to blocked list")
	utils.database_conn = duckdb.connect(utils.database_file)
	utils.database_conn.execute("INSERT INTO blocked_users VALUES (?)", (int(user_id),))
	utils.database_conn.close()

def unblock_user(user_id):
	'''
		Remove a user_id from the blocked_users table
	'''
	logger.log(logger.LOG_INFO, f"Removing user {user_id} from blocked list")
	utils.database_conn = duckdb.connect(utils.database_file)
	utils.database_conn.execute("DELETE FROM blocked_users WHERE user_id = ?", (int(user_id),))
	utils.database_conn.close()

def is_user_blocked(user_id) -> bool:
	'''
		Return True if a user is in the blocked_users table
	'''
	logger.log(logger.LOG_INFO, f"Checking if user {user_id} is in blocked list")
	utils.database_conn = duckdb.connect(utils.database_file)
	result = utils.database_conn.execute("SELECT user_id FROM blocked_users WHERE user_id = ?", (int(user_id),)).fetchall()
	utils.database_conn.close()
	return bool(result)
import duckdb

from .. import logger
from .. import utils

'''
	Used to call this banned users but moved to calling it blocked users but left the database table name
	
	banned_users
		user_id TEXT,
		PRIMARY KEY (user_id)
'''

def get_all_blocked_users():
	'''
		Return a list of all user_ids that have been blocked
	'''
	utils.database_conn = duckdb.connect(utils.database_name)
	result = utils.database_conn.execute("SELECT user_id FROM banned_users").fetchall()
	utils.database_conn.close()
	return [int(row[0]) for row in result]

def block_user(user_id):
	'''
		Insert a user_id into the banned_users table
	'''
	logger.log(logger.LOG_INFO, f"Adding user {user_id} to banned list.")
	utils.database_conn = duckdb.connect(utils.database_name)
	utils.database_conn.execute("INSERT INTO banned_users VALUES (?)", (int(user_id),))
	utils.database_conn.close()

def unblock_user(user_id):
	'''
		Remove a user_id from the banned_users table
	'''
	logger.log(logger.LOG_INFO, f"Removing user {user_id} from banned list.")
	utils.database_conn = duckdb.connect(utils.database_name)
	utils.database_conn.execute("DELETE FROM banned_users WHERE user_id = ?", (int(user_id),))
	utils.database_conn.close()
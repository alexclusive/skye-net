import duckdb

from .. import logger
from .. import utils

'''
	react_opt_out
		user_id TEXT,
		PRIMARY KEY (user_id)
'''

def get_all_opt_out_users():
	'''
		Return a list of all user_ids that have opted out of reactions
	'''
	utils.database_conn = duckdb.connect(utils.database_name)
	result = utils.database_conn.execute("SELECT user_id FROM react_opt_out").fetchall()
	utils.database_conn.close()
	return [int(row[0]) for row in result]

def opt_out(user_id):
	'''
		Insert a user_id into the react_opt_out table
	'''
	logger.log(logger.LOG_INFO, f"User {user_id} opted out of reactions.")
	utils.database_conn = duckdb.connect(utils.database_name)
	utils.database_conn.execute("INSERT INTO react_opt_out VALUES (?)", (user_id,))
	utils.database_conn.close()

def opt_in(user_id):
	'''
		Remove a user_id from the react_opt_out table
	'''
	logger.log(logger.LOG_INFO, f"User {user_id} opted in to reactions.")
	utils.database_conn = duckdb.connect(utils.database_name)
	utils.database_conn.execute("DELETE FROM react_opt_out WHERE user_id = ?", (user_id,))
	utils.database_conn.close()
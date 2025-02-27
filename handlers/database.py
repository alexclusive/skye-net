import duckdb
from datetime import datetime

import handlers.utils as utils_module

def init_db():
	'''
		If database does not exist, create it
		If table "prompts" does not exist, create it with columns "prompt TEXT, user_id TEXT, datetime TIMESTAMP"
		If table "react_opt_out" does not exist, create it with columns "user_id TEXT"
		Insert the initial prompt into the database
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("CREATE TABLE IF NOT EXISTS prompts (prompt TEXT NOT NULL, user_id TEXT NOT NULL, datetime TIMESTAMP NOT NULL)")
	utils_module.database_conn.execute("CREATE TABLE IF NOT EXISTS react_opt_out (user_id TEXT)")

	utils_module.database_conn.execute("INSERT INTO prompts VALUES (?, ?, ?)", (utils_module.initial_prompt, utils_module.ownerid, datetime.now()))
	utils_module.database_conn.close()

def get_most_recent_prompt():
	'''
		Return the most recent prompt in the database
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT prompt FROM prompts ORDER BY datetime DESC LIMIT 1").fetchall()
	utils_module.database_conn.close()
	if result:
		return result[0][0]
	return None

def get_all_opt_out_users():
	'''
		Return a list of all user_ids that have opted out of reactions
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT user_id FROM react_opt_out").fetchall()
	utils_module.database_conn.close()
	return [int(row[0]) for row in result]

def insert_prompt(prompt, user_id):
	'''
		Insert a new prompt into the database
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("INSERT INTO prompts VALUES (?, ?, ?)", (prompt, int(user_id), datetime.now()))
	utils_module.database_conn.close()

def opt_out(user_id):
	'''
		Insert a user_id into the react_opt_out table
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("INSERT INTO react_opt_out VALUES (?)", (int(user_id),))
	utils_module.database_conn.close()

def opt_in(user_id):
	'''
		Remove a user_id from the react_opt_out table
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("DELETE FROM react_opt_out WHERE user_id = ?", (int(user_id),))
	utils_module.database_conn.close()
import duckdb

from .. import logger
from .. import utils

'''
	train_facts
		fact_num INTEGER,
		fact TEXT,
		PRIMARY KEY (fact_num)
'''

def get_random_train_fact():
	'''
		Return a random train fact
	'''
	logger.log(logger.LOG_INFO, "Getting random train fact")
	utils.database_conn = duckdb.connect(utils.database_file)
	result = utils.database_conn.execute("SELECT fact FROM train_facts ORDER BY RANDOM() LIMIT 1").fetchall()
	utils.database_conn.close()
	return result[0][0] if result else None

def get_all_train_facts():
	'''
		Return a discord.Embed containing all train facts
	'''
	logger.log(logger.LOG_INFO, "Getting all train facts")
	utils.database_conn = duckdb.connect(utils.database_file)
	result = utils.database_conn.execute("SELECT fact_num, fact FROM train_facts").fetchall()
	utils.database_conn.close()
	return result

def insert_train_fact(fact):
	'''
		Get the next fact_num and insert a new train fact into the database
	'''
	logger.log(logger.LOG_INFO, f"Inserting new train fact: {fact}")
	utils.database_conn = duckdb.connect(utils.database_file)
	result = utils.database_conn.execute("SELECT MAX(fact_num) FROM train_facts").fetchall()
	fact_num = result[0][0] + 1 if result[0][0] else 1
	utils.database_conn.execute("INSERT INTO train_facts VALUES (?, ?)", (fact_num, fact))
	utils.database_conn.close()

def remove_train_fact(fact_num):
	'''
		Remove a train fact from the database
	'''
	logger.log(logger.LOG_INFO, f"Removing train fact with id {fact_num}")
	utils.database_conn = duckdb.connect(utils.database_file)
	result = utils.database_conn.execute("SELECT fact FROM train_facts WHERE fact_num = ?", (fact_num,)).fetchall()
	utils.database_conn.execute("DELETE FROM train_facts WHERE fact_num = ?", (fact_num,))
	utils.database_conn.close()
	logger.log(logger.LOG_DETAIL, f"Removed train fact: {result[0][0]}")
	return result[0][0] if result else None
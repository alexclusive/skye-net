import duckdb

from typing import Optional

from .. import logger
from .. import utils

'''
	number_facts
		number INTEGER,
		fact TEXT,
		PRIMARY KEY (number)
'''

def get_number_fact(number:int) -> Optional[str]:
	'''
		Return the fact for a given number
	'''
	utils.database_conn = duckdb.connect(utils.database_name)
	result = utils.database_conn.execute("SELECT fact FROM number_facts WHERE number = ?", (number,)).fetchall()
	utils.database_conn.close()
	if result:
		return result[0][0]
	return None

def update_number_fact(number:int, fact:str):
	'''
		Update the fact for a given number (override or add)
	'''
	logger.log(logger.LOG_INFO, f"Updating fact for number {number}: >{fact}<.")
	utils.database_conn = duckdb.connect(utils.database_name)
	utils.database_conn.execute("INSERT OR REPLACE INTO number_facts (number, fact) VALUES (?, ?)", (number, fact))
	utils.database_conn.close()

def append_number_fact(number:int, fact:str):
	'''
		Append a fact for a given number (add to existing fact)
	'''
	logger.log(logger.LOG_INFO, f"Appending fact for number {number}: >{fact}<.")
	existing_fact = get_number_fact(number)
	utils.database_conn = duckdb.connect(utils.database_name)
	if existing_fact:
		new_fact = existing_fact + " " + fact
	else:
		new_fact = fact
	utils.database_conn.execute("INSERT OR REPLACE INTO number_facts (number, fact) VALUES (?, ?)", (number, new_fact))
	utils.database_conn.close()
	logger.log(logger.LOG_INFO, f"Fact for number {number} is now: >{new_fact}<.")

def remove_number_fact(number:int):
	'''
		Remove the fact for a given number
	'''
	logger.log(logger.LOG_INFO, f"Removing fact for number {number}.")
	utils.database_conn = duckdb.connect(utils.database_name)
	utils.database_conn.execute("DELETE FROM number_facts WHERE number = ?", (number,))
	utils.database_conn.close()
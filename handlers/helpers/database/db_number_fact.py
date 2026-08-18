import duckdb
from typing import Optional

import handlers.utils as utils_module
import handlers.logger as logger_module

from handlers.logger import LOG_SETUP, LOG_INFO, LOG_DETAIL, LOG_EXTRA_DETAIL

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
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT fact FROM number_facts WHERE number = ?", (number,)).fetchall()
	utils_module.database_conn.close()
	if result:
		return result[0][0]
	return None

def update_number_fact(number:int, fact:str):
	'''
		Update the fact for a given number (override or add)
	'''
	logger_module.log(LOG_INFO, f"Updating fact for number {number}: >{fact}<.")
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("INSERT OR REPLACE INTO number_facts (number, fact) VALUES (?, ?)", (number, fact))
	utils_module.database_conn.close()

def append_number_fact(number:int, fact:str):
	'''
		Append a fact for a given number (add to existing fact)
	'''
	logger_module.log(LOG_INFO, f"Appending fact for number {number}: >{fact}<.")
	existing_fact = get_number_fact(number)
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	if existing_fact:
		new_fact = existing_fact + " " + fact
	else:
		new_fact = fact
	utils_module.database_conn.execute("INSERT OR REPLACE INTO number_facts (number, fact) VALUES (?, ?)", (number, new_fact))
	utils_module.database_conn.close()
	logger_module.log(LOG_INFO, f"Fact for number {number} is now: >{new_fact}<.")

def remove_number_fact(number:int):
	'''
		Remove the fact for a given number
	'''
	logger_module.log(LOG_INFO, f"Removing fact for number {number}.")
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("DELETE FROM number_facts WHERE number = ?", (number,))
	utils_module.database_conn.close()
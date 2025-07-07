import duckdb
import discord
from datetime import datetime
from typing import Optional

import handlers.utils as utils_module
import handlers.logger as logger_module

from handlers.logger import LOG_SETUP, LOG_INFO, LOG_DETAIL, LOG_EXTRA_DETAIL

'''
	todo
		item_num INTEGER,
		todo TEXT,
		PRIMARY KEY (item_num)
'''

def get_all_todo_items():
	'''
		Return a list of all todo items
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT item_num, todo FROM todo").fetchall()
	utils_module.database_conn.close()
	return result if result else None

def insert_todo_item(todo):
	'''
		Insert a new todo item into the database
	'''
	logger_module.log(LOG_INFO, f"Inserting todo task >{todo}<.")
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT MAX(item_num) FROM todo").fetchall()
	item_num = result[0][0] + 1 if result[0][0] else 1
	utils_module.database_conn.execute("INSERT INTO todo VALUES (?, ?)", (item_num, todo))
	utils_module.database_conn.close()

def remove_todo_item(item_num):
	'''
		Remove a todo item from the database
	'''
	logger_module.log(LOG_INFO, f"Removing todo task number >{item_num}<.")
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT todo FROM todo WHERE item_num = ?", (item_num,)).fetchall()
	utils_module.database_conn.execute("DELETE FROM todo WHERE item_num = ?", (item_num,))
	utils_module.database_conn.close()
	logger_module.log(LOG_DETAIL, f"Removed todo task >{result[0][0]}<.")
	return result[0][0] if result else None
import duckdb

from typing import Optional

from .. import logger
from .. import utils

'''
	todo
		item_num INTEGER,
		todo TEXT,
		PRIMARY KEY (item_num)
'''

def get_all_todo_items() -> list:
	'''
		Return a list of all todo items
	'''
	utils.database_conn = duckdb.connect(utils.database_name)
	result = utils.database_conn.execute("SELECT item_num, todo FROM todo").fetchall()
	utils.database_conn.close()
	return result

def insert_todo_item(todo:str):
	'''
		Insert a new todo item into the database
	'''
	logger.log(logger.LOG_INFO, f"Inserting todo task >{todo}<.")
	utils.database_conn = duckdb.connect(utils.database_name)
	result = utils.database_conn.execute("SELECT MAX(item_num) FROM todo").fetchall()
	item_num = result[0][0] + 1 if result[0][0] else 1
	utils.database_conn.execute("INSERT INTO todo VALUES (?, ?)", (item_num, todo))
	utils.database_conn.close()

def remove_todo_item(item_num:int) -> Optional[str]:
	'''
		Remove a todo item from the database
	'''
	logger.log(logger.LOG_INFO, f"Removing todo task number >{item_num}<.")
	utils.database_conn = duckdb.connect(utils.database_name)
	result = utils.database_conn.execute("SELECT todo FROM todo WHERE item_num = ?", (item_num,)).fetchall()
	utils.database_conn.execute("DELETE FROM todo WHERE item_num = ?", (item_num,))
	utils.database_conn.close()
	logger.log(logger.LOG_DETAIL, f"Removed todo task >{result[0][0]}<.")
	return result[0][0] if result else None
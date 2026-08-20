import duckdb

from .. import logger
from .. import utils

'''
	reactions
		trigger TEXT,
		emoji_id_1 TEXT,
		emoji_id_2 TEXT,
		emoji_id_3 TEXT,
		PRIMARY KEY (trigger)
'''

def get_all_reactions():
	'''
		Return a list of tuples of (reaction_text, emoji_ids)
	'''
	utils.database_conn = duckdb.connect(utils.database_name)
	result = utils.database_conn.execute("SELECT reaction, emoji_id_1, emoji_id_2, emoji_id_3 FROM reactions").fetchall()
	utils.database_conn.close()
	return [(row[0], [row[1], row[2], row[3]]) for row in result]

def insert_reaction(trigger, emoji_id_1, emoji_id_2="", emoji_id_3=""):
	'''
		Insert a new reaction into the database
	'''
	logger.log(logger.LOG_INFO, f"Inserting reaction for trigger >{trigger}< with emoji id/s {emoji_id_1}/{emoji_id_2}/{emoji_id_3}.")
	utils.database_conn = duckdb.connect(utils.database_name)
	utils.database_conn.execute("INSERT INTO reactions VALUES (?, ?, ?, ?)", (trigger, emoji_id_1, emoji_id_2, emoji_id_3))
	utils.database_conn.close()

def remove_reaction(trigger):
	'''
		Remove a reaction from the database
		Returns the emoji_ids of the removed reaction
	'''
	logger.log(logger.LOG_INFO, f"Removing reaction for trigger >{trigger}<.")
	utils.database_conn = duckdb.connect(utils.database_name)
	result = utils.database_conn.execute("SELECT emoji_id_1, emoji_id_2, emoji_id_3 FROM reactions WHERE trigger = ?", (trigger,)).fetchall()
	utils.database_conn.execute("DELETE FROM reactions WHERE trigger = ?", (trigger,))
	utils.database_conn.close()
	logger.log(logger.LOG_DETAIL, f"Removed reaction emojis {result[0][0]}/{result[0][1]}/{result[0][2]}.")
	return result if result else None

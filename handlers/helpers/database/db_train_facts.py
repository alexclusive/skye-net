import duckdb
import discord
from datetime import datetime
from typing import Optional

import handlers.utils as utils_module
import handlers.logger as logger_module

from handlers.logger import LOG_SETUP, LOG_INFO, LOG_DETAIL, LOG_EXTRA_DETAIL

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
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT fact FROM train_facts ORDER BY RANDOM() LIMIT 1").fetchall()
	utils_module.database_conn.close()
	return result[0][0] if result else None

def get_all_train_facts():
	'''
		Return a list of all train facts
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT fact_num, fact FROM train_facts").fetchall()
	utils_module.database_conn.close()
	embed = discord.Embed(title="Train Facts", colour=0xffffff)
	for row in result:
		embed.add_field(name=f"Fact {row[0]}", value=row[1], inline=False)
	embed.set_author(name="SkyeNet", icon_url=utils_module.discord_bot.user.display_avatar.url)
	return result

def insert_train_fact(fact):
	'''
		Get the next fact_num and insert a new train fact into the database
	'''
	logger_module.log(LOG_INFO, f"Inserting new train fact >{fact}<.")
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT MAX(fact_num) FROM train_facts").fetchall()
	fact_num = result[0][0] + 1 if result[0][0] else 1
	utils_module.database_conn.execute("INSERT INTO train_facts VALUES (?, ?)", (fact_num, fact))
	utils_module.database_conn.close()

def remove_train_fact(fact_num):
	'''
		Remove a train fact from the database
	'''
	logger_module.log(LOG_INFO, f"Removing train fact with id {fact_num}.")
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT fact FROM train_facts WHERE fact_num = ?", (fact_num,)).fetchall()
	utils_module.database_conn.execute("DELETE FROM train_facts WHERE fact_num = ?", (fact_num,))
	utils_module.database_conn.close()
	logger_module.log(LOG_DETAIL, f"Removed train fact >{result[0][0]}<.")
	return result[0][0] if result else None
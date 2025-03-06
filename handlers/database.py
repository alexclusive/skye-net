import duckdb
import discord
from datetime import datetime
from typing import Optional

import handlers.utils as utils_module

def init_db():
	'''
		If database does not exist, create it
		If table "prompts" does not exist, create it with columns "prompt TEXT, user_id TEXT, datetime TIMESTAMP"
		If table "react_opt_out" does not exist, create it with column "user_id TEXT"
		If table "daily_tasks" does not exist, create it with column "datetime TIMESTAMP"
		If table "train_facts" does not exist, create it with column "fact_num INTEGER, fact TEXT"
		Insert the initial prompt into the database
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("CREATE TABLE IF NOT EXISTS prompts (prompt TEXT NOT NULL, user_id TEXT NOT NULL, datetime TIMESTAMP NOT NULL)")
	utils_module.database_conn.execute("CREATE TABLE IF NOT EXISTS react_opt_out (user_id TEXT)")
	utils_module.database_conn.execute("CREATE TABLE IF NOT EXISTS daily_tasks (datetime TIMESTAMP NOT NULL)")
	utils_module.database_conn.execute("CREATE TABLE IF NOT EXISTS train_facts (fact_num INTEGER NOT NULL, fact TEXT NOT NULL)")

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

def get_last_daily_task_time() -> Optional[datetime]:
	'''
		Return the most recent datetime in the daily_tasks table
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT datetime FROM daily_tasks ORDER BY datetime DESC LIMIT 1").fetchall()
	utils_module.database_conn.close()
	if result:
		return result[0][0]
	return None

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

def insert_daily_task_time():
	'''
		Insert the current datetime into the daily_tasks table
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("INSERT INTO daily_tasks VALUES (?)", (datetime.now(),))
	utils_module.database_conn.close()

def insert_train_fact(fact):
	'''
		Get the next fact_num and insert a new train fact into the database
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT MAX(fact_num) FROM train_facts").fetchall()
	fact_num = result[0][0] + 1 if result[0][0] else 1
	utils_module.database_conn.execute("INSERT INTO train_facts VALUES (?, ?)", (fact_num, fact))
	utils_module.database_conn.close()

def remove_train_fact(fact_num):
	'''
		Remove a train fact from the database
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT fact FROM train_facts WHERE fact_num = ?", (fact_num,)).fetchall()
	utils_module.database_conn.execute("DELETE FROM train_facts WHERE fact_num = ?", (fact_num,))
	utils_module.database_conn.close()
	return result[0][0] if result else None
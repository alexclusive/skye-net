import duckdb
import discord
from datetime import datetime
from typing import Optional, List, Tuple

import handlers.utils as utils_module

def init_db():
	'''
		If database does not exist, create it
		If table "prompts" does not exist, create it with columns "prompt TEXT, user_id TEXT, datetime TIMESTAMP"
		If table "react_opt_out" does not exist, create it with column "user_id TEXT"
		If table "daily_tasks" does not exist, create it with column "datetime TIMESTAMP"
		If table "train_facts" does not exist, create it with columns "fact_num INTEGER, fact TEXT"
		If table "reactions" does not exist, create it with columns "trigger TEXT, emoji_id_1 TEXT, emoji_id_2 TEXT, emoji_id_3 TEXT"
		If table "logging_channels" does not exist, create it with columns "guild_id TEXT, message_channel_id TEXT, member_channel_id TEXT, guild_channel_id TEXT"
		If table "banned_users" does not exist, create it with column "user_id TEXT"
		If table "important_roles" does not exist, create it with columns "guild_id TEXT, welcomed_role_id TEXT, trusted_role_id TEXT, trusted_time_days INTEGER"
		If table "todo" does not exist, create it with columns "item_num INTEGER, todo TEXT"
		Insert the initial prompt into the database
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("CREATE TABLE IF NOT EXISTS prompts (prompt TEXT NOT NULL, user_id TEXT NOT NULL, datetime TIMESTAMP NOT NULL)")
	utils_module.database_conn.execute("CREATE TABLE IF NOT EXISTS react_opt_out (user_id TEXT)")
	utils_module.database_conn.execute("CREATE TABLE IF NOT EXISTS daily_tasks (datetime TIMESTAMP NOT NULL)")
	utils_module.database_conn.execute("CREATE TABLE IF NOT EXISTS train_facts (fact_num INTEGER NOT NULL, fact TEXT NOT NULL)")
	utils_module.database_conn.execute("CREATE TABLE IF NOT EXISTS reactions (trigger TEXT NOT NULL, emoji_id_1 TEXT NOT NULL, emoji_id_2 TEXT, emoji_id_3 TEXT)")
	utils_module.database_conn.execute("CREATE TABLE IF NOT EXISTS logging_channels (guild_id TEXT NOT NULL, message_channel_id TEXT NOT NULL, member_channel_id TEXT NOT NULL, guild_channel_id TEXT NOT NULL)")
	utils_module.database_conn.execute("CREATE TABLE IF NOT EXISTS banned_users (user_id TEXT NOT NULL)")
	utils_module.database_conn.execute("CREATE TABLE IF NOT EXISTS important_roles (guild_id TEXT NOT NULL, welcomed_role_id TEXT NOT NULL, trusted_role_id TEXT NOT NULL, trusted_time_days INTEGER NOT NULL)")
	utils_module.database_conn.execute("CREATE TABLE IF NOT EXISTS todo (item_num INTEGER NOT NULL, todo TEXT NOT NULL)")
	utils_module.database_conn.execute("INSERT INTO prompts VALUES (?, ?, ?)", (utils_module.initial_prompt, utils_module.ownerid, datetime.now()))
	utils_module.database_conn.close()

# Prompts
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

def insert_prompt(prompt, user_id):
	'''
		Insert a new prompt into the database
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("INSERT INTO prompts VALUES (?, ?, ?)", (prompt, int(user_id), datetime.now()))
	utils_module.database_conn.close()

# Opt Out
def get_all_opt_out_users():
	'''
		Return a list of all user_ids that have opted out of reactions
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT user_id FROM react_opt_out").fetchall()
	utils_module.database_conn.close()
	return [int(row[0]) for row in result]

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

# Daily Tasks
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

def insert_daily_task_time():
	'''
		Insert the current datetime into the daily_tasks table
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("INSERT INTO daily_tasks VALUES (?)", (datetime.now(),))
	utils_module.database_conn.close()

# Train Facts
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

# Reactions
def get_all_reactions():
	'''
		Return a list of tuples of (reaction_text, emoji_ids)
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT reaction, emoji_id_1, emoji_id_2, emoji_id_3 FROM reactions").fetchall()
	utils_module.database_conn.close()
	return [(row[0], [row[1], row[2], row[3]]) for row in result]

def insert_reaction(trigger, emoji_id_1, emoji_id_2="", emoji_id_3=""):
	'''
		Insert a new reaction into the database
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("INSERT INTO reactions VALUES (?, ?, ?, ?)", (trigger, emoji_id_1, emoji_id_2, emoji_id_3))
	utils_module.database_conn.close()

def remove_reaction(trigger):
	'''
		Remove a reaction from the database
		Returns the emoji_ids of the removed reaction
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT emoji_id_1, emoji_id_2, emoji_id_3 FROM reactions WHERE trigger = ?", (trigger,)).fetchall()
	utils_module.database_conn.execute("DELETE FROM reactions WHERE trigger = ?", (trigger,))
	utils_module.database_conn.close()
	return result if result else None

# Logging Channels
def get_logging_channels(guild_id):
	'''
		Return the logging channels for a guild
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT message_channel_id, member_channel_id, guild_channel_id FROM logging_channels WHERE guild_id = ?", (guild_id,)).fetchall()
	utils_module.database_conn.close()
	return result if result else None

def insert_logging_channels(guild_id, message_channel:discord.TextChannel=None, member_channel:discord.TextChannel=None, guild_channel:discord.TextChannel=None):
	'''
		Insert the logging channels for a guild
		If guild already exists, update the channels
		Only update the channels that are not None
	'''
	message_channel_id = message_channel.id if message_channel else None
	member_channel_id = member_channel.id if member_channel else None
	guild_channel_id = guild_channel.id if guild_channel else None
	
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT * FROM logging_channels WHERE guild_id = ?", (guild_id,)).fetchall()
	if result:
		if message_channel_id:
			utils_module.database_conn.execute("UPDATE logging_channels SET message_channel_id = ? WHERE guild_id = ?", (message_channel_id, guild_id))
		if member_channel_id:
			utils_module.database_conn.execute("UPDATE logging_channels SET member_channel_id = ? WHERE guild_id = ?", (member_channel_id, guild_id))
		if guild_channel_id:
			utils_module.database_conn.execute("UPDATE logging_channels SET guild_channel_id = ? WHERE guild_id = ?", (guild_channel_id, guild_id))
	else:
		utils_module.database_conn.execute("INSERT INTO logging_channels VALUES (?, ?, ?, ?)", (guild_id, message_channel_id, member_channel_id, guild_channel_id))

# Banned Users
def get_all_banned_users():
	'''
		Return a list of all user_ids that have been banned
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT user_id FROM banned_users").fetchall()
	utils_module.database_conn.close()
	return [int(row[0]) for row in result]

def ban_user(user_id):
	'''
		Insert a user_id into the banned_users table
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("INSERT INTO banned_users VALUES (?)", (int(user_id),))
	utils_module.database_conn.close()

def unban_user(user_id):
	'''
		Remove a user_id from the banned_users table
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	utils_module.database_conn.execute("DELETE FROM banned_users WHERE user_id = ?", (int(user_id),))
	utils_module.database_conn.close()

# Important Roles
def get_important_roles(guild_id):
	'''
		Return the important roles for a guild
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT welcomed_role_id, trusted_role_id, trusted_time_days FROM important_roles WHERE guild_id = ?", (guild_id,)).fetchall()
	utils_module.database_conn.close()
	return result[0] if result else None

def insert_important_roles(guild_id, welcomed_role_id, trusted_role_id, trusted_time_days):
	'''
		Insert the important roles for a guild'
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT * FROM important_roles WHERE guild_id = ?", (guild_id,)).fetchall()
	if result:
		utils_module.database_conn.execute("UPDATE important_roles SET welcomed_role_id = ?, trusted_role_id = ?, trusted_time_days = ? WHERE guild_id = ?", (welcomed_role_id, trusted_role_id, trusted_time_days, guild_id))
	else:
		utils_module.database_conn.execute("INSERT INTO important_roles VALUES (?, ?, ?, ?)", (guild_id, welcomed_role_id, trusted_role_id, trusted_time_days))
	utils_module.database_conn.close()

# To do list

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
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT MAX(item_num) FROM todo").fetchall()
	item_num = result[0][0] + 1 if result[0][0] else 1
	utils_module.database_conn.execute("INSERT INTO todo VALUES (?, ?)", (item_num, todo))
	utils_module.database_conn.close()

def remove_todo_item(item_num):
	'''
		Remove a todo item from the database
	'''
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT todo FROM todo WHERE item_num = ?", (item_num,)).fetchall()
	utils_module.database_conn.execute("DELETE FROM todo WHERE item_num = ?", (item_num,))
	utils_module.database_conn.close()
	return result[0][0] if result else None
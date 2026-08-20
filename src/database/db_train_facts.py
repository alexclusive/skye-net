import discord
import duckdb

from .. import logger
from .. import utils

# TODO: this shouldn't have to import discord, that should be done where these functions are called from

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
	utils.database_conn = duckdb.connect(utils.database_name)
	result = utils.database_conn.execute("SELECT fact FROM train_facts ORDER BY RANDOM() LIMIT 1").fetchall()
	utils.database_conn.close()
	return result[0][0] if result else None

def get_all_train_facts():
	'''
		Return a discord.Embed containing all train facts
	'''
	utils.database_conn = duckdb.connect(utils.database_name)
	result = utils.database_conn.execute("SELECT fact_num, fact FROM train_facts").fetchall()
	utils.database_conn.close()
	embed = discord.Embed(title="Train Facts", colour=0xffffff)
	for row in result:
		embed.add_field(name=f"Fact {row[0]}", value=row[1], inline=False)
	# If the bot user exists, set its avatar as the author icon
	try:
		embed.set_author(name="SkyeNet", icon_url=utils.discord_bot.user.display_avatar.url)
	except Exception:
		# Ignore if discord bot/user isn't available in this context
		pass
	if len(result) == 0:
		embed.description = "No train facts available."
	return embed

def insert_train_fact(fact):
	'''
		Get the next fact_num and insert a new train fact into the database
	'''
	logger.log(logger.LOG_INFO, f"Inserting new train fact >{fact}<.")
	utils.database_conn = duckdb.connect(utils.database_name)
	result = utils.database_conn.execute("SELECT MAX(fact_num) FROM train_facts").fetchall()
	fact_num = result[0][0] + 1 if result[0][0] else 1
	utils.database_conn.execute("INSERT INTO train_facts VALUES (?, ?)", (fact_num, fact))
	utils.database_conn.close()

def remove_train_fact(fact_num):
	'''
		Remove a train fact from the database
	'''
	logger.log(logger.LOG_INFO, f"Removing train fact with id {fact_num}.")
	utils.database_conn = duckdb.connect(utils.database_name)
	result = utils.database_conn.execute("SELECT fact FROM train_facts WHERE fact_num = ?", (fact_num,)).fetchall()
	utils.database_conn.execute("DELETE FROM train_facts WHERE fact_num = ?", (fact_num,))
	utils.database_conn.close()
	logger.log(logger.LOG_DETAIL, f"Removed train fact >{result[0][0]}<.")
	return result[0][0] if result else None
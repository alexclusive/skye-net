import duckdb
import discord
from datetime import datetime
from typing import Optional

import handlers.utils as utils_module
import handlers.logger as logger_module

from handlers.logger import LOG_SETUP, LOG_INFO, LOG_DETAIL, LOG_EXTRA_DETAIL

'''
	important_roles
		guild_id TEXT,
		welcomed_role_id TEXT,
		trusted_role_id TEXT,
		trusted_time_days INTEGER,
		PRIMARY KEY (guild_id)
'''

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
	logger_module.log(LOG_INFO, f"Updating important roles for guild {guild_id}. Welcomed >{welcomed_role_id}<. Trusted >{trusted_role_id}<. Trusted time >{trusted_time_days}<.")
	utils_module.database_conn = duckdb.connect(utils_module.database_name)
	result = utils_module.database_conn.execute("SELECT * FROM important_roles WHERE guild_id = ?", (guild_id,)).fetchall()
	if result:
		utils_module.database_conn.execute("UPDATE important_roles SET welcomed_role_id = ?, trusted_role_id = ?, trusted_time_days = ? WHERE guild_id = ?", (welcomed_role_id, trusted_role_id, trusted_time_days, guild_id))
	else:
		utils_module.database_conn.execute("INSERT INTO important_roles VALUES (?, ?, ?, ?)", (guild_id, welcomed_role_id, trusted_role_id, trusted_time_days))
	utils_module.database_conn.close()
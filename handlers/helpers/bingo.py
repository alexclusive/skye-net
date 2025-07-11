import discord
from typing import Optional

import handlers.utils as utils_module
import handlers.logger as logger_module
import handlers.database as database_module

from handlers.logger import LOG_SETUP, LOG_INFO, LOG_DETAIL, LOG_EXTRA_DETAIL

free_space_item = "FREE SPACE"

def split_bingo_card_items(items:list) -> list:
	'''
		Split the items from a 1d array into a 2d array of 5 items per row.
	'''
	return [items[i:i + 5] for i in range(0, len(items), 5)]

def get_bingo_grid(card_items:list) -> str:
	'''
		Get the bingo grid as a string using :white_large_square: for unchecked, and :green_square: for checked.
	'''
	grid = ""
	for row in card_items:
		row_string = ""
		for item in row:
			if is_item_checked(item):
				row_string += ":green_square: "
			else:
				row_string += ":white_large_square: "

		grid += row_string + "\n"
	return grid

def is_item_checked(item:str) -> bool:
	'''
		Check if an item is checked (has a strike through).
	'''
	return item.startswith("~~") and item.endswith("~~") or item == free_space_item

def check_bingo_item(item:str) -> str:
	if item == free_space_item or is_item_checked(item):
		return item
	else:
		return f"~~{item}~~"
	
def uncheck_bingo_item(item:str) -> str:
	if item == free_space_item or not is_item_checked(item):
		return item
	else:
		return item[2:-2]

def is_winning_bingo(card_items:list) -> bool:
	'''
		Get the 2d array of items from the bingo card and see if the user has won.
		An item is checked if it has a strike through (~~item~~), or if it is "FREE SPACE".
	'''
	for row in card_items:
		if all(is_item_checked(item) for item in row):
			return True
	
	for col in range(5):
		if all(is_item_checked(card_items[row][col]) for row in range(5)):
			return True
		
	# Diagonal
	if all(is_item_checked(card_items[i][i]) for i in range(5)) or all(is_item_checked(card_items[i][4 - i]) for i in range(5)):
		return True
		
	return False

def get_all_bingo_templates() -> Optional[discord.Embed]:
	templates = database_module.get_all_bingo_templates()
	if not templates:
		logger_module.log(LOG_INFO, "No bingo templates found.")
		return None

	embed = discord.Embed(title="Bingo Templates", colour=0xffffff)
	for guild_id, guild_templates in templates.items():
		template_text = ""
		for template in guild_templates:
			template_text += f"{template[0]} (Free Space: {template[1]})\n"
		embed.add_field(name=f"Guild {guild_id}", value=template_text, inline=False)
	return embed

def get_bingo_templates_for_guild(guild_id: str) -> Optional[discord.Embed]:
	templates = database_module.get_all_bingo_templates_for_guild(guild_id)
	if not templates:
		logger_module.log(LOG_INFO, f"No bingo templates found for guild {guild_id}.")
		return None

	embed = discord.Embed(title=f"Bingo Templates for Guild {guild_id}", colour=0xffffff)
	for template in templates:
		embed.add_field(name=template[0], value=f"Free Space: {template[1]}", inline=False)
	return embed

def create_bingo_template(guild_id:str, bingo_name:str, free_space:bool, items_str:str) -> bool:
	if (free_space and len(items_str.split("\n")) < 24) or (not free_space and len(items_str.split("\n")) < 25):
		return False
	
	database_module.create_bingo_template(guild_id, bingo_name, free_space, items_str)
	logger_module.log(LOG_INFO, f"Created bingo template '{bingo_name}' for guild {guild_id}.")
	return True

def delete_bingo_template(guild_id:str, bingo_name:str) -> bool:
	if not database_module.does_bingo_template_exist(guild_id, bingo_name):
		return False

	database_module.delete_bingo_template(guild_id, bingo_name)
	logger_module.log(LOG_INFO, f"Deleted bingo template '{bingo_name}' for guild {guild_id}.")
	return True

def create_bingo_card(guild_id:str, bingo_name:str, user_id:str) -> bool:
	if not database_module.does_bingo_template_exist(guild_id, bingo_name):
		return False

	database_module.create_bingo_card(guild_id, bingo_name, user_id)
	logger_module.log(LOG_INFO, f"Created bingo card for user {user_id} in template '{bingo_name}' for guild {guild_id}.")
	return True

def get_bingo_card(guild_id:str, bingo_name:str, user_id:str) -> Optional[discord.Embed]:
	if not database_module.does_bingo_template_exist(guild_id, bingo_name):
		return None
	
	if not database_module.has_user_created_bingo_card(guild_id, bingo_name, user_id):
		logger_module.log(LOG_DETAIL, f"User {user_id} has not created a bingo card for bingo '{bingo_name}' in guild {guild_id}. Creating a new card.")
		database_module.create_bingo_card(guild_id, bingo_name, user_id)

	card_items = database_module.get_bingo_card(guild_id, bingo_name, user_id)
	if len(card_items) == 0:
		logger_module.log(LOG_DETAIL, f"No bingo card found for user {user_id} in bingo '{bingo_name}' for guild {guild_id}. Even after forcing a creation.")
		return None
	
	embed_title = f"{bingo_name} Bingo Card"
	user = utils_module.discord_bot.get_user(user_id)
	if user:
		embed_title = f"{user.name}'s {bingo_name} Bingo Card"
	embed = discord.Embed(title=embed_title, colour=0xffffff)

	split_card_items = split_bingo_card_items(card_items)
	for row in range(len(split_card_items)):
		first = f":one: {split_card_items[row][0]}"
		second = f":two: {split_card_items[row][1]}"
		third = f":three: {split_card_items[row][2]}"
		fourth = f":four: {split_card_items[row][3]}"
		fifth = f":five: {split_card_items[row][4]}"
		embed.add_field(name=f"Row {row + 1}", value="\n".join([first, second, third, fourth, fifth]), inline=False)

	if is_winning_bingo(split_card_items):
		embed.colour = 0x00ff00

	embed.description = get_bingo_grid(split_card_items)
	embed.set_footer(text=f"User ID: {user_id} | Guild ID: {guild_id}")
	return embed

def get_bingo_card_minimal(guild_id:str, bingo_name:str, user_id:str) -> Optional[discord.Embed]:
	embed = get_bingo_card(guild_id, bingo_name, user_id)
	
	if embed is not None:
		embed.clear_fields()
	
	return embed

def bingo_check(guild_id:str, bingo_name:str, user_id:str, item_row:int, item_column:int) -> Optional[discord.Embed]:
	if not database_module.does_bingo_template_exist(guild_id, bingo_name):
		logger_module.log(LOG_INFO, f"Bingo template '{bingo_name}' does not exist for guild {guild_id}.")
		return None
	
	if not database_module.has_user_created_bingo_card(guild_id, bingo_name, user_id):
		logger_module.log(LOG_DETAIL, f"User {user_id} has not created a bingo card for bingo '{bingo_name}' in guild {guild_id}.")
		return None
	
	card = database_module.get_bingo_card(guild_id, bingo_name, user_id)
	if len(card) == 0:
		logger_module.log(LOG_DETAIL, f"No bingo card found for user {user_id} in bingo '{bingo_name}' for guild {guild_id}.")
		return None
	
	if item_row < 1 or item_row > 5 or item_column < 1 or item_column > 5:
		logger_module.log(LOG_DETAIL, f"Invalid item row {item_row} or column {item_column} for bingo '{bingo_name}' in guild {guild_id}.")
		embed = discord.Embed(title="Invalid Bingo Index", colour=0xff0000)
		embed.add_field(name=f"Invalid item row {item_row} or column {item_column}.", value="Please provide values between 1 and 5.")
		return embed
	
	items_array = split_bingo_card_items(card)
	if is_item_checked(items_array[item_row - 1][item_column - 1]):
		items_array[item_row - 1][item_column - 1] = uncheck_bingo_item(items_array[item_row - 1][item_column - 1])
	else:
		items_array[item_row - 1][item_column - 1] = check_bingo_item(items_array[item_row - 1][item_column - 1])

	card_items = [item for sublist in items_array for item in sublist]  # Flatten the 2D array to 1D
	database_module.update_bingo_card(guild_id, bingo_name, user_id, card_items)

	embed = get_bingo_card(guild_id, bingo_name, user_id)

	if is_winning_bingo(items_array):
		embed_title = "Bingo!"
		user = utils_module.discord_bot.get_user(user_id)
		if user:
			embed_title = f"BINGO! Congratulations {user.name}!"
		embed.title = embed_title

	return embed

def bingo_help() -> discord.Embed:
	'''
		Admin
			create_bingo_template
			delete_bingo_template
			get_bingo_templates
		Everyone
			create_bingo_card
			get_bingo_card
			get_bingo_card_minimal
			bingo_check
			bingo_help
	'''
	embed = discord.Embed(title="Bingo Help", colour=0xffffff)
	embed.add_field(name="/create_bingo_template `admin only`", value="Create a new bingo template for the server. Specify a name, whether it has a free center space, and the items for the bingo card. Items can be provided in the command with each item separated by a comma, or through a message where each item is separated by a new line.")
	embed.add_field(name="/delete_bingo_template `admin only`", value="Delete a bingo template from the server. Specify the name of the bingo template to delete.")
	embed.add_field(name="/get_bingo_templates `admin only`", value="Get a list of all bingo templates for the server.")

	embed.add_field(name="/create_bingo_card", value="Create a new bingo card for the user. Specify the name of the bingo template to use.")
	embed.add_field(name="/get_bingo_card", value="Get the current bingo card for the user. Creates a new card if the user has not created one yet.")
	embed.add_field(name="/get_bingo_card_minimal", value="Get a minimal version of the current bingo card for the user.")
	embed.add_field(name="/bingo_check", value="Mark off an item in the user's bingo card. Specify the name of the bingo template, the row (1-5), and the column (1-5) of the item to check or uncheck.")
	embed.add_field(name="/bingo_help", value="Get help information for using the bingo commands.")

	return embed
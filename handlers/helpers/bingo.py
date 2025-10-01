import discord
from typing import Optional

import handlers.utils as utils_module
import handlers.logger as logger_module
import handlers.database as database_module

from handlers.logger import LOG_INFO, LOG_DETAIL

colour_green = 0x00ff00
colour_white = 0xffffff

free_space_item = "FREE SPACE"
not_your_bingo = "This isn't your bingo board!"

# Helpers

def split_bingo_card_items(items:list) -> list:
	return [items[i:i + 5] for i in range(0, len(items), 5)]

def is_item_checked(item:str) -> bool:
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

def get_bingo_grid(card_items:list) -> str:
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

def is_winning_bingo(card_items:list) -> bool:
	# Rows
	for row in card_items:
		if all(is_item_checked(item) for item in row):
			return True
	# Columns
	for col in range(5):
		if all(is_item_checked(card_items[row][col]) for row in range(5)):
			return True
	# Diagonals
	if all(is_item_checked(card_items[i][i]) for i in range(5)) or all(is_item_checked(card_items[i][4 - i]) for i in range(5)):
		return True
	return False

# Get Bingo Card Command

def get_bingo_card(guild_id:int, bingo_name:str, user_id:int) -> tuple:
	embed = create_bingo_embed(guild_id, user_id, bingo_name)

	if not does_bingo_card_exist(guild_id, bingo_name, user_id):
		return embed, None
	
	items = split_bingo_card_items(database_module.get_bingo_card(guild_id, bingo_name, user_id))

	embed = update_bingo_embed_items(embed, items)
	view = BingoView(guild_id, bingo_name, user_id, items)
	return embed, view

# Get Bingo Card Core functions

def does_bingo_card_exist(guild_id:int, bingo_name:str, user_id:int) -> bool:
	'''
		Check if a template exists and if the user has created a card for it.
		Creates a card if it can.
	'''
	if not database_module.does_bingo_template_exist(guild_id, bingo_name):
		logger_module.log(LOG_INFO, f"Bingo template '{bingo_name}' does not exist for guild {guild_id}.")
		return False
	
	if not database_module.has_user_created_bingo_card(guild_id, bingo_name, user_id):
		database_module.create_bingo_card(guild_id, bingo_name, user_id)
		logger_module.log(LOG_DETAIL, f"Auto-created bingo card for user {user_id} in '{bingo_name}'.")
		if not database_module.has_user_created_bingo_card(guild_id, bingo_name, user_id):
			logger_module.log(LOG_INFO, f"Failed to create bingo card for user {user_id} in '{bingo_name}'.")
			return False
		
	return True

def create_bingo_embed(guild_id:int, user_id:int, bingo_name:str) -> discord.Embed:
	user = utils_module.discord_bot.get_user(user_id)
	if user:
		embed_title = f"{user.name}'s {bingo_name} Bingo Card"
	else:
		embed_title = f"Unknown user's {bingo_name} Bingo Card"

	embed = discord.Embed(title=embed_title, colour=colour_white)
	embed.set_footer(text=f"User ID: {user_id} | Guild ID: {guild_id}")
	return embed

def update_bingo_embed_items(embed:discord.Embed, items:list) -> discord.Embed:
	embed.description = get_bingo_grid(items)

	if is_winning_bingo(items):
		embed.colour = colour_green  # Green for winning bingo
	else:
		embed.colour = colour_white  # Default color

	return embed

def get_complete_bingo_embed(guild_id:int, user_id:int, bingo_name:str, items:list) -> discord.Embed:
	embed = create_bingo_embed(guild_id, user_id, bingo_name)
	embed = update_bingo_embed_items(embed, items)
	return embed

def toggle_bingo_item(guild_id: int, bingo_name: str, user_id: int, row: int, col: int) -> list:
	card = database_module.get_bingo_card(guild_id, bingo_name, user_id)
	items_2d = split_bingo_card_items(card)

	if is_item_checked(items_2d[row][col]):
		items_2d[row][col] = uncheck_bingo_item(items_2d[row][col])
	else:
		items_2d[row][col] = check_bingo_item(items_2d[row][col])

	flattened = [item for sublist in items_2d for item in sublist]
	database_module.update_bingo_card(guild_id, bingo_name, user_id, flattened)

	return items_2d

# Get Bingo Card Button classes

class BingoButton(discord.ui.Button):
	def __init__(self, label:str, row:int, col:int, guild_id:int, bingo_name:str, card_owner_id:int):
		super().__init__(label=label, style=discord.ButtonStyle.secondary, row=row)
		self.row_idx = row
		self.col_idx = col
		self.guild_id = guild_id
		self.bingo_name = bingo_name
		self.card_owner_id = card_owner_id

	async def callback(self, interaction: discord.Interaction):
		if interaction.user.id != self.card_owner_id:
			await interaction.response.send_message(not_your_bingo, ephemeral=True)
			return

		items = toggle_bingo_item(self.guild_id, self.bingo_name, self.card_owner_id, self.row_idx, self.col_idx)
		view = BingoView(self.guild_id, self.bingo_name, self.card_owner_id, items)
		embed = get_complete_bingo_embed(self.guild_id, self.card_owner_id, self.bingo_name, items)

		await interaction.response.edit_message(embed=embed, view=view)

class BingoView(discord.ui.View):
	def __init__(self, guild_id:int, bingo_name:str, card_owner_id:int, items:list):
		super().__init__(timeout=None)
		for r in range(5):
			for c in range(5):
				label = items[r][c].replace("~~", "")
				label = self.format_label(label, r, c)
				btn = BingoButton(label, r, c, guild_id, bingo_name, card_owner_id)
				if is_item_checked(items[r][c]):
					btn.style = discord.ButtonStyle.success
				self.add_item(btn)

	def format_label(self, label:str, row:int, col:int, length:int=30) -> str:
		position = f"({row + 1}, {col + 1}) "
		label = position + label
		if len(label) > length:
			label = label[:length - 3] + "..."
		return label

# Other Commands

def get_all_bingo_templates() -> Optional[discord.Embed]:
	templates = database_module.get_all_bingo_templates()
	if not templates:
		logger_module.log(LOG_INFO, "No bingo templates found.")
		return None

	embed = discord.Embed(title="Bingo Templates", colour=colour_white)
	for guild_id, guild_templates in templates.items():
		template_text = ""
		for template in guild_templates:
			template_text += f"{template[0]} (Free Space: {template[1]})\n"
			guild_name = utils_module.discord_bot.get_guild(guild_id)
		embed.add_field(name=f"Guild {guild_name}", value=template_text, inline=False)
	return embed

def get_bingo_templates_for_guild(guild_id:int) -> Optional[discord.Embed]:
	templates = database_module.get_all_bingo_templates_for_guild(guild_id)
	if not templates:
		logger_module.log(LOG_INFO, f"No bingo templates found for guild {guild_id}.")
		return None

	guild_name = utils_module.discord_bot.get_guild(guild_id)
	embed = discord.Embed(title=f"Bingo Templates for Guild {guild_name}", colour=colour_white)
	for template in templates:
		embed.add_field(name=template[0], value=f"Free Space: {template[1]}", inline=False)
	return embed

def create_bingo_template(guild_id:int, bingo_name:str, free_space:bool, items_str:str) -> bool:
	if (free_space and len(items_str.split("\n")) < 24) or (not free_space and len(items_str.split("\n")) < 25):
		return False
	
	database_module.create_bingo_template(guild_id, bingo_name, free_space, items_str)
	logger_module.log(LOG_INFO, f"Created bingo template '{bingo_name}' for guild {guild_id}.")
	return True

def delete_bingo_template(guild_id:int, bingo_name:str) -> bool:
	if not database_module.does_bingo_template_exist(guild_id, bingo_name):
		return False

	database_module.delete_bingo_template(guild_id, bingo_name)
	logger_module.log(LOG_INFO, f"Deleted bingo template '{bingo_name}' for guild {guild_id}.")
	return True

def reset_bingo_card(guild_id: int, bingo_name: str, user_id: int):
	items = split_bingo_card_items(database_module.get_bingo_card(guild_id, bingo_name, user_id))
	for r in range(5):
		for c in range(5):
			if items[r][c] != free_space_item:
				items[r][c] = uncheck_bingo_item(items[r][c])

	flattened = [item for sublist in items for item in sublist]
	database_module.update_bingo_card(guild_id, bingo_name, user_id, flattened)

def get_bingo_card_items_embed(guild_id:int, bingo_name:str, user_id:int) -> discord.Embed:
	embed = create_bingo_embed(guild_id, user_id, bingo_name)	
	if not does_bingo_card_exist(guild_id, bingo_name, user_id):
		embed.description = f"You have no bingo card for the {bingo_name} bingo"
		return embed

	items = split_bingo_card_items(database_module.get_bingo_card(guild_id, bingo_name, user_id))
	embed = update_bingo_embed_items(embed, items)

	for row in range(len(items)):
		first = f":one: {items[row][0]}"
		second = f":two: {items[row][1]}"
		third = f":three: {items[row][2]}"
		fourth = f":four: {items[row][3]}"
		fifth = f":five: {items[row][4]}"
		embed.add_field(name=f"Row {row + 1}", value="\n".join([first, second, third, fourth, fifth]), inline=False)

	return embed
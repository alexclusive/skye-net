import discord

from .. import commands_module as commands
from .. import logger
from .. import utils
from ..handlers import train_game as train_game_handler

'''
 - train_game_rules
 - train_game
 '''

@utils.discord_bot.tree.command(description="Train game - explanation of rules")
async def train_game_rules(interaction:discord.Interaction):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)

	try:
		rules = "In each car for every train, there is a four digit number.\n"
		rules += "We break down the number into four separate digits, and perform simple arithmetic operations to reach a specified target.\n"
		rules += "In general, the target number is 10 (but you can also use any other integer).\n"
		rules += "By default, the operations are: addition (+), subtraction (-), multiplication (*), and division (/).\n"
		rules += "Optionally, with strict_mode you can also use power/exponentiation (^), and modulo (%). This also disallows permutation of the digits.\n"
	
		embed = discord.Embed(title="Train Game Rules", colour=0xffffff, description=rules)
	
		await interaction.followup.send(embed=embed)
	except Exception as e:
		print(f"Error getting train game rules: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@discord.app_commands.describe(
	number="The starting number for the game - four digits",
	target="The target number to reach - default 10",
	strict_mode="Only use basic operations (+-*/), and do not permutate the numbers - default False"
)
@utils.discord_bot.tree.command(description="Train game - get to [target] using (+-*/) and optionally (^%)")
async def train_game(
	interaction:discord.Interaction,
	number:str,
	target:int = 10,
	strict_mode:bool = False,
):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)

	try:
		try:
			target = int(target)
			if len(number) != 4:
				await interaction.followup.send("`" + number + "` is not valid for the train game. Please give a four digit number (0000-9999).")
				return
			a = int(number[0]) # these will raise an exception if they can't convert
			b = int(number[1])
			c = int(number[2])
			d = int(number[3])
		except Exception as e:
			print(f"Train game: error converting. {e}")
			await interaction.followup.send("Sorry! Unable to compute.")
			return
		await train_game_handler.train_game(interaction, number, a, b, c, d, target, strict_mode)
	except Exception as e:
		print(f"Error getting train game: {e}")
		await interaction.followup.send(commands.something_went_wrong)
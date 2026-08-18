import discord

import handlers.database as database_module

async def print_number_fact(interaction:discord.Interaction, number:int):
	fact = get_number_fact(number)
	if fact is None:
		await interaction.followup.send(f"No fact found for {number}.")
	else:
		await interaction.followup.send(f"Fact for {number}: {fact}\nMore facts can be found at https://oeis.org/search?q={number}&language=english&go=Search")

def get_number_fact(number:int) -> str:
	fact = database_module.get_number_fact(number)
	if fact is None:
		return ""
	else:
		return fact
import os
import sys
import platform
import signal
import discord

from assets import core_utils
from assets.core_utils import is_owner, discord_bot

nice_try = "Guess you're not cool enough for this one �"

async def die(interaction:discord.Interaction):
	if not is_owner(interaction):
		await interaction.followup.send(nice_try)
		return
	await interaction.followup.send("Going to sleep... Goodnight!")
	await discord_bot.close()
	
	if platform.system() == "Windows":
		os.kill(os.getpid(), signal.SIGTERM)
	else:
		os.kill(os.getpid(), signal.SIGKILL)

async def restart(interaction:discord.Interaction):
	if not core_utils.is_owner(interaction):
		await interaction.followup.send(nice_try)
		return
	await interaction.followup.send("Restarting the bot...", ephemeral=True)

	try:
		await discord_bot.close()
		os.execl(sys.executable, sys.executable, *sys.argv)
	except Exception as e:
		await interaction.followup.send(f"Failed to restart: {e}")

async def delete_message_by_id(interaction:discord.Interaction, id):
	if not core_utils.is_owner(interaction):
		await interaction.followup.send(nice_try)
		return
	try:
		channel = interaction.channel
		message = await channel.fetch_message(id)
		await message.delete()
		await interaction.followup.send("Deleted", ephemeral=True)
	except Exception as e:
		await interaction.followup.send(e)
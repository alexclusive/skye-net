import os
import sys
from discord.ext import commands

from assets import core_utils

bot = commands.Bot()

nice_try = "Nice try bozo :)"

async def restart(ctx):
	if not core_utils.is_owner(ctx):
		await ctx.respond(nice_try)
		return
	await ctx.respond("Restarting the bot...", ephemeral=True)

	try:
		await bot.close()
		os.execl(sys.executable, sys.executable, *sys.argv)
	except Exception as e:
		await ctx.followup.send(f"Failed to restart: {e}")

async def delete_message_by_id(ctx, id):
	if not core_utils.is_owner(ctx):
		await ctx.respond(nice_try)
		return
	try:
		channel = ctx.channel
		message = await channel.fetch_message(id)
		await message.delete()
		await ctx.respond("Deleted", ephemeral=True)
	except Exception as e:
		await ctx.respond(e)
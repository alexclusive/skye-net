from discord.errors import Forbidden
import discord

import handlers.utils as utils_module
import handlers.database as database_module
import handlers.helpers.bot_ping as bot_ping_module
import handlers.helpers.triggers as triggers_module

async def message(message):
	try:
		if message.author == utils_module.discord_bot.user:
			return

		message_sent = False
		if utils_module.discord_bot.user in message.mentions:
			await bot_ping_module.handle_bot_ping(message)
			message_sent = True
	except Exception as e:
		print(f"on_message: openai interaction{e}")

	try:
		opted_out_users = database_module.get_all_opt_out_users()
		if int(message.author.id) in opted_out_users:
			return
		await triggers_module.handle_reactions(message, utils_module.all_emojis)
		if not message_sent:
			await triggers_module.handle_triggers(message, utils_module.all_emojis)
	except Forbidden as e:
		if e.code == 90001: # blocked
			print(f"on_message: I was blocked by user {message.author} :(")
		else:
			print(f"on_message: reactions/triggers {e}")
	except Exception as e:
		print(f"on_message: reactions/triggers {e}")

async def message_deleted(message:discord.Message):
	try:
		if message.author == utils_module.discord_bot.user:
			return
		if message.guild is None:
			return # ignore DMs
		
		log_channel = message.guild.get_channel(utils_module.message_log_channel)
		if log_channel is None:
			return

		embed = discord.Embed(
			title=f"Message Deleted in {message.channel.mention}",
			colour=0xff0000
		)
		embed.set_author(name=message.author.name, icon_url=message.author.display_avatar.url)
		embed.timestamp = message.created_at
		
		if message.content:
			embed.add_field(name="Content", value=message.content, inline=False)
		if message.attachments:
			embed.add_field(name="Attachments", value="\n".join([attachment.url for attachment in message.attachments]), inline=False)

		await log_channel.send(embed=embed)
	except Exception as e:
		print(f"on_message_delete: {e}")
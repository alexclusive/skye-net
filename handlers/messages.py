from discord.errors import Forbidden

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
import discord
import re
from datetime import datetime as dt

from .. import utils
from .. import logger
from .. import database_module as database
from ..handlers import spotify as spotify_handler
from ..handlers import openAI as openAI_handler
from ..handlers import triggers as triggers_handler

'''
 - on_message
 - on_message_delete
'''

async def message(message:discord.Message):
	try:
		if message.author == utils.discord_bot.user:
			return
		if message.webhook_id is not None:
			return

		message_sent = False
		if utils.discord_bot.user in message.mentions:
			await openAI_handler.handle_bot_ping(message)
			message_sent = True
	except Exception as e:
		print(f"on_message: openai interaction {e}")

	try:
		spotify_tracks = re.findall(r"https?://open\.spotify\.com/track/[a-zA-Z0-9]+", message.content)
		spotify_albums = re.findall(r"https?://open\.spotify\.com/album/[a-zA-Z0-9]+", message.content)
		spotify_playlists = re.findall(r"https?://open\.spotify\.com/playlist/[a-zA-Z0-9]+", message.content)

		if len(spotify_tracks) > 0 or len(spotify_albums) > 0 or len(spotify_playlists) > 0:
			logger.log(logger.LOG_EXTRA_DETAIL, f"Found spotify details - {len(spotify_tracks)} tracks, {len(spotify_albums)} albums, and {len(spotify_playlists)} playlists in message.")

			for link in spotify_tracks:
				embed = spotify_handler.get_spotify_track_embed(link)
				if embed:
					await message.reply(embed=embed, mention_author=False)
					message_sent = True
	
			for link in spotify_albums:
				embed = spotify_handler.get_spotify_album_embed(link)
				if embed:
					await message.reply(embed=embed, mention_author=False)
					message_sent = True
	
			for link in spotify_playlists:
				embed = spotify_handler.get_spotify_playlist_embed(link)
				if embed:
					await message.reply(embed=embed, mention_author=False)
					message_sent = True
	except Exception as e:
		print(f"on_message: spotify embed {e}")

	try:
		opted_out_users = database.get_all_opt_out_users()
		if str(message.author.id) in opted_out_users:
			logger.log(logger.LOG_EXTRA_DETAIL, f"User {message.author.name} opted out of reactions.")
			return
		
		await triggers_handler.handle_reactions(message, utils.all_emojis)
		if not message_sent:
			await triggers_handler.handle_triggers(message, utils.all_emojis)
	except discord.errors.Forbidden as e:
		if e.code == 90001: # blocked
			print(f"on_message: I was blocked by user {message.author} :(")
			logger.log(logger.LOG_EXTRA_DETAIL, f"User {message.author.name} blocked Skyenet :(")
		else:
			print(f"on_message: reactions/triggers {e}")
	except discord.NotFound as e:
		if e.status == 404 and e.code == 10008:
			logger.log(logger.LOG_EXTRA_DETAIL, "Attempted to react to a message that was deleted.")
			return # message was deleted before we could react to it
	except Exception as e:
		print(f"on_message: reactions/triggers {e}")

async def message_deleted(message:discord.Message, retrying:bool=False):
	try:
		if message.author == utils.discord_bot.user:
			return
		if message.guild is None:
			return # ignore DMs
		
		log_channel = utils.get_default_log_channel()
		if log_channel is None:
			return
			
		if len(message.content) > 1500:
			message.content = message.content[:1500] + "..."  # truncate long messages

		embeds:list[discord.Embed] = []
		if message.content and len(message.content) > 900:
			# We need to send more than one message (Discord has a 1024 character limit)
			num_messages_needed = len(message.content) // 900 + 1
			for i in range(num_messages_needed):
				embed_part = discord.Embed(
					title=f"Message Deleted in {message.channel.mention} (Part {i+1} of {num_messages_needed})",
					colour=0xff0000
				)

				start = i * 900
				end = start + 900
				embed_part.add_field(name="Content", value=message.content[start:end], inline=False)
				
				embeds.append(embed_part)
		else:
			# Only need one message
			embed = discord.Embed(
				title=f"Message Deleted in {message.channel.mention}",
				colour=0xff0000
			)
			if message.content:
				embed.add_field(name="Content", value=message.content, inline=False)
			embeds.append(embed)

		if message.attachments and len(embeds) > 0:
			# Add any attachements to just the first embed
			try:
				await log_channel.send(files=[await x.to_file() for x in message.attachments]) # discord.NotFound will be raised here
				embeds[0].add_field(name="Attachments", value="\n".join([attachment.url for attachment in message.attachments]), inline=False)
			except discord.NotFound as e:
				logger.log(logger.LOG_DETAIL, f"Error attempting to retrieve message attachments from a message that was deleted. Error: {e}")
				if e.status == 404 and e.code == 0:
					attachment_urls = "\n".join([attachment.url for attachment in message.attachments])
					if attachment_urls:
						embed_message = "Attachment/s could not be retrieved normally, using direct URLs:\n" + attachment_urls
						embeds[0].add_field(name="Attachments", value=embed_message, inline=False)
					else:
						embeds[0].add_field(name="Attachments", value="Attachment/s could not be retrieved after deletion", inline=False)

		# Add the original sent time to the first embed if possible
		try:
			if hasattr(message, "created_at") and message.created_at is not None and len(embeds) > 0:
				# use the same formatter as other handlers
				created_timestamp = int(message.created_at.timestamp())
				now_timestamp = int(dt.now(utils.timezone_here).timestamp())
				time_between = now_timestamp - created_timestamp

				created_timestamp_formatted = utils.get_timestamp_formatted(created_timestamp)
				now_timestamp_formatted = utils.get_timestamp_now_formatted()
				time_between_formatted = utils.format_time_difference(time_between)

				formatted = f"Sent {created_timestamp_formatted}\nDeleted {now_timestamp_formatted}\nUp Time {time_between_formatted}"

				embeds[0].add_field(name="Sent At", value=formatted, inline=False)
		except Exception:
			# non-fatal: if timestamp formatting fails, just don't add the field
			pass

		for embed in embeds:
			embed.set_author(name=message.author.name, icon_url=message.author.display_avatar.url)
			embed.timestamp = dt.now(utils.timezone_here)
			embed.set_footer(text=f"Message ID: {message.id}")
			await log_channel.send(embed=embed)
	except OSError as e:
		if e.errno == 32:  # Broken pipe
			if not retrying:
				await message_deleted(message, retrying=True)
			else:
				print(f"message_deleted (after retry): {e}")
	except Exception as e:
		if e.errno == 400:  # Bad Request
			if not retrying:
				await message_deleted(message, retrying=True)
				# try again but this time send attachments in separate message
			else:
				print(f"message_deleted (after retry): {e}")
		print(f"message_deleted: {e}")
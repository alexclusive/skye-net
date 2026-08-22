import discord
import re

from .. import logger
from .. import utils

async def handle_reactions(message:discord.Message, emojis:dict):
	'''
		React to message when certain content is found
	'''
	# birth in vc	🤰
	# headpat		<:Headpat:1309732487412580392>
	# lesbian		<:LesbianBrick:1329672980443435070>
	# mwah			💋
	# nomnom		<:Chomp:1309732491862609930>
	# not far		<:NotFar:1300683648650973306>
	# perchance		🦀
	# perhaps		🦀
	# prey animal	🐰
	# hear no evil	🙉
	# see no evil	🙈
	# skye net		🤖
	# skyenet		🤖
	# skynet		🤖
	# speak no evil	🙊
	# um actually	☝️ 🤓
	# vampire		🧛‍♀️
	# witch			🧙‍♀️
	# what!			‼️
	# yippee		<:AutismCreature:1235124052813807658>
	content = message.content.lower()
	logger.log(logger.LOG_INFO, f"Checking reactions for message {content}")

	# other reactions
	if "birth in vc" in content:
		await message.add_reaction("🤰")
	if "headpat" in content:
		emoji = utils.discord_bot.get_emoji(emojis["HEADPAT"])
		await message.add_reaction(emoji)
	if "hear no evil" in content:
		await message.add_reaction("🙉")
	if "lesbian" in content:
		emoji = utils.discord_bot.get_emoji(emojis["LESBIAN_BRICK"])
		await message.add_reaction(emoji)
	if re.search(r'\bmwah\b', content): # don't match mwaha
		await message.add_reaction("💋")
	if "nomnom" in content:
		emoji = utils.discord_bot.get_emoji(emojis["CHOMP"])
		await message.add_reaction(emoji)
	if "not far" in content:
		emoji = utils.discord_bot.get_emoji(emojis["NOT_FAR"])
		await message.add_reaction(emoji)
	if 'perchance' in content:
		await message.add_reaction("🦀")
	if 'perhaps' in content:
		await message.add_reaction("🦀")
	if 'prey animal' in content:
		await message.add_reaction("🐰")
	if "see no evil" in content:
		await message.add_reaction("🙈")
	if "skye net" in content\
		or "skyenet" in content\
		or "skynet" in content:
		await message.add_reaction("🤖")
	if "speak no evil" in content:
		await message.add_reaction("🙊")
	if "um actually" in content:
		await message.add_reaction("☝️")
		await message.add_reaction("🤓")
	if "vampire" in content:
		await message.add_reaction("🧛‍♀️")
	if re.search(r'\bwitch\b', content): # don't match 'switch'
		await message.add_reaction("🧙‍♀️")
	if "what!" in content:
		await message.add_reaction("‼️")
	if "yippee" in content:
		emoji = utils.discord_bot.get_emoji(emojis["AUTISM_CREATURE"])
		await message.add_reaction(emoji)

async def handle_triggers(message:discord.Message, emojis:dict) -> None:
	'''
		Respond to message when certain content is found
	'''
	# 500 cigarettes		5️⃣0️⃣0️⃣🚬
	# i know what you are	🫵
	# nuh uh				<a:no:1300690431373217802> <a:WaggingFinger:1300743838926770186>
	# oh.					🫥
	content = message.content.lower()
	logger.log(logger.LOG_INFO, f"Checking triggers for message {content}")

	if "500 cigarettes" in content:
		contents = "5️⃣0️⃣0️⃣🚬"
		await message.reply(contents, mention_author=False)
	if "i know what you are" in content:
		await message.reply(":index_pointing_at_the_viewer:", mention_author=False)
	if "nuh uh" in content:
		emoji = utils.discord_bot.get_emoji(emojis["NUH_UH"])
		nuhuh = format_emoji(emoji, True)
		emoji = utils.discord_bot.get_emoji(emojis["WAGGING_FINGER"])
		wagging = format_emoji(emoji, True)

		contents = nuhuh + wagging
		await message.reply(contents, mention_author=False)
	if re.fullmatch(r"oh\.+", content):
		contents = "🫥" # dotted line neutral face
		await message.reply(contents, mention_author=False)
	
def format_emoji(emoji:discord.Emoji, animated:bool=False) -> str:
	if emoji:
		if animated:
			return f"<a:{emoji.name}:{emoji.id}>"
		return f"<:{emoji.name}:{emoji.id}>"
	else:
		return ""
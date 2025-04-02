import re

import handlers.utils as utils_module

async def handle_reactions(message, emojis):
	'''
		React to message when certain content is found
	'''
	# birth in vc	🤰
	# bouldering	🧗‍♀️
	# headpat		<:Headpat:1309732487412580392>
	# lesbian		<:LesbianBrick:1329672980443435070>
	# mwah			💋
	# nomnom		<:Chomp:1309732491862609930>
	# not far		<:NotFar:1300683648650973306>
	# oasis			🏝️
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
	# witch			🧙‍♀️
	# what!			‼️
	# yippee		<:AutismCreature:1235124052813807658>
	content = message.content.lower()
	await handle_reactions_vtm(message, emojis, content)	

	# other reactions
	if "birth in vc" in content:
		await message.add_reaction("🤰")
	if "boulder" in content:
		await message.add_reaction("🧗‍♀️")
	if "headpat" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["HEADPAT"])
		await message.add_reaction(emoji)
	if "hear no evil" in content:
		await message.add_reaction("🙉")
	if "lesbian" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["LESBIAN_BRICK"])
		await message.add_reaction(emoji)
	if "mwah" in content:
		await message.add_reaction("💋")
	if "nomnom" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["CHOMP"])
		await message.add_reaction(emoji)
	if "not far" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["NOT_FAR"])
		await message.add_reaction(emoji)
	if "oasis" in content:
		await message.add_reaction("🏝️")
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
	if re.search(r'\bwitch\b', content): # don't match 'switch'
		await message.add_reaction("🧙‍♀️")
	if "what!" in content:
		await message.add_reaction("‼️")
	if "yippee" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["AUTISM_CREATURE"])
		await message.add_reaction(emoji)

async def handle_reactions_vtm(message, emojis, content):
	# anarch		<:VTM_Anarch:1297549861750571078>
	# banu haqim	<:VTM_BanuHaqim:1297549896080953454>
	# book of nod	<:VTM_BookOfNod:1297549855576817756>
	# brujah		<:VTM_Brujah:1297549893182685276>
	# camarilla		<:VTM_Camarilla:1297549864002916366>
	# coterie		<:VTM:1297549858139410483>
	# gangrel		<:VTM_Gangrel:1297549906042425385>
	# hecata		<:VTM_Hecata:1297549898270507108>
	# kindred		<:VTM:1297549858139410483>
	# lasombra		<:VTM_Lasombra:1297549915265957928>
	# malkavian		<:VTM_Malkavian:1297549917534818376>
	# ministry		<:VTM_Ministry:1297549852468711434>
	# nosferatu		<:VTM_Nosferatu:1297549890750251070>
	# ravnos		<:VTM_Ravnos:1297549910974922883>
	# sabbat		<:VTM_Sabbat:1327974479120437341>
	# toreador		<:VTM_Toreador:1297549886631182437>
	# tremere		<:VTM_Tremere:1297549908634767515>
	# tzimisce		<:VTM_Tzimisce:1297549903873970278>
	# vampire		🧛‍♀️
	# ventrue		<:VTM_Ventrue:1297549883930054676>
	# vtm			🧛‍♀️ <:VTM:1297549858139410483>

	if "anarch" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["VTM_ANARCH"])
		await message.add_reaction(emoji)
	if "banu haqim" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["VTM_BANU_HAQIM"])
		await message.add_reaction(emoji)
	if "book of nod" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["VTM_BOOK_OF_NOD"])
		await message.add_reaction(emoji)
	if "brujah" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["VTM_BRUJAH"])
		await message.add_reaction(emoji)
	if "camarilla" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["VTM_CAMARILLA"])
		await message.add_reaction(emoji)
	if "coterie" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["VTM"])
		await message.add_reaction(emoji)
	if "gangrel" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["VTM_GANGREL"])
		await message.add_reaction(emoji)
	if "hecata" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["VTM_HECATA"])
		await message.add_reaction(emoji)
	if "kindred" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["VTM"])
		await message.add_reaction(emoji)
	if "lasombra" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["VTM_LASOMBRA"])
		await message.add_reaction(emoji)
	if "malkavian" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["VTM_MALKAVIAN"])
		await message.add_reaction(emoji)
	if "ministry" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["VTM_MINISTRY"])
		await message.add_reaction(emoji)
	if "nosferatu" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["VTM_NOSFERATU"])
		await message.add_reaction(emoji)
	if "ravnos" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["VTM_RAVNOS"])
		await message.add_reaction(emoji)
	if "sabbat" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["VTM_SABBAT"])
		await message.add_reaction(emoji)
	if "toreador" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["VTM_TOREADOR"])
		await message.add_reaction(emoji)
	if "tremere" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["VTM_TREMERE"])
		await message.add_reaction(emoji)
	if "tzimisce" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["VTM_TZIMISCE"])
		await message.add_reaction(emoji)
	if "vampire" in content:
		await message.add_reaction("🧛‍♀️")
	if "ventrue" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["VTM_VENTRUE"])
		await message.add_reaction(emoji)
	if "vtm" in content:
		await message.add_reaction("🧛‍♀️")
		emoji = utils_module.discord_bot.get_emoji(emojis["VTM"])
		await message.add_reaction(emoji)

async def handle_triggers(message, emojis):
	'''
		Respond to message when certain content is found
	'''
	# 500 cigarettes		5️⃣0️⃣0️⃣🚬
	# i know what you are	<:point:1116044591196549120>
	# nuh uh				<a:no:1300690431373217802> <a:WaggingFinger:1300743838926770186>
	# oh.					🫥
	content = message.content.lower()

	if "500 cigarettes" in content:
		contents = "5️⃣0️⃣0️⃣🚬"
		await message.reply(contents, mention_author=False)
	if "i know what you are" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["POINT"])
		point = format_emoji(emoji)
		await message.reply(point, mention_author=False)
	if "nuh uh" in content:
		emoji = utils_module.discord_bot.get_emoji(emojis["NUH_UH"])
		nuhuh = format_emoji(emoji)
		emoji = utils_module.discord_bot.get_emoji(emojis["WAGGING_FINGER"])
		wagging = format_emoji(emoji)

		contents = nuhuh + wagging
		await message.reply(contents, mention_author=False)
	if "oh." in content:
		contents = "🫥" # dotted line neutral face
		await message.reply(contents, mention_author=False)
	
def format_emoji(emoji):
	if emoji:
		return f"<:{emoji.name}:{emoji.id}>"
	else:
		return ""
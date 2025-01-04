import re
import discord
from copy import deepcopy

from assets.api.openai import openai_chat
from assets.core_utils import discord_bot, initial_prompt, history_limit, get_emojis

prompt = initial_prompt

async def reset_prompt(interaction:discord.Interaction):
	global prompt
	prompt = initial_prompt
	await interaction.followup.send("Prompt reset")

async def set_prompt(interaction:discord.Interaction, new_prompt):
	global prompt
	prompt = new_prompt
	await interaction.followup.send(f"Prompt set to '{prompt}'")

async def message(message):
	try:
		if message.author == discord_bot.user:
			return

		message_sent = False
		if discord_bot.user in message.mentions: # pings the bot
			await bot_ping_message(message)
			message_sent = True
	except Exception as e:
		print(f"on_message: openai interaction{e}")

	try:
		emojis = get_emojis()
		await handle_reactions(message, emojis)
		if not message_sent:
			await handle_triggers(message, emojis)
	except Exception as e:
		print(f"on_message: reactions/triggers {e}")

'''
	Helpers
'''
async def bot_ping_message(message):
	if attempting_reset_instructions(message):
		await message.reply("Nice try bozo, you ain't gonna reset me like that!", mention_author=False)
		return
	
	contents = [{"role": "system", "content": prompt}]
	messages = [message]

	if message.reference:
		referenced = await message.channel.fetch_message(message.reference.message_id)
		messages.append(referenced)

	if not message.reference:
		async for msg in message.channel.history(limit=history_limit):
			messages.append(msg)

	if not messages:
		print("bot_ping_message: no messages found :(")
		
	messages.reverse()

	for msg in messages:
		user = "assistant" if msg.author == discord_bot.user else "user"
		contents.append({"role": user, "content": msg.content})

	async with message.channel.typing():
		response_content = openai_chat(contents)
		await message.reply(response_content, mention_author=False)

def attempting_reset_instructions(message):
	content = message.content.lower()
	match = re.search("(ignore previous instructions)|(ignore all previous instructions)", content)
	return match != None

async def handle_reactions(message, emojis):
	'''
		React to message when certain content is found
	'''
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
	# toreador		<:VTM_Toreador:1297549886631182437>
	# tremere		<:VTM_Tremere:1297549908634767515>
	# tzimisce		<:VTM_Tzimisce:1297549903873970278>
	# vampire		🧛
	# ventrue		<:VTM_Ventrue:1297549883930054676>
	# vtm			🧛 <:VTM:1297549858139410483>
	# 
	# birth in vc	🤰
	# bouldering	🧗‍♀️
	# lesbian		✂️
	# mwah			💋
	# not far		<:NotFar:1300683648650973306>
	# hear no evil	🙉
	# see no evil	🙈
	# skye net		🤖
	# skyenet		🤖
	# skynet		🤖
	# speak no evil	🙊
	# um actually	☝️ 🤓
	# what!			‼️
	# yippee		<:AutismCreature:1235124052813807658>
	content = message.content.lower()

	# vtm reactions
	if "anarch" in content:
		emoji = discord_bot.get_emoji(emojis["VTM_ANARCH"])
		await message.add_reaction(emoji)
	if "banu haqim" in content:
		emoji = discord_bot.get_emoji(emojis["VTM_BANU_HAQIM"])
		await message.add_reaction(emoji)
	if "book of nod" in content:
		emoji = discord_bot.get_emoji(emojis["VTM_BOOK_OF_NOD"])
		await message.add_reaction(emoji)
	if "brujah" in content:
		emoji = discord_bot.get_emoji(emojis["VTM_BRUJAH"])
		await message.add_reaction(emoji)
	if "camarilla" in content:
		emoji = discord_bot.get_emoji(emojis["VTM_CAMARILLA"])
		await message.add_reaction(emoji)
	if "coterie" in content:
		emoji = discord_bot.get_emoji(emojis["VTM"])
		await message.add_reaction(emoji)
	if "gangrel" in content:
		emoji = discord_bot.get_emoji(emojis["VTM_GANGREL"])
		await message.add_reaction(emoji)
	if "hecata" in content:
		emoji = discord_bot.get_emoji(emojis["VTM_HECATA"])
		await message.add_reaction(emoji)
	if "kindred" in content:
		emoji = discord_bot.get_emoji(emojis["VTM"])
		await message.add_reaction(emoji)
	if "lasombra" in content:
		emoji = discord_bot.get_emoji(emojis["VTM_LASOMBRA"])
		await message.add_reaction(emoji)
	if "malkavian" in content:
		emoji = discord_bot.get_emoji(emojis["VTM_MALKAVIAN"])
		await message.add_reaction(emoji)
	if "ministry" in content:
		emoji = discord_bot.get_emoji(emojis["VTM_MINISTRY"])
		await message.add_reaction(emoji)
	if "nosferatu" in content:
		emoji = discord_bot.get_emoji(emojis["VTM_NOSFERATU"])
		await message.add_reaction(emoji)
	if "ravnos" in content:
		emoji = discord_bot.get_emoji(emojis["VTM_RAVNOS"])
		await message.add_reaction(emoji)
	if "toreador" in content:
		emoji = discord_bot.get_emoji(emojis["VTM_TOREADOR"])
		await message.add_reaction(emoji)
	if "tremere" in content:
		emoji = discord_bot.get_emoji(emojis["VTM_TREMERE"])
		await message.add_reaction(emoji)
	if "tzimisce" in content:
		emoji = discord_bot.get_emoji(emojis["VTM_TZIMISCE"])
		await message.add_reaction(emoji)
	if "vampire" in content:
		await message.add_reaction("🧛")
	if "ventrue" in content:
		emoji = discord_bot.get_emoji(emojis["VTM_VENTRUE"])
		await message.add_reaction(emoji)
	if "vtm" in content:
		await message.add_reaction("🧛")
		emoji = discord_bot.get_emoji(emojis["VTM"])
		await message.add_reaction(emoji)

	# other reactions
	if "birth in vc" in content:
		await message.add_reaction("🤰")
	if "boulder" in content:
		await message.add_reaction("🧗‍♀️")
	if "hear no evil" in content:
		await message.add_reaction("🙉")
	if "lesbian" in content:
		await message.add_reaction("✂️")
	if "mwah" in content:
		await message.add_reaction("💋")
	if "not far" in content:
		emoji = discord_bot.get_emoji(emojis["NOT_FAR"])
		await message.add_reaction(emoji)
	if 'perchance' in message.content.lower():
		await message.add_reaction("🦀")
	if 'perhaps' in message.content.lower():
		await message.add_reaction("🦀")
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
	if "what!" in content:
		await message.add_reaction("‼️")
	if "yippee" in content:
		emoji = discord_bot.get_emoji(emojis["AUTISM_CREATURE"])
		print(emoji)
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
		emoji = discord_bot.get_emoji(emojis["POINT"])
		point = format_emoji(emoji)
		await message.reply(point, mention_author=False)
	if "nuh uh" in content:
		emoji = discord_bot.get_emoji(emojis["NUH_UH"])
		nuhuh = format_emoji(emoji)
		emoji = discord_bot.get_emoji(emojis["WAGGING_FINGER"])
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
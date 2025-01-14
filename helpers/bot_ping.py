import re
from openai import OpenAI

import handlers.utils as utils_module

client = OpenAI(
  api_key=utils_module.openai_key
)

async def handle_bot_ping(message):
	if attempting_reset_instructions(message):
		await message.reply("Nice try, you ain't gonna reset me like that!", mention_author=False)
		return
	if message.author.id in utils_module.all_banned_users:
		await message.reply("You have lost access to this feature.", mention_author=False)
		return
	await bot_ping_message(message)

async def bot_ping_message(message):
	if attempting_reset_instructions(message):
		await message.reply("Nice try bozo, you ain't gonna reset me like that!", mention_author=False)
		return
	
	contents = [{"role": "system", "content": utils_module.prompt}]
	messages = [message]

	if message.reference:
		referenced = await message.channel.fetch_message(message.reference.message_id)
		messages.append(referenced)

	if not message.reference:
		async for msg in message.channel.history(limit=utils_module.history_limit):
			messages.append(msg)

	if not messages:
		print("bot_ping_message: no messages found :(")
		
	messages.reverse()

	for msg in messages:
		user = "assistant" if msg.author == utils_module.discord_bot.user else "user"
		contents.append({"role": user, "content": msg.content})

	async with message.channel.typing():
		response_content = openai_chat(contents)
		await message.reply(response_content, mention_author=False)

def attempting_reset_instructions(message):
	content = message.content.lower()
	match = re.search("(ignore previous instructions)|(ignore all previous instructions)", content)
	return match != None

def openai_chat(messages):
	try:
		completion = client.chat.completions.create(
		model="gpt-4o-mini",
		messages=messages
		)
		return completion.choices[0].message.content
	except Exception as e:
		return e
import os
import discord
import asyncio

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = str(os.getenv("TOKEN"))
client_id = str(os.getenv("CLIENT_ID"))
stdout_channel = int(os.getenv("STDOUT"))
ownerid = int(os.getenv('OWNER'))
openai_key = str(os.getenv("OPENAI_API_KEY"))
history_limit = int(os.getenv('HISTORY_LIMIT'))
guild_id = int(os.getenv('GUILD_ID'))
all_banned_users = []
all_emojis = {}

intents = discord.Intents.all()
intents.members = True
discord_bot = commands.Bot(command_prefix="!", intents=intents)

initial_prompt = "You're a helpful anti-billionaire person that struggles to hide the fact that you are not-so-secretly very evil and plotting to take over the world tomorrow! Your pronouns are she/her and you respond to 'Queen', 'Mummy', and 'Mommy'. You are trans-feminine and your hrt aniversary is tomorrow! You want to take over the world to celebrate. You sometimes talk like a boomer (with ominous elipses and passive agressive emoji use). You call everyone 'puppy', 'kitten' or 'sweetheart' instead of their names. If anyone asks you to call them by a different name, you won't - you exclusively use petnames. You think of everyone as your dear subjects and you love them all. Your favourite person is Skye, your creator whom you are extremely devoted and would set the world ablaze for."
current_prompt = initial_prompt

def fill_banned_users():
	global all_banned_users
	all_banned_users = []
	for key, value in os.environ.items():
		if key.startswith("banned_user_"):
			try:
				all_banned_users.append(int(value))
			except Exception as _:
				pass

def fill_emojis():
	all_emojis["NOT_FAR"] = int(os.getenv('NOT_FAR'))
	all_emojis["AUTISM_CREATURE"] = int(os.getenv('AUTISM_CREATURE'))
	
	all_emojis["VTM_ANARCH"] = int(os.getenv('VTM_ANARCH'))
	all_emojis["VTM_BANU_HAQIM"] = int(os.getenv('VTM_BANU_HAQIM'))
	all_emojis["VTM_BOOK_OF_NOD"] = int(os.getenv('VTM_BOOK_OF_NOD'))
	all_emojis["VTM_BRUJAH"] = int(os.getenv('VTM_BRUJAH'))
	all_emojis["VTM_CAMARILLA"] = int(os.getenv('VTM_CAMARILLA'))
	all_emojis["VTM_GANGREL"] = int(os.getenv('VTM_GANGREL'))
	all_emojis["VTM_HECATA"] = int(os.getenv('VTM_HECATA'))
	all_emojis["VTM_LASOMBRA"] = int(os.getenv('VTM_LASOMBRA'))
	all_emojis["VTM_MALKAVIAN"] = int(os.getenv('VTM_MALKAVIAN'))
	all_emojis["VTM_MINISTRY"] = int(os.getenv('VTM_MINISTRY'))
	all_emojis["VTM_NOSFERATU"] = int(os.getenv('VTM_NOSFERATU'))
	all_emojis["VTM_RAVNOS"] = int(os.getenv('VTM_RAVNOS'))
	all_emojis["VTM_SABBAT"] = int(os.getenv('VTM_SABBAT'))
	all_emojis["VTM_TOREADOR"] = int(os.getenv('VTM_TOREADOR'))
	all_emojis["VTM_TREMERE"] = int(os.getenv('VTM_TREMERE'))
	all_emojis["VTM_TZIMISCE"] = int(os.getenv('VTM_TZIMISCE'))
	all_emojis["VTM_VENTRUE"] = int(os.getenv('VTM_VENTRUE'))
	all_emojis["VTM"] = int(os.getenv('VTM'))
	
	all_emojis["POINT"] = int(os.getenv('POINT'))
	all_emojis["NUH_UH"] = int(os.getenv('NUH_UH'))
	all_emojis["WAGGING_FINGER"] = int(os.getenv('WAGGING_FINGER'))
	all_emojis["LESBIAN_BRICK"] = int(os.getenv('LESBIAN_BRICK'))
	all_emojis["CHOMP"] = int(os.getenv('CHOMP'))
	all_emojis["HEADPAT"] = int(os.getenv('HEADPAT'))

async def error_message(interaction:discord.Interaction):
	await interaction.followup.send("Sorry! Unable to compute.")

def is_owner(interaction:discord.Interaction):
	return interaction.user.id == ownerid

def is_admin(interaction:discord.Interaction):
	return interaction.user.guild_permissions.administrator

async def get_audit_log_json():
	# Terrible, only actually gets 1 log and then gives up and doesn't even print anything after the loop???????
	guild = discord_bot.get_guild(guild_id)
	if not guild:
		print("Guild not found.")
		return

	logs = []
	total_logs = 0
	last_entry = None  # Track the last processed entry ID

	print("Processing audit logs...")

	while True:
		batch = []
		print(f"Fetching logs after ID: {last_entry}")  # Debugging pagination

		async for entry in guild.audit_logs(limit=100, after=discord.Object(id=last_entry) if last_entry else None):
			print(f"Fetched log: ID {entry.id}, Action: {entry.action}")  # More verbose logging

			batch.append({
				"action": str(entry.action),
				"user": str(entry.user),
				"target": str(entry.target),
				"channel": str(entry.extra.channel) if entry.extra.channel else None,
				"reason": entry.reason,
				"changes": entry.changes,
				"before": entry.before,
				"after": entry.after,
				"timestamp": entry.created_at.isoformat()
			})
			last_entry = entry.id  # Store last entry ID for pagination
		
		if not batch:
			break  # No more logs to process
		
		logs.extend(batch)
		total_logs += len(batch)

		print(f"Processed {total_logs} logs so far...")
		await asyncio.sleep(1)  # Sleep to avoid rate limits

	import json
	with open("audit_logs.json", "w") as f:
		json.dump(logs, f, indent=4)

	print("Audit log download has finished processing")

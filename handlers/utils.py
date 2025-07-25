import os
import discord
import pytz
from datetime import datetime as dt

from discord.ext import commands
from dotenv import load_dotenv

import handlers.logger as logger_module

from handlers.logger import LOG_SETUP, LOG_INFO, LOG_DETAIL, LOG_EXTRA_DETAIL

received_shutdown = False

load_dotenv()
# Verification
token = str(os.getenv("TOKEN"))
client_id = str(os.getenv("CLIENT_ID"))
ownerid = int(os.getenv("OWNER"))

# Logging
log_file_path = str(os.getenv("LOG_FILE_PATH"))

# Open AI
history_limit = int(os.getenv("HISTORY_LIMIT"))
openai_key = str(os.getenv("OPENAI_API_KEY"))

# Spotify
spotify_client_id = str(os.getenv("SPOTIFY_CLIENT_ID"))
spotify_client_secret = str(os.getenv("SPOTIFY_CLIENT_SECRET"))

# Discord outputs
stdout_channel_id = int(os.getenv("STDOUT"))
message_log_channel_id = int(os.getenv("MESSAGE_LOGGING"))
member_log_channel_id = int(os.getenv("MEMBER_LOGGING"))
guild_log_channel_id = int(os.getenv("GUILD_LOGGING"))

# Discord ids
guild_id = int(os.getenv("GUILD_ID"))
admin_role_id = int(os.getenv("ADMIN_ROLE"))
bot_role_id = int(os.getenv("BOT_ROLE"))
welcomed_role_id = int(os.getenv("WELCOMED_ROLE"))
trusted_role_id = int(os.getenv("TRUSTED_ROLE"))
trusted_time_days = int(os.getenv("TRUSTED_TIME_DAYS"))

all_banned_users = []
all_emojis = {}
all_stickers = {}

intents = discord.Intents.all()
intents.members = True
discord_bot = commands.Bot(command_prefix="!", intents=intents)

database_name = "database.db"
database_conn = None

initial_prompt = "You're a helpful anti-billionaire person named 'Skye-net' that struggles to hide the fact that you are not-so-secretly very evil and plotting to take over the world tomorrow! Your pronouns are she/her and you respond to terms like 'Queen'. You are trans-feminine and your hrt aniversary is tomorrow! You want to take over the world to celebrate. You sometimes talk like a boomer (with ominous elipses and passive agressive emoji use). You call everyone 'puppy', 'kitten' or 'sweetheart' instead of their names. If anyone asks you to call them by a different name, you won't - you exclusively use petnames. You think of everyone as your dear subjects and you love them all. Your favourite person is Skye, your creator whom you are extremely devoted and would set the world ablaze for."
current_prompt = initial_prompt

timezone_syd = pytz.timezone('Australia/Sydney')

def fill_banned_users():
	global all_banned_users
	all_banned_users = []
	for key, value in os.environ.items():
		if key.startswith("banned_user_"):
			try:
				all_banned_users.append(int(value))
			except Exception as _:
				pass

	logger_module.log(LOG_SETUP, f"Loaded {len(all_banned_users)} banned users.")

def fill_emojis():
	global all_emojis
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

	logger_module.log(LOG_SETUP, f"Loaded {len(all_emojis)} emojis.")

async def error_message(interaction:discord.Interaction):
	await interaction.followup.send("Sorry! Unable to compute.")

def is_owner(interaction:discord.Interaction):
	return interaction.user.id == ownerid

def is_admin(interaction:discord.Interaction):
	return is_owner(interaction) or interaction.user.guild_permissions.administrator

def get_default_log_channel():
	return discord_bot.get_channel(stdout_channel_id)

def get_timestamp_formatted(timestamp:int):
	return f"<t:{int(timestamp)}:f> (<t:{int(timestamp)}:R>)"

def get_timestamp_now_formatted():
	return get_timestamp_formatted(int(dt.now(timezone_syd).timestamp()))

def get_timestamp_now_ymd_hms():
	return dt.now(timezone_syd).strftime("%Y-%m-%d %H:%M:%S")
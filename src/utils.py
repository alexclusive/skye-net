import discord
import os
import pytz

from datetime import datetime as dt
from discord.ext import commands
from dotenv import load_dotenv

all_emojis = {}

intents = discord.Intents.all()
discord_bot = commands.Bot(command_prefix="!", intents=intents)
load_dotenv(dotenv_path="/volume1/documents/git/skye-net/.env")
received_shutdown = False
database_conn = None
current_prompt = ""

# Verification
token = str(os.getenv("TOKEN"))
client_id = str(os.getenv("CLIENT_ID"))
owner_id = int(os.getenv("OWNER"))

# File locations
base_path = str(os.getenv("BASE_PATH"))
log_file_path = base_path + "/" + str(os.getenv("LOG_FILE_PATH"))
database_name = base_path + "/" + str(os.getenv("DATABASE_FILE_NAME"))

# Open AI
history_limit = int(os.getenv("HISTORY_LIMIT"))
openai_key = str(os.getenv("OPENAI_API_KEY"))

# Spotify
spotify_client_id = str(os.getenv("SPOTIFY_CLIENT_ID"))
spotify_client_secret = str(os.getenv("SPOTIFY_CLIENT_SECRET"))

# Main Discord Output
stdout_channel_id = int(os.getenv("STDOUT"))

# Timezone
timezone_here = pytz.timezone(str(os.getenv("TIMEZONE")))

# Discord ids
guild_id = int(os.getenv("GUILD_ID"))
admin_role_id = int(os.getenv("ADMIN_ROLE"))
bot_role_id = int(os.getenv("BOT_ROLE"))
welcomed_role_id = int(os.getenv("WELCOMED_ROLE"))
trusted_role_id = int(os.getenv("TRUSTED_ROLE"))
trusted_time_days = int(os.getenv("TRUSTED_TIME_DAYS"))

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(current_dir, "database", "train_info.csv")

def get_default_log_channel():
	return discord_bot.get_channel(stdout_channel_id)

def set_current_prompt(new_prompt:str):
	global current_prompt
	current_prompt = new_prompt

def get_timestamp_formatted(timestamp:int):
	return f"<t:{int(timestamp)}:f> (<t:{int(timestamp)}:R>)"

def get_timestamp_now_formatted():
	return get_timestamp_formatted(int(dt.now(timezone_here).timestamp()))

def get_timestamp_now_ymd_hms():
	return dt.now(timezone_here).strftime("%Y-%m-%d %H:%M:%S")

def format_time_difference(seconds: int):
	minutes, sec = divmod(seconds, 60)
	hours, minutes = divmod(minutes, 60)
	days, hours = divmod(hours, 24)

	parts = []
	if days > 0:
		parts.append(f"{days}d")
	if hours > 0:
		parts.append(f"{hours}h")
	if minutes > 0:
		parts.append(f"{minutes}m")
	if sec > 0 or not parts:
		parts.append(f"{sec}s")

	return ' '.join(parts)

def fill_emojis():
	global all_emojis
	all_emojis["NOT_FAR"] = int(os.getenv('NOT_FAR'))
	all_emojis["AUTISM_CREATURE"] = int(os.getenv('AUTISM_CREATURE'))
	
	all_emojis["POINT"] = int(os.getenv('POINT'))
	all_emojis["NUH_UH"] = int(os.getenv('NUH_UH'))
	all_emojis["WAGGING_FINGER"] = int(os.getenv('WAGGING_FINGER'))
	all_emojis["LESBIAN_BRICK"] = int(os.getenv('LESBIAN_BRICK'))
	all_emojis["CHOMP"] = int(os.getenv('CHOMP'))
	all_emojis["HEADPAT"] = int(os.getenv('HEADPAT'))

def is_user_in_guild(interaction:discord.Interaction):
	if interaction.guild_id is None\
		or interaction.user is None:
		return False
	
	guild = discord_bot.get_guild(interaction.guild_id)
	if guild is None:
		return False
	
	user = guild.get_member(interaction.user.id)
	if user is None:
		return False
	
	return True
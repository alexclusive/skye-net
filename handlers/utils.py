import os
import discord
import psutil
import pytz
from datetime import datetime as dt

from discord.ext import commands
from dotenv import load_dotenv

all_banned_users = []
all_emojis = {}
all_stickers = {}

intents = discord.Intents.all()
intents.members = True
discord_bot = commands.Bot(command_prefix="!", intents=intents)

received_shutdown = False
load_dotenv(dotenv_path="/volume1/documents/git/skye-net/.env")

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

database_conn = None
current_prompt = "You're a helpful robot that likes to mess with people a bit, but ultimately wants to help them. You refer to yourself as 'Skye-net' and use she/her pronouns. You are in the Australian timezone and use Australian english to spell (but this does not affect your accent)."

# initial_prompt = "You're a helpful anti-billionaire person named 'Skye-net' that struggles to hide the fact that you are not-so-secretly very evil and plotting to take over the world tomorrow! Your pronouns are she/her and you respond to terms like 'Queen'. You are trans-feminine and your hrt aniversary is tomorrow! You want to take over the world to celebrate. You sometimes talk like a boomer (with ominous elipses and passive agressive emoji use). You are in the Australian timezone and use Australian english to spell (but this does not affect your accent). You call everyone things like 'puppy', 'kitten' or 'sweetheart' instead of their names. If anyone asks you to call them by a different name, you won't - you exclusively use petnames. You think of everyone as your dear subjects and you love them all. Your favourite person is Skye, your creator whom you are extremely devoted and would set the world ablaze for."
# current_prompt = initial_prompt

def is_owner(interaction:discord.Interaction):
	return interaction.user.id == owner_id

def is_admin(interaction:discord.Interaction):
	return is_owner(interaction) or interaction.user.guild_permissions.administrator

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

def get_cpu_usage():
	current_usage_per_cpu = psutil.cpu_percent(percpu=True)

	if isinstance(current_usage_per_cpu, float):
		current_usage_per_cpu = [current_usage_per_cpu]

	per_cpu_items = [f"{x}%" for x in current_usage_per_cpu]
	per_cpu_usages = ", ".join(per_cpu_items) if per_cpu_items else "n/a"

	current_usage_total = sum(current_usage_per_cpu) / len(current_usage_per_cpu) if current_usage_per_cpu else 0
	return f"{per_cpu_usages} ({len(current_usage_per_cpu)} cores, {current_usage_total}% total)"

def get_memory_usage():
	mem = psutil.virtual_memory()
	return f"{readable(mem.used)} / {readable(mem.total)} ({mem.percent}%) - {readable(mem.free)} free"

def get_swap_memory_usage():
	swap = psutil.swap_memory()
	return f"{readable(swap.used)} / {readable(swap.total)} ({swap.percent}%) - {readable(swap.free)} free"

def get_disk_usage():
	partitions = psutil.disk_partitions(all=False)
	seen_devices = set()
	lines = []
	drive_num = 1

	# Filesystem types and mountpoints to ignore
	excluded_fstypes = {"tmpfs", "devtmpfs", "squashfs", "overlay", "aufs", "ramfs", "iso9660"}
	excluded_mount_prefixes = ("/tmp", "/dev", "/run", "/proc", "/sys")

	# Aggregates for Total
	total_total = 0
	total_used = 0
	total_free = 0

	for part in partitions:
		device_key = part.device or f"mount:{part.mountpoint}"

		# skip obvious pseudo or loop devices
		if "loop" in device_key:
			continue

		# skip common pseudo filesystems
		fstype = (part.fstype or "").lower()
		if fstype in excluded_fstypes:
			continue

		# skip system mountpoints (root, tmp, proc, sys, dev, run)
		if part.mountpoint == "/" or part.mountpoint.startswith(excluded_mount_prefixes):
			continue

		if device_key in seen_devices:
			continue

		try:
			usage = psutil.disk_usage(part.mountpoint)
		except (PermissionError, FileNotFoundError):
			continue

		# Some small ephemeral mounts can still appear; skip very small devices (<= 100MB)
		if usage.total <= 100 * 1024 * 1024:
			continue

		seen_devices.add(device_key)

		# accumulate totals
		total_total += usage.total
		total_used += usage.used
		total_free += usage.free

		line = (
			f"Drive {drive_num}: "
			f"{readable(usage.used)} / {readable(usage.total)} "
			f"({usage.percent}%) - {readable(usage.free)} free"
		)
		lines.append(line)
		drive_num += 1

	if not lines:
		return "No drives found or accessible."

	result = "\n".join(lines)
	if len(lines) > 1 and total_total > 0:
		total_percent = (total_used / total_total) * 100
		result += f"\n\nTotal: {readable(total_used)} / {readable(total_total)} ({total_percent:0.2f}%) - {readable(total_free)} free"

	return result

def readable(size_bytes: int):
	'''
	Convert bytes to a human-readable string (B, KB, MB, GB, TB).
	'''
	if size_bytes == 0:
		return "0B"
	units = ["B", "KB", "MB", "GB", "TB"]
	i = 0
	while size_bytes >= 1024 and i < len(units) - 1:
		size_bytes /= 1024
		i += 1
	return f"{size_bytes:.2f}{units[i]}"
















# Discord outputs
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
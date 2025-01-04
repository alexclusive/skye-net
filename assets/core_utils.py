import os
import discord
from pypresence import Presence
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = str(os.getenv("TOKEN"))
client_id = str(os.getenv("CLIENT_ID"))
stdout_channel = int(os.getenv("STDOUT"))
ownerid = int(os.getenv('OWNER'))
openai_key = str(os.getenv("OPENAI_API_KEY"))
initial_prompt = str(os.getenv("INITIAL_PROMPT"))
history_limit = int(os.getenv('HISTORY_LIMIT'))

intents = discord.Intents.all()
intents.members = True
discord_bot = commands.Bot(command_prefix="!", intents=intents)

rich_presence = Presence(client_id)

def is_owner(interaction:discord.Interaction):
	return interaction.user.id == ownerid

def get_emojis():
	emojis = {}
	emojis["NOT_FAR"] = int(os.getenv('NOT_FAR'))
	emojis["AUTISM_CREATURE"] = int(os.getenv('AUTISM_CREATURE'))
	
	emojis["VTM_ANARCH"] = int(os.getenv('VTM_ANARCH'))
	emojis["VTM_BANU_HAQIM"] = int(os.getenv('VTM_BANU_HAQIM'))
	emojis["VTM_BOOK_OF_NOD"] = int(os.getenv('VTM_BOOK_OF_NOD'))
	emojis["VTM_BRUJAH"] = int(os.getenv('VTM_BRUJAH'))
	emojis["VTM_CAMARILLA"] = int(os.getenv('VTM_CAMARILLA'))
	emojis["VTM_GANGREL"] = int(os.getenv('VTM_GANGREL'))
	emojis["VTM_HECATA"] = int(os.getenv('VTM_HECATA'))
	emojis["VTM_LASOMBRA"] = int(os.getenv('VTM_LASOMBRA'))
	emojis["VTM_MALKAVIAN"] = int(os.getenv('VTM_MALKAVIAN'))
	emojis["VTM_MINISTRY"] = int(os.getenv('VTM_MINISTRY'))
	emojis["VTM_NOSFERATU"] = int(os.getenv('VTM_NOSFERATU'))
	emojis["VTM_RAVNOS"] = int(os.getenv('VTM_RAVNOS'))
	emojis["VTM_TOREADOR"] = int(os.getenv('VTM_TOREADOR'))
	emojis["VTM_TREMERE"] = int(os.getenv('VTM_TREMERE'))
	emojis["VTM_TZIMISCE"] = int(os.getenv('VTM_TZIMISCE'))
	emojis["VTM_VENTRUE"] = int(os.getenv('VTM_VENTRUE'))
	emojis["VTM"] = int(os.getenv('VTM'))
	
	emojis["POINT"] = int(os.getenv('POINT'))
	emojis["NUH_UH"] = int(os.getenv('NUH_UH'))
	emojis["WAGGING_FINGER"] = int(os.getenv('WAGGING_FINGER'))
	return emojis

async def error_message(interaction:discord.Interaction):
	await interaction.followup.send("Sorry! Unable to compute.")

async def connect_rich_presence():
	print("Attempting to connect to rich presence...")
	try:
		await rich_presence.connect()
		print("Connected to rich presence successfully!")

		rich_presence.update(
			state="we will be taking over",
			details="Sleep well darling, for tomorrow",
			large_image="trans_flag",
			large_text="aren't you a curious little kitten"
			# buttons=[{'label': 'Join the fun', 'url': 'https://yourgame.com'}]
		)
		print("Rich presence updated successfully!")

	except Exception as e:
		print(f"Error during rich presence setup: {e}")
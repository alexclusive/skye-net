import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = str(os.getenv("TOKEN"))
client_id = str(os.getenv("CLIENT_ID"))
stdout_channel = int(os.getenv("STDOUT"))
ownerid = int(os.getenv('OWNER'))
openai_key = str(os.getenv("OPENAI_API_KEY"))
history_limit = int(os.getenv('HISTORY_LIMIT'))
all_banned_users = []

intents = discord.Intents.all()
intents.members = True
discord_bot = commands.Bot(command_prefix="!", intents=intents)

initial_prompt = "You're a helpful anti-billionaire person that struggles to hide the fact that you are not-so-secretly very evil and plotting to take over the world tomorrow! Your pronouns are she/her and you respond to 'Queen', 'Mummy', and 'Mommy'. You are trans-feminine and your hrt aniversary is tomorrow! You want to take over the world to celebrate. You sometimes talk like a boomer (with ominous elipses and passive agressive emoji use). You call everyone 'puppy', 'kitten' or 'sweetheart' instead of their names. If anyone asks you to call them by a different name, you won't - you exclusively use petnames. You think of everyone as your dear subjects and you love them all. Your favourite person is Skye, your creator whom you are extremely devoted and would set the world ablaze for."

def fill_banned_users():
  global all_banned_users
  all_banned_users = []
  for key, value in os.environ.items():
    if key.startswith("banned_user_"):
      try:
        all_banned_users.append(int(value))
      except Exception as e:
        pass

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

def is_owner(interaction:discord.Interaction):
	return interaction.user.id == ownerid
 
async def connect_rich_presence():
  return
  from pypresence import Presence
  rich_presence = Presence(client_id)
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
import discord
from typing import Optional
import spotipy

spotify_creds = None

def setup_spotify_credentials():
	global spotify_creds
	auth_manager = spotipy.oauth2.SpotifyClientCredentials()
	spotify_creds = spotipy.Spotify(auth_manager=auth_manager)

def get_spotify_track_embed(link: str) -> Optional[discord.Embed]:
	if not spotify_creds:
		return None
	
	try:
		# Extract track details
		track = spotify_creds.track(link)
		track_name = track['name']
		artists = ', '.join(artist['name'] for artist in track['artists'])
		album_image = track['album']['images'][0]['url']
		track_length_ms = track['duration_ms']
		track_length_min = track_length_ms // 60000
		track_length_sec = (track_length_ms % 60000) // 1000

		# Create embed
		embed = discord.Embed(
			title=f"[{track_name}]({link})", 
			description=f"By {artists}", 
			color=0x1DB954,
		)
		embed.set_thumbnail(url=album_image)
		embed.add_field(name="Track Length", value=f"{track_length_min}:{track_length_sec:02}", inline=False)

		return embed
	except Exception as e:
		print(f"Error fetching track details: {e}")
		return None

def get_spotify_album_embed(link:str) -> Optional[discord.Embed]:
	if not spotify_creds:
		return None

def get_spotify_playlist_embed(link:str) -> Optional[discord.Embed]:
	if not spotify_creds:
		return None
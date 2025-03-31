import discord
from typing import Optional
import spotipy

import handlers.utils as utils_module

spotify_creds = None

def setup_spotify_credentials():
	global spotify_creds
	auth_manager = spotipy.oauth2.SpotifyClientCredentials(
		client_id = utils_module.spotify_client_id,
		client_secret = utils_module.spotify_client_secret
	)
	spotify_creds = spotipy.Spotify(auth_manager=auth_manager)

def get_track(link:str):
	try:
		if not spotify_creds:
			return None
		return spotify_creds.track(link)
	except Exception as e:
		print(f"Error fetching track details: {e}")
		return None
	
def get_album(link:str):
	try:
		if not spotify_creds:
			return None
		return spotify_creds.album(link)
	except Exception as e:
		print(f"Error fetching album details: {e}")
		return None
	
def get_playlist(link:str):
	try:
		if not spotify_creds:
			return None
		return spotify_creds.playlist(link)
	except Exception as e:
		print(f"Error fetching playlist details: {e}")
		return None
	
def get_title(item):
	return item['name']

def get_artists(item):
	return ', '.join(artist['name'] for artist in item['artists'])

def get_track_length(track):
	track_length_ms = track['duration_ms']
	track_length_min = track_length_ms // 60000
	track_length_sec = (track_length_ms % 60000) // 1000
	return f"{track_length_min}:{track_length_sec:02}"

def get_playlist_cover(playlist):
	return playlist['images'][0]['url'] if 'images' in playlist and playlist['images'] else None

def get_album_cover(album):
	return album['images'][0]['url']

def get_track_album_cover(track):
	return get_album_cover(track['album'])

def get_all_tracks(item):
	return item['tracks']['items']

def get_all_album_track_details(album):
	tracks = get_all_tracks(album)
	details = []
	for track in tracks:
		title = get_title(track)
		artists = get_artists(track)
		track_detail = (title, artists)
		details.append(track_detail)
	return details

def get_all_playlist_track_details(playlist):
	tracks = get_all_tracks(playlist)
	details = []
	for track in tracks:
		# title = f"[{get_title(track['track'])}]({track['track']['external_urls']['spotify']})"
		title = f"{get_title(track['track'])}"
		artists = get_artists(track['track'])
		track_detail = (title, artists)
		details.append(track_detail)
	return details

def get_spotify_track_embed(link: str) -> Optional[discord.Embed]:
	track = get_track(link)
	if not track:
		return None

	embed = discord.Embed(
		title = get_title(track),
		url = link,
		description = get_artists(track),
		color = 0x1DB954
	)
	embed.set_thumbnail(url=get_track_album_cover(track))
	embed.set_footer(text=get_track_length(track))
	return embed

def get_spotify_album_embed(link:str) -> Optional[discord.Embed]:
	album = get_album(link)
	if not album:
		return None
	
	embed = discord.Embed(
		title = get_title(album),
		url = link,
		color = 0x1DB954
	)
	details = get_all_album_track_details(album)
	for track in details[:10]:
		embed.add_field(
			name=track[0],
			value=track[1],
			inline=False
		)
	embed.set_footer(text=(str(album['total_tracks']) + " tracks"))
	
	embed.set_thumbnail(url=get_album_cover(album))
	return embed

def get_spotify_playlist_embed(link:str) -> Optional[discord.Embed]:
	playlist = get_playlist(link)
	if not playlist:
		return None

	embed = discord.Embed(
		title = get_title(playlist),
		url = link,
		color = 0x1DB954
	)
	details = get_all_playlist_track_details(playlist)
	for track in details[:10]:
		embed.add_field(
			name=track[0],
			value=track[1],
			inline=False
		)
	embed.set_footer(text=(str(playlist['tracks']['total']) + " tracks"))

	cover = get_playlist_cover(playlist)
	if cover:
		embed.set_thumbnail(url=cover)

	return embed
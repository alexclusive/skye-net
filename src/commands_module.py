import discord

from . import utils

command_called_log_string = "Command called"
something_went_wrong = "Something went wrong :("
must_be_guild_member = "You must be a server member to use this command."
nice_try = "Guess you're not cool enough for this one :)"

owner_commands_names = []
owner_commands = []

def is_owner(interaction:discord.Interaction) -> bool:
	return interaction.user.id == utils.owner_id

def is_admin(interaction:discord.Interaction) -> bool:
	return is_owner(interaction) or interaction.user.guild_permissions.administrator

def owner_only():
	def predicate(interaction:discord.Interaction) -> bool:
		return is_owner(interaction)
	return discord.app_commands.check(predicate)

def admin_only():
	def predicate(interaction:discord.Interaction) -> bool:
		return is_admin(interaction)
	return discord.app_commands.check(predicate)

async def ensure_correct_permissions():
	for guild in utils.discord_bot.guilds:
		for cmd in await utils.discord_bot.tree.fetch_commands(guild=guild):
			if cmd.name in owner_commands_names:
				perm = discord.app_commands.PermissionOverwrite(
					id=utils.owner_id,
					type=discord.app_commands.PermissionType.user,
					permission=True
				)
				await cmd.edit_permissions(guild=guild, permissions=[perm])

	for cmd in owner_commands:
		cmd.dm_permission = False
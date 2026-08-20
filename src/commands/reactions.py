import discord

from .. import commands_module as commands
from .. import database_module as database
from .. import logger
from .. import utils

'''
 - opt_out
 - opt_in
 - opt_out_user [Admin]
 - opt_in_user [Admin]
 - get_opt_out_users [Owner]
'''

@utils.discord_bot.tree.command(description="Opt out of the bot's reactions")
async def opt_out(interaction:discord.Interaction):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)

	try:
		database.opt_out(interaction.user.id)
		await interaction.followup.send("You have opted out of reactions")
	except Exception as e:
		print(f"Error getting opt out reactions: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@utils.discord_bot.tree.command(description="Opt in to the bot's reactions")
async def opt_in(interaction:discord.Interaction):
	await interaction.response.defer()
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)

	try:
		database.opt_in(interaction.user.id)
		await interaction.followup.send("You have opted in to reactions")
	except Exception as e:
		print(f"Error getting opt in reactions: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@discord.app_commands.describe(
	user_id="User ID to opt out from bot reactions"
)
@utils.discord_bot.tree.command(description="[Admin] Opt a user out of reactions")
@discord.app_commands.default_permissions(administrator=True)
@commands.admin_only()
async def opt_out_user(interaction:discord.Interaction, user_id:int):
	await interaction.response.defer(ephemeral=True)
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_admin(interaction):
		await interaction.followup.send(commands.nice_try)
		return

	try:
		database.opt_out(user_id)
		await interaction.followup.send(f"{user_id} opted out of reactions")
	except Exception as e:
		print(f"Error forcing opt out of reactions: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@discord.app_commands.describe(
	user_id="User ID to opt in to bot reactions"
)
@utils.discord_bot.tree.command(description="[Admin] Opt a user in to reactions")
@discord.app_commands.default_permissions(administrator=True)
@commands.admin_only()
async def opt_in_user(interaction:discord.Interaction, user_id:int):
	await interaction.response.defer(ephemeral=True)
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_admin(interaction):
		await interaction.followup.send(commands.nice_try)
		return

	try:
		database.opt_in(user_id)
		await interaction.followup.send(f"{user_id} opted in to reactions")
	except Exception as e:
		print(f"Error forcing opt in of reactions: {e}")
		await interaction.followup.send(commands.something_went_wrong)

@utils.discord_bot.tree.command(description="[Owner] Get list of user IDs that have opted out of reactions")
@discord.app_commands.default_permissions() # No perms, set up in on_ready
@commands.owner_only()
async def get_opt_out_users(interaction:discord.Interaction):
	await interaction.response.defer(ephemeral=True)
	logger.log(logger.LOG_DETAIL, commands.command_called_log_string)
	if not commands.is_owner(interaction):
		await interaction.followup.send(commands.nice_try)
		return

	try:
		opted_out_user_ids = database.get_all_opt_out_users()
		opted_out_user_objs:list[discord.User] = []
		for user_id in opted_out_user_ids:
			try:
				user = await utils.discord_bot.fetch_user(user_id)
				if user:
					opted_out_user_objs.append(user)
			except Exception:
				continue
		await interaction.followup.send(f"Opted out users: {', '.join(user.name for user in opted_out_user_objs)}")
	except Exception as e:
		print(f"Error getting opt-out users: {e}")
		await interaction.followup.send(commands.something_went_wrong)
		
commands.owner_commands_names.append("get_opt_out_users")
commands.owner_commands.append(get_opt_out_users)
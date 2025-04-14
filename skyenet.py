import sys
import asyncio
import discord

import handlers.utils as utils_module
import handlers.commands as commands_module
import handlers.database as database_module
import handlers.events as events_module
import handlers.tasks as tasks_module

import handlers.helpers.spotify as spotify_module

'''
	Commands
	[Owner] is for just the bot owner
	[Admin] is for anyone with administrator permissions
'''
def owner_only():
	async def predicate(interaction:discord.Interaction) -> bool:
		return utils_module.is_owner(interaction)
	return discord.app_commands.check(predicate)

def admin_only():
	async def predicate(interaction:discord.Interaction) -> bool:
		return utils_module.is_admin(interaction)
	return discord.app_commands.check(predicate)

@utils_module.discord_bot.tree.command(description="[Owner] Shutdown the bot")
@owner_only()
async def kill(interaction:discord.Interaction):
	await interaction.response.defer()
	await commands_module.die(interaction)

@utils_module.discord_bot.tree.command(description="[Owner] Get list of user IDs that have opted out of reactions")
@owner_only()
async def get_opt_out_users(interaction:discord.Interaction):
	await interaction.response.defer(ephemeral=True)
	await commands_module.get_opt_out_users(interaction)

@utils_module.discord_bot.tree.command(description="[Owner] Force trusted roles task")
@owner_only()
async def force_trusted_roles(interaction:discord.Interaction):
	await interaction.response.defer(ephemeral=True)
	await commands_module.force_trusted_roles(interaction)

@utils_module.discord_bot.tree.command(description="[Owner] Force audit log check")
@owner_only()
async def force_audit_log(interaction:discord.Interaction):
	await interaction.response.defer(ephemeral=True)
	await commands_module.force_audit_log(interaction)

@utils_module.discord_bot.tree.command(description="[Admin] Enter train fact")
@admin_only()
async def enter_train_fact(interaction:discord.Interaction, fact:str):
	await interaction.response.defer()
	await commands_module.enter_train_fact(interaction, fact)

@utils_module.discord_bot.tree.command(description="[Admin] Remove train fact")
@admin_only()
async def remove_train_fact(interaction:discord.Interaction, fact_num:int):
	await interaction.response.defer()
	await commands_module.remove_train_fact(interaction, fact_num)

@utils_module.discord_bot.tree.command(description="[Admin] Get the list of train facts - may overflow")
@admin_only()
async def get_train_facts(interaction:discord.Interaction):
	await interaction.response.defer()
	await commands_module.get_train_facts(interaction)

@utils_module.discord_bot.tree.command(description="[Admin] Get the list of reactions")
@admin_only()
async def get_reactions(interaction:discord.Interaction):
	await interaction.response.defer()
	await commands_module.get_reactions(interaction)

@utils_module.discord_bot.tree.command(description="[Admin] Insert a reaction trigger")
@admin_only()
async def insert_reaction(interaction:discord.Interaction, trigger:str, emoji_1:str, emoji_2:str="", emoji_3:str=""):
	await interaction.response.defer()
	await commands_module.insert_reaction(interaction, trigger, emoji_1, emoji_2, emoji_3)

@utils_module.discord_bot.tree.command(description="[Admin] Remove a reaction trigger")
@admin_only()
async def remove_reaction(interaction:discord.Interaction, trigger:str):
	await interaction.response.defer()
	await commands_module.remove_reaction(interaction, trigger)

@utils_module.discord_bot.tree.command(description="[Admin] Get logging channels")
@admin_only()
async def get_logging_channels(interaction:discord.Interaction):
	await interaction.response.defer()
	await commands_module.get_log_channels(interaction)

@utils_module.discord_bot.tree.command(description="[Admin] Set logging channel")
@admin_only()
async def set_logging_channel(interaction:discord.Interaction, message_channel:discord.TextChannel=None, member_channel:discord.TextChannel=None, role_channel:discord.TextChannel=None):
	await interaction.response.defer()
	await commands_module.set_log_channels(interaction, message_channel, member_channel, role_channel)

@utils_module.discord_bot.tree.command(description="[Admin] Get banned users")
@admin_only()
async def get_banned_users(interaction:discord.Interaction):
	await interaction.response.defer()
	await commands_module.get_banned_users(interaction)

@utils_module.discord_bot.tree.command(description="[Admin] Ban a user from openai interactions")
@admin_only()
async def ban_user(interaction:discord.Interaction, user:discord.User):
	await interaction.response.defer()
	await commands_module.ban_user(interaction, user)

@utils_module.discord_bot.tree.command(description="[Admin] Unban a user from openai interactions")
@admin_only()
async def unban_user(interaction:discord.Interaction, user:discord.User):
	await interaction.response.defer()
	await commands_module.unban_user(interaction, user)

@utils_module.discord_bot.tree.command(description="[Admin] Get important roles")
@admin_only()
async def get_roles(interaction:discord.Interaction):
	await interaction.response.defer()
	await commands_module.get_important_roles(interaction)

@utils_module.discord_bot.tree.command(description="[Admin] Set important roles")
@admin_only()
async def set_roles(interaction:discord.Interaction, welcomed:discord.Role=None, trusted:discord.Role=None, trusted_time_days:int=14):
	await interaction.response.defer()
	await commands_module.set_important_roles(interaction, welcomed, trusted, trusted_time_days)

@utils_module.discord_bot.tree.command(description="[Admin] Get to do list")
@admin_only()
async def get_todo(interaction:discord.Interaction):
	await interaction.response.defer()
	await commands_module.get_todo(interaction)

@utils_module.discord_bot.tree.command(description="[Admin] Add to do item")
@admin_only()
async def add_todo(interaction:discord.Interaction, item:str):
	await interaction.response.defer()
	await commands_module.add_todo(interaction, item)

@utils_module.discord_bot.tree.command(description="[Admin] Remove to do item")
@admin_only()
async def remove_todo(interaction:discord.Interaction, item_num:int):
	await interaction.response.defer()
	await commands_module.remove_todo(interaction, item_num)

@utils_module.discord_bot.tree.command(description="Check the bot's ping")
async def ping(interaction:discord.Interaction):
	await interaction.response.defer()
	await commands_module.ping(interaction)

@utils_module.discord_bot.tree.command(description="Train game - get to [target] using (+-*/) and optionally (^%)")
async def train_game(
	interaction:discord.Interaction,
	number:int,  # The starting number for the game - four digits
	target:int = 10,  # The target number to reach - default 10
	use_power:str = "True",  # Allow usage of the power (^) operation - default True
	use_modulo:str = "True",  # Allow usage of the modulo (%) operation - default True
):
	use_power_bool = "true" in use_power.lower()
	use_modulo_bool = "true" in use_modulo.lower()
	await interaction.response.defer()
	await commands_module.train_game(interaction, number, target, use_power_bool, use_modulo_bool)

@utils_module.discord_bot.tree.command(description="Train game - explanation of rules")
async def train_game_rules(interaction:discord.Interaction):
	await interaction.response.defer()
	await commands_module.train_game_rules(interaction)

@utils_module.discord_bot.tree.command(description="Train fun-fact")
async def train_fact(interaction:discord.Interaction):
	await interaction.response.defer()
	await commands_module.train_fact(interaction)

@utils_module.discord_bot.tree.command(description="Reset the bot's prompt")
async def reset_prompt(interaction:discord.Interaction):
	await interaction.response.defer()
	await commands_module.reset_prompt(interaction)

@utils_module.discord_bot.tree.command(description="Set the bot's prompt")
async def set_prompt(interaction:discord.Interaction, prompt:str):
	await interaction.response.defer()
	await commands_module.set_prompt(interaction, prompt)

@utils_module.discord_bot.tree.command(description="Get the etymology of a word")
async def etymology(interaction:discord.Interaction, argument:str):
	await interaction.response.defer()
	await commands_module.etymology(interaction, argument)

@utils_module.discord_bot.tree.command(description="Opt out of the bot's reactions")
async def opt_out(interaction:discord.Interaction):
	await interaction.response.defer()
	await commands_module.opt_out_reactions(interaction)

@utils_module.discord_bot.tree.command(description="Opt in to the bot's reactions")
async def opt_in(interaction:discord.Interaction):
	await interaction.response.defer()
	await commands_module.opt_in_reactions(interaction)

'''
	Events
'''
@utils_module.discord_bot.event
async def on_ready():
	await utils_module.discord_bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.CustomActivity("Skye-net is watching...", type=discord.ActivityType.watching))
	await utils_module.discord_bot.tree.sync()
	print(f"{utils_module.discord_bot.user} is ready and online :P")
	await tasks_module.tasks_on_ready()

@utils_module.discord_bot.event
async def on_message(message):
	await events_module.message(message)

@utils_module.discord_bot.event
async def on_message_delete(message):
	await events_module.message_deleted(message)

@utils_module.discord_bot.event
async def on_guild_channel_create(channel:discord.abc.GuildChannel):
	await events_module.channel_create(channel)

@utils_module.discord_bot.event
async def on_guild_channel_delete(channel:discord.abc.GuildChannel):
	await events_module.channel_delete(channel)

@utils_module.discord_bot.event
async def on_guild_role_create(role:discord.Role):
	await events_module.role_create(role)

@utils_module.discord_bot.event
async def on_guild_role_delete(role:discord.Role):
	await events_module.role_delete(role)

@utils_module.discord_bot.event
async def on_member_join(member:discord.Member):
	await events_module.member_join(member)

@utils_module.discord_bot.event
async def on_member_remove(member:discord.Member):
	await events_module.member_remove(member)

@utils_module.discord_bot.event
async def on_member_update(before:discord.Member, after:discord.Member):
	# nickname / roles / guild avatar
	await events_module.member_update(before, after)

@utils_module.discord_bot.event
async def on_member_ban(member:discord.Member):
	await events_module.member_ban(member)

'''
	Discord handling
'''
def send_message(channel:discord.abc.Messageable, message:str) -> None:
	if len(message) > 2000:  # discord won't allow longer than 2000 characters, so split it up
		for i in range(0, len(message), 2000):
			chunk = message[i:i+2000]
			asyncio.ensure_future(channel.send(chunk))
	else:
		asyncio.ensure_future(channel.send(message))

def send_output_to_discord(message:str):
	message = message.strip()
	if message:
		channel = utils_module.discord_bot.get_channel(utils_module.stdout_channel_id)
		if channel:
			try: # catch error code 32: broken pipe
				send_message(channel, message)
			except discord.HTTPException as e:
				if e.code == 32:
					asyncio.sleep(0.5) # wait for a bit and try again
					send_message(channel, message)

async def run_bot():
	sys.stdout.write = send_output_to_discord
	sys.stderr.write = send_output_to_discord

	utils_module.fill_banned_users()
	utils_module.fill_emojis()
	database_module.init_db()
	utils_module.current_prompt = database_module.get_most_recent_prompt()
	spotify_module.setup_spotify_credentials()

	try:
		await utils_module.discord_bot.start(utils_module.token)
	except KeyboardInterrupt:
		pass

asyncio.run(run_bot())
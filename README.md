# skye-net

## dotenv
| Field | Description |
|-------|-------------|
| TOKEN | Discord app token from discord developer portal |
| CLIENT_ID | Discord app client-id from discord developer portal |
| OWNER | Owner's discord id |
| LOG_FILE_PATH | Relative filepath to log to |
| HISTORY_LIMIT | How many messages for openai to use for context |
| OPENAI_API_KEY | Key to connect to openai api |
| SPOTIFY_CLIENT_ID | Spotify client ID |
| SPOTIFY_CLIENT_SECRET | Spotify client secret |
| STDOUT | Discord channel id to print stdout and stderr to |
| MESSAGE_LOGGING | Discord channel id for logging message events |
| MEMBER_LOGGING | Discord channel id for logging member events |
| GUILD_LOGGING | Discord channel id for logging guild (server) events |
| GUILD_ID | Discord guild (server) id |
| WELCOMED_ROLE | Role id for the 'welcomed' role |
| TRUSTED_ROLE | Role id for the 'trusted' role |
| TRUSTED_TIME_DAYS | Number of days a user must be in the server before being given the 'trusted' role (only if they have the 'welcomed' role) |
| BANNED_USER_x | User id of user that is banned from using openai interactions (replace x with anything), can have multiple |

### emojis
Put in all emoji ids from discord for what you want to use for reactions and triggers

### banned users
All banned users - disallows each banned user from using openai messaging  
Field in the form of `BANNED_USER_.*`  
e.g. `BANNED_USER_1`

## events
### on_message
- React to the message with different emojis for different trigger words
- If no openai interaction, respond to the message for specific triggers
#### openai interaction
| Context | Description |
|---------|-------------|
| Pings bot<br>not replying | Check the last few messages (default 10) and have openai respond to the message with context |
| Pings bot<br> replying | Check the replied message and have openai respond to the original message |
| Doesn't ping bot | Check triggers to see if there is content to respond with |

### message_deleted
Log deleted message with link to any attachments (expiring link)

### channel_create
Log channel name, type, category, and position

### channel_delete
Log channel name, type, category, and position

### role_create
Log role name and permissions

### role_delete
Log role name and permissions

### member_join
Log member name, joined at date, created at date, and roles

### member_remove
Log member name, joined at date, created at date, roles, and left at date

### member_ban
Log member name, joined at date, created at date, roles, and banned at date

## commands
### [Owner] kill
Shutdown the bot

### [Owner] set_debug_level
Set the debug level for logging

### [Owner] get_opt_out_users
Get a list of all users who have opted out of reactions

### [Owner] force_trusted_roles
Force the trusted roles task

### [Owner] force_audit_log
Force the audit log task

### [Owner] get_all_stickers
Get a list of all stickers that are being used for triggers in each server

### [Owner] get_todo
Get a list of all todo items

### [Owner] add_todo
Add to the todo list

### [Owner] remove_todo
Remove from the todo list

### [Owner] get_all_bingo_templates
Remove all bingo templates

### [Admin] enter_train_fact
Enter a train fact

### [Admin] remove_train_fact
Remove a train fact

### [Admin] get_train_facts
Get all train facts

### [Admin] get_reactions
Get all reactions

### [Admin] insert_reaction
Insert a reaction

### [Admin] remove_reaction
Remove a reaction

### [Admin] get_logging_channels
Get the logging channels

### [Admin] set_logging_channel
Set the logging channels

### [Admin] get_banned_users
Get all banned users

### [Admin] ban_user
Ban a user

### [Admin] unban_user
Unban a user

### [Admin] get_roles
Get important roles

### [Admin] set_roles
Set important roles

### [Admin] get_stickers
Get all stickers for current guild

### [Admin] add_sticker
Add a sticker to be used for the current guild

### [Admin] remove_sticker
Remove a sticker from use in the current guild

### [Admin] opt_out_user
Opt a user out of reactions

### [Admin] opt_in_user
Opt a user in to reactions

### [Admin] get_bingo_templates_for_guild
Get all bingo templates for the current guild

### [Admin] create_bingo_template
Create a new bingo template

### [Admin] delete_bingo_template
Delete a new bingo template

### ping
Check the bots ping

### train_game
Play the train game

### train_game_rules
Show the train game rules

### train_fact
Show a train fact

### reset_prompt
Reset the AI prompt

### set_prompt
Set the AI prompt

### etymology
See the etymology of a word

### opt_out
Opt out of reactions

### opt_in
Opt in to reactions

### create_bingo_card
Create a new bingo card (overwriting any existing)

### get_bingo_card
Get a bingo card

### bingo_check
Check off an item in a bingo card
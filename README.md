# skye-net

## dotenv
| Field | Description |
|-------|-------------|
| TOKEN | Discord app token from discord developer portal |
| CLIENT_ID | Discord app client-id from discord developer portal |
| OWNER | Owner's discord id |
| HISTORY_LIMIT | How many messages for openai to use for context |
| OPENAI_API_KEY | Key to connect to openai api |
| STDOUT | Discord channel id to print stdout and stderr to |
| MESSAGE_LOGGING | Discord channel id for logging message events |
| MEMBER_LOGGING | Discord channel id for logging member events |
| GUILD_LOGGING | Discord channel id for logging guild (server) events |
| BANNED_USER_x | User id of user that is banned from using openai interactions (replace x with anything), can have multiple |
| GUILD_ID | Discord guild (server) id |
| WELCOMED_ROLE | Role id for the 'welcomed' role |
| TRUSTED_ROLE | Role id for the 'trusted' role |
| TRUSTED_TIME_DAYS | Number of days a user must be in the server before being given the 'trusted' role (only if they have the 'welcomed' role) |

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

### [Owner] restart
Restart the bot

### [Admin] delete_message_by_id
Delete a message by the provided message id

### [Admin] get_opt_out_users
Get a list of all users who have opted out of having the bot react to their messages

### [Admin] force_daily_tasks
Run daily tasks even if already run today

### ping
Check the bot's ping

### train_game
Play the train game: get to target (default 10) using 4 numbers, with the operations +-*/ and optionally ^%

### train_game_rules
Show the train game's rules

### train_fact
Not implemented: Show a train fun fact

### reset_prompt
Reset the bot's openai prompt

### set_prompt
Set the bot's openai prompt

### etymology
Get the etymology of a given word

### opt_out
Opt out of having the bot react to your messages

### opt_in
Opt back in to having the bot react to your messages

## planned features
- Make the etymology search through etymonline and show the text - instead of just giving the url
- Add train facts into the train fact database (with command to add / remove)
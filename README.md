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

### emojis
Put in all emoji ids from discord for what you want to use for reactions and triggers

### banned users
All banned users - disallows each banned user from using openai messaging  
Field in the form of `BANNED_USER_.*`  
e.g. `BANNED_USER_1`

## slash-commands
### owner-only
In `assets/cmds/cmd_owner.py`  
#### kill
Shutdown the bot

#### restart
Restart the bot

#### delete message by id
Delete a message by the given message id

### misc
In `assets/cmds/cmd_misc.py`  
#### ping
Check latency

#### train game
Play the train game: get to target (default 10) using 4 numbers, with the operations +-*/ and optionally ^%

#### reset prompt
Reset the openai prompt

#### set prompt
Set the openai prompt

## events
### on message
#### openai
| Context | Description |
|---------|-------------|
| Pings bot<br>not replying | Check the last few messages (default 10) and have openai respond to the message with context |
| Pings bot<br> replying | Check the replied message and have openai respond to the original message |
| Doesn't ping bot | Check triggers to see if there is content to respond with |
| Any message | Check reactions to see if there is content to react to |
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
| BLOCKED_USER_x | User id of user that is blocked from using openai interactions (replace x with anything), can have multiple |

### Emojis
Put in all emoji ids from discord for what you want to use for reactions and triggers (ones that would need nitro)

### Blocked users
All blocked users - disallows each blocked user from using openai messaging  
Field in the form of `BLOCKED_USER_.*`  
e.g. `BLOCKED_USER_1`

## Events
Not all discord events are tracked, and those that are aren't really looked at too hard. The following are what have implementations:
 - on_message
 - on_message_delete
 - on_guild_channel_create
 - on_guild_channel_delete
 - on_guild_role_create
 - on_guild_role_delete
 - on_member_join
 - on_member_remove
 - on_member_update
 - on_member_ban
 - guild_join
 - guild_remove

Most of these just log basic data upon an event, the only one that really has any depth is `on_message`.  

On a message, the bot will check a few things:
 - are there any phrases that trigger a reaction?
 - were there any spotify links that could be cleaned up?

Other than that, if the bot has been pinged it will trigger an open ai interaction.  
| Context | Description |
|---------|-------------|
| Normal ping | Check the last few messages (default 10) and have openai respond to the message with context |
| Pings bot through reply | Check the replied message and have openai respond with the original message as context |

## Commands
Some commands are designated as only for the owner of the bot, or admins. Owner-only `[Owner]` commands can only be run by the bot owner as determined by `OWNER` in the `.env`. Admin-only `[Admin]` can only be run by the owner and anyone with administrator privileges for whatever guild the command is being run in.  

There are a few sets of commands for different groups of tasks:
 - Bot Admin
 - To Do List
 - Open AI
 - Reactions
 - Bingo
 - Train Facts
 - Train Game
 - Number Facts
 - Misc

### Bot Admin
 - die [Owner]
 - set_debug_level [Owner]
 - send_as_bot [Owner]
 - info [Owner]
 - force_trusted_roles [Owner]
 - force_audit_log [Owner]
 - force_reread_train_info [Owner]
 - run_test [Owner]

These are just for the bot owner to do tasks that mainly are just bot maintenance things.  
`die` kill the bot
`set_debug_level` sets the current debug level (more info in Logs section)  
`send_as_bot` allows the owner to send a message in a channel as the bot  
`info` shows info of the machine the bot is running on (e.g. CPU/Mem)  
`force_*` forces a task to run even if the time for the task to run is not now (more info in Tasks section)  
`run_test` placeholder command for testing new commands so that the owner doesn't need to restart discord to be able to run a new command

### To Do List
 - get_todo [Owner]
 - add_todo [Owner]
 - remove_todo [Owner]

A limited todo list for the owner to keep track of tasks they may want to implement into the bot.  
`get_todo` show the current list of todo items  
`add_todo` add a new todo item (will be n+1 where n is the highest current todo item num)  
`remove_todo` remove todo item by item num

### Open AI
 - set_prompt
 - block_user [Admin]
 - unblock_user [Admin]
 - get_blocked_users [Owner]

When the bot is pinged, it responds using open ai interactions. Here users can set a prompt for the personality of the bot. If some users are misusing these interactions, and admin can block them from being able to talk to the bot through this.  
`set_prompt` set a new prompt  
`block_user` restrict a user from openai interactions  
`unblock_user` unrestrict a user from openai interactions  
`get_blocked_users` get a full list of all blocked users

### Reactions
 - opt_out
 - opt_in
 - opt_out_user [Admin]
 - opt_in_user [Admin]
 - get_opt_out_users [Owner]

When a user sends a message, the bot may react with emoji/s based on triggers in the message.  
`opt_out` opt out of the bot reacts  
`opt_in` opt in to the bot reacts  
`opt_out_user` force a particular user to opt out of bot reacts  
`opt_in_user` force a particular user to opt in to bot reacts  
`get_opt_out_users` get a full list of all opted out users

### Bingo
 - create_bingo_card
 - get_bingo_card
 - get_bingo_card_items
 - reset_bingo_card
 - create_bingo_template [Admin]
 - update_bingo_template [Admin]
 - delete_bingo_template [Admin]
 - get_bingo_templates [Admin]
 - get_all_bingo_templates [Owner]

Allows for a 5x5 bingo grid of user-made tiles using discord embed and buttons. A template is a category of bingo card, and a card is a bingo card that uses the tiles from its category.  
`create_bingo_card` create or recreate and display a bingo card for a particular template  
`get_bingo_card` show the user's current bingo card  
`get_bingo_card_items` show the user's current bingo card (items only)  
`reset_bingo_card` clear items for the current bingo card  
`create_bingo_template` create a new bingo template  
`update_bingo_template` update an existing bingo template  
`delete_bingo_template` delete an existing bingo template  
`get_bingo_templates` see bingo templates for the current guild  
`get_all_bingo_templates` see all bingo templates for all guilds

### Train Facts
 - train_fact
 - enter_train_fact [Admin]
 - remove_train_fact [Admin]
 - get_train_facts [Admin]

The bot can hold a database of train facts for if users want to see a random one.  
`train_fact` display a train fact  
`enter_train_fact` add a new train fact  
`remove_train_fact` remove a train fact  
`get_train_facts` get a list of all train facts  

### Train Game
 - train_game_rules
 - train_game

Train number game to get to 10 with a train car's 4 digits.  
`train_game_rules` show the rules of the game  
`train_game` play the game

### Number Facts
 - number_fact
 - update_number_fact [Admin]
 - append_number_fact [Admin]
 - remove_number_fact [Admin]

Show different fun tidbits for different numbers.  
`number_fact` get a number fact  
`update_number_fact` add or update a number fact  
`append_number_fact` append to a number's fact  
`remove_number_fact` remove a number's fact

### Misc
 - ping
 - etymology

`ping` ping the bot  
`etymology` get the etymology of a word or phrase

 ## Tasks

 There are a few tasks the bot runs periodically. 
 | Task | Time | Description |
 |------|------|-------------|
 | Trusted Roles | 19:00 UTC Daily | Specific to GUILD_ID from .env. Add a 'trusted' role to new users as configured through .env variables |
 | Audit Log | 20:00 UTC Daily | Gather and display any new logs from the audit log from admins of the GUILD_ID |
 | Backup Logs | 00:00 UTC Daily | Backup the daily logs into dated directories |
 | Read Train Info | 21:00 UTC Daily | Re-grab the HTML data of NSW trains for train facts in the train game |

 ## Logs
 When events or commands are triggered, a log entry is made. The logs show the datetime, log level, and log detail. Log levels are SETUP (0), INFO (1), DETAIL (2), and EXTRA_DETAIL (3).
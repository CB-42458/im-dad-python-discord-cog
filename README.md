Note: This git repository has yet to be tested, it is possible that is does not work as intended.

## im-dad-python-discord-cog
This is a cog which is made for a python discord bot which runs on one server only. It contains the following commands
which are used as examples so that others can make their own cog. The bot reads the messages from the channels it has
accesses to and if it finds a message which contains the string `im` or `i'm`, it will respond with `Hi {name}, I'm
Dad!`. It supports slash commands to allow users to opt in and out of the bot responding to them. The bot has content
filtering using the `Gasegamer/super-profanity` npm package. Prior to filtering with super-profanity, it will run
through function which replaces homographs with their ascii counterparts.  
This was designed to work with my `python-discord-bot` repository. The cog is intended to be used as a git submodule in
the `cogs_submodules` directory. If you want to use this cog, you can use the following command to add it as a git
submodule:  
```shell
git submodule add https://github.com/CB-42458/im-dad-python-discord-cog cogs_submodules/im-dad
```
### Commands:

- `/imdadoptin` - This command allows users to opt in to the bot responding to them. It will add the user to the opt-in
list and will respond with a message to let the user know that they have opted in. If the user is already opted in, it
will respond with a message to let the user know that they are already opted in.
- `/imdadoptout` - This command allows users to opt out of the bot responding to them. It will remove the user from the
opt-in list and will respond with a message to let the user know that they have opted out. If the user is already opted
out, it will respond with a message to let the user know that they are already opted out.
- `/imdadoptstatus` - This command allows users to check their opt-in status. It will respond with a message to let the
user know if they are opted in or out.
- `/imdadoptouts` - This command allows the owner of the bot to check the opt-in status of all users. It will respond
with a message containing a list of all the users who are opted out.

### .env file:
This cog requires a `.env` file to be created in the `./bot` directory. The `.env` file should contain the following
variables:
- `BLACKLISTED_USERS` - This is a comma separated list of user ids which the bot will ignore. This is useful for users
which are bad actors and are trying to get the bot to respond to them with something inappropriate.
- `IMDAD_SPAM_USERS` - This is a comma separated list of user ids which the bot will ignore. This is useful for users
which are not sending messages which are inappropriate, but are attempting to send messages to the bot in a way which
will cause the bot to spam the channel.
- `IMDAD_EXCLUDED_CHANNELS` - This is a comma separated list of channel ids which the bot will ignore. This is useful
for channels which are not appropriate for the bot to be active in.
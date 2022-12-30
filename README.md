# hamyamdiscord
HamYam bot ported to Discord

## Installation
This bot requires a Discord API key, QRZ XML data access, and Python3.

1. Edit the hamyambot.py file to include your credentials for Discord and QRZ
2. Install required python libraries
> python -m pip install -r requirements.txt; python -m pip install discord.py
3. Run the bot
> python hamyambot.py

## Creating a Discord bot
This guide assumes that you have at least some familiarity with how bots are created from within the Discord developer portal, however some basic information about the correct permissions and inviting the bot to your server are provided here. 

### Build-a-bot

Follow the guide at https://discordpy.readthedocs.io/en/stable/discord.html for creating a Discord bot and inviting it to your server. The bot will need to be running and have the proper keys and credentials inserted into the hamyambot.py file before you can invite it to your server. When generating the OAUTH2 invitation URL, you will need to ensure that the following permissions are enabled for the bot to function properly:
![](https://i.imgur.com/MYkd0pB.png)
![](https://i.imgur.com/1iBHUXU.png)

Once you have configured these parameters, simply copy and paste the generated URL into your web browser to invite the bot to your server.

### Note on Guild IDs
When editing the hamyambot.py file, there is a list for you to insert "guild IDs". These are needed, since new or modified Discord bots can take up to 24 hours to properly sync commands with a server after the bot is first invited. To obtain this ID, follow this guide: https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID- Adding this ID to your configuration will allow the bot to properly sync commands with your server in just a few moments.

## Usage
Once the bot is running and added to a Discord server, you can then run commands to perform various functions. Run the "/help" command for a list of available commands, and their parameters, as well as to display other information about the bot. You can also type a single "/" to see a list of commands available to be run in your server.

![](https://i.imgur.com/SeBfM4v.png)
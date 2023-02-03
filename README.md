# hamyamdiscord
HamYam bot ported to Discord

## Installation
This bot requires a Discord API key, QRZ XML data access, an Imgur Client ID, and Python3.

1. Install required python libraries from the requirements.txt file
> python -m pip install -r requirements.txt
2. Edit the hamyam.conf file to include your credentials for Discord and QRZ. This file is in JSON format. See below for information on obtaining these credentials.
3. Run the bot
> python hamyambot.py

## Configuration
Information about the bot's configuration options is provided here. This file is in JSON format, so you will need to take care to follow proper JSON formatting when adding your information. A JSON validation tool may help in ensuring that you are following the correct format.

### QRZ_USERNAME
The username you would normally use to log in to QRZ. This will typically be your callsign or email address.

### QRZ_PASSWORD
The password you would normally use to log in to QRZ. This will be the password you set when logging in to QRZ. Best security practice does dictate that websites should strive to use API keys wherever possible, however QRZ does not offer API keys for accounts with XML data access.

### IMGUR_CLIENT_ID
The client ID obtained from a new Imgur application. Please see below for an explanation on why this is required, as well as where to obtain this.

### DISCORD_TOKEN
The Discord bot token, explained further below.

### GUILD_IDS
The Server IDs in list format for all of the servers that the bot is a part of. Instructions on how to obtain server IDs are listed below.

### Global variables
The bot uses several global variables to define the URLs used for various lookups and embeds. These are contained within several global variables, and should not be modified unless you know exactly what you are doing. Changes to these values may result in unexpected behavior!

## Creating a Discord bot
This guide assumes that you have at least some familiarity with how bots are created from within the Discord developer portal, however some basic information about the correct permissions and inviting the bot to your server are provided here. 

### Build-a-bot
Follow the guide at https://discordpy.readthedocs.io/en/stable/discord.html for creating a Discord bot and inviting it to your server. The bot will need to be running and have the proper keys and credentials inserted into the hamyambot.py file before you can invite it to your server. When generating the OAUTH2 invitation URL, you will need to ensure that the following permissions are enabled for the bot to function properly:
![](https://i.imgur.com/MYkd0pB.png)
![](https://i.imgur.com/5FSwjTT.png)

Once you have configured these parameters, simply copy and paste the generated URL into your web browser to invite the bot to your server.

### Note on Guild IDs
When editing the hamyam.conf file, there is a list for you to insert "guild IDs". These are needed, since new or modified Discord bots can take up to 24 hours to properly sync commands with a server after the bot is first invited. To obtain this ID, follow this guide: https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID- Adding this ID to your configuration will allow the bot to properly sync commands with your server in just a few moments.

## Imgur Client ID
Due to a potential bug in the interactions.py library that this bot uses, it's not currently possible for bots to embed URLs ending in anything other than a known image file extension. As a temporary workaround, the bot uses Imgur to upload a copy of an image, and obtain a URL that can be embedded in a Discord message. To obtain this Client ID, you will need to create an Imgur account. New Imgur accounts do require a verified phone number, and there is no workaround to this. Any files uploaded to Imgur by the bot are not linked to your Imgur account.

### Obtaining the Imgur Client ID
Once you have an Imgur account, visit https://api.imgur.com/oauth2/addclient and fill out the form with the proper details. A website and description are not required, but the email address field and callback URL must be populated for this to work correctly. 

Since we do not need a callback URL, you can use the Postman dummy callback URL.
> https://www.getpostman.com/oauth2/callback

![](https://i.imgur.com/ne41kHE.png)

Finally, fill out the Captcha at the bottom of the page and click "Submit". You will be presented with both a Client ID and a Client Secret.

**You only need the Client ID! The Client Secret can be ignored!**

## Usage
Once the bot is running and added to a Discord server, you can then run commands to perform various functions. Run the "/help" command for a list of available commands, and their parameters, as well as to display other information about the bot. You can also type a single "/" to see a list of commands available to be run in your server.

![](https://i.imgur.com/SeBfM4v.png)

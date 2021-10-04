# HamYam Discord Bot
# HamYam bot ported from Telegram to Discord
# Original bot created for Telegram by V
# Converted to a Discord bot by Red in 2021
# Greetings from ROC
# 73 de KD2SSH

# https://github.com/rdragonz/hamyamdiscord

# This code is licensed under the GNU General Public License v3.0
# For more information see the LICENSE file that was distributed with this code
# Or visit https://www.gnu.org/licenses/gpl-3.0.en.html


# ----- BEGIN SECRETS AND KEYS FOR BOT -----
QRZ_USERNAME = '' # Remove before flight
QRZ_PASSWORD = '' # Remove before flight
DISCORD_TOKEN = '' # Remove before flight
GUILD_IDS = [] # Remove before flight
# ----- END SECRETS AND KEYS FOR BOT -----

import logging
import requests
import xmltodict
import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
import pycountry
from uuid import uuid4
import numpy as np
import maidenhead as mh
import json
import random


# Define global objects
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

client = discord.Client(intents=discord.Intents.default())
slash = SlashCommand(client, sync_commands=True) # Declares slash commands through the client.

def escapeChars(txt):
		message = txt
		temp = message.replace('-', '\-')
		temp = temp.replace('.', '\.')
		temp = temp.replace('#', '\#')
		temp = temp.replace('(', '\(')
		temp = temp.replace('=', '\=')
		temp = temp.replace(')', '\)')
		temp = temp.replace('+', '\+')
		temp = temp.replace('!', '\!')
		#temp = temp.replace('.', '\.')
		return temp

def qrz_lookup(callsign):
		url = '''https://xmldata.qrz.com/xml/current/?username={0}&password={1}'''.format(QRZ_USERNAME, QRZ_PASSWORD)
		session = requests.Session()
		r = session.get(url)
		raw_session = xmltodict.parse(r.content)
		session_key = raw_session.get('QRZDatabase').get('Session').get('Key')

		url2 = """https://xmldata.qrz.com/xml/current/?s={0}&callsign={1}""".format(session_key, callsign)
		r2 = session.get(url2)
		raw = xmltodict.parse(r2.content).get('QRZDatabase')
		ham = raw.get('Callsign')
		return ham

def lookup_call(callsign):
		"""Add a job to the queue."""

		if len(callsign) < 3 or len(callsign) >= 15:
			return 'Please provide a valid call sign.'

		outs = qrz_lookup(str(callsign))

		if not outs:
			return 'No results found on QRZ.com'
		else:
			message = str()

			if 'country' in outs:
				try:
					country_emoji_search = pycountry.countries.search_fuzzy(outs['country'])

					if country_emoji_search:
						ces_first = country_emoji_search[0]
						if hasattr(ces_first, 'alpha_2'):
							ces_outs = (":flag_" + ces_first.alpha_2.lower() + ":")
							message += ces_outs
				except:
					message += str(outs['country'])

			if 'call' in outs:
				message += '  __**{0}**__'.format(str(outs['call']))

			message += '\n**Name:** '
			if 'fname' in outs:
				message += str(escapeChars(outs['fname']))
			if 'name' in outs:
				message += " " + str(escapeChars(outs['name']))

			if 'aliases' in outs:
				message += '\n**Aliases:** {0}'.format(str(outs['aliases']))

			if 'trustee' in outs:
				message += '\n**Trustee:** {0}'.format(str(outs['trustee']))

			if 'class' in outs:
				message += '\n**Class:** {0}'.format(str(outs['class']))

			if 'addr2' in outs:
				message += '\n**Location:** {0}'.format(str(escapeChars(outs['addr2'])))

			if 'state' in outs:
				message += ', {0}'.format(str(escapeChars(outs['state'])))

			if 'country' in outs:
				message += ', {0}'.format(str(escapeChars(outs['country'])))

			if 'grid' in outs:
				grid_code = str(outs['grid'][:4])
				# https://aprs.fi/#!addr=EM89
				message += ' \[[{0}]({1})\]'.format(grid_code, 'https://www.karhukoti.com/maidenhead-grid-square-locator/?grid=' + str(grid_code))

			if 'cqzone' in outs:
				message += '\n**CQ Zone:** {0}'.format(str(outs['cqzone']))

			if 'ituzone' in outs:
				message += '\n**ITU Zone:** {0}'.format(str(outs['ituzone']))

			if 'efdate' in outs and outs['efdate'] != '0000-00-00':
				message += '\n**Granted:** {0}'.format(str(escapeChars(outs['efdate'])))

			if 'expdate' in outs and outs['expdate'] != '0000-00-00':
				message += '\n**Expiry:** {0}'.format(str(escapeChars(outs['expdate'])))

			yes_var = ':white_check_mark:'
			no_var = ':x:'

			if 'lotw' in outs:
				message += '\n**QSL via LoTW:** '
				if outs['lotw'] == '1':
					message += yes_var
				else:
					message += no_var

			if 'eqsl' in outs:
				message += '\n**QSL via eQSL:** '
				if outs['eqsl'] == '1':
					message += yes_var
				else:
					message += no_var

			if 'mqsl' in outs:
				message += '\n**QSL via Mail:** '
				if outs['mqsl'] == '1':
					message += yes_var
				else:
					message += no_var

			if 'qslmgr' in outs:
				message += '\n**QSL Manager:** {0}'.format(escapeChars(str(outs['qslmgr'])))


			message += '\n[Profile on QRZ](https://www.qrz.com/db/{0})'.format(str(outs['call']).upper())

			return message

def distance(mh1, mh2):
		'''
		calculate the distance between two maidenhead locations
		'''

		error_mh = 'Please provide two valid Maidenhead locations.'

		if len(mh1) < 4 or len(mh2) < 4 or len(mh1) > 6 or len(mh2) > 6 or not mh1[:2].isalpha() or not mh2[:2].isalpha():
			return error_mh

		mh1_gps = mh.to_location(mh1)
		mh2_gps = mh.to_location(mh2)

		answer = haversine_distance(mh1_gps[0], mh1_gps[1], mh2_gps[0], mh2_gps[1])
		answer_miles = np.round(answer * 0.62137119224, 2)

		outs = 'Distance is: {0} km ({1} mi)'.format(str(answer), str(answer_miles))
		return outs

def haversine_distance(lat1, lon1, lat2, lon2):
		r = 6371
		phi1 = np.radians(lat1)
		phi2 = np.radians(lat2)
		delta_phi = np.radians(lat2 - lat1)
		delta_lambda = np.radians(lon2 - lon1)
		a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
		res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
		return np.round(res, 2)

def dmr_by_call(callsign):
	url = '''https://www.radioid.net/api/dmr/user/?callsign={0}'''.format(callsign)
	session = requests.Session()
	r = session.get(url)
	message = str()
	if not r:
		message = "This callsign is not associated with a DMR ID."
	else:
		content = json.loads(r.content.decode("utf-8"))
		if int(content["count"]) == 0:
			message = "This callsign is not associated with a DMR ID."
		else:
			message += "**__DMR ID Report__**\n"
			message += "**Callsign: **" + content["results"][0]["callsign"] + "\n"
			if int(content["count"]) > 1:
				message += "This callsign is assoicated with multiple DMR IDs\n**DMR IDs:** "
			else:
				message += "**DMR ID:** "
			count = content["count"]
			for item in range(count):
				message += str(content["results"][item]["id"])
				if item != (count-1):
					message += ", "
			message += "\n"
			message += "**Name: **" + content["results"][0]["fname"] + " " + content["results"][0]["surname"] + "\n"
			message += "**Country: **" + content["results"][0]["country"] + "\n"
			message += "**Location: **" + content["results"][0]["city"]
			if content["results"][0]["state"] != "":
				message += ", " + content["results"][0]["state"]

	return message

def call_by_dmrid(callsign):
	url = '''https://www.radioid.net/api/dmr/user/?id={0}'''.format(callsign)
	session = requests.Session()
	r = session.get(url)
	message = str()
	if not r:
		message = "This DMR ID is not associated with a callsign."
	else:
		content = json.loads(r.content.decode("utf-8"))
		if int(content["count"]) == 0:
			message = "This DMR ID is not associated with a callsign."
		else:
			message += "**__DMR ID Report__**\n"
			message += "**Callsign: **" + content["results"][0]["callsign"] + "\n"
			if int(content["count"]) > 1:
				message += "This callsign is assoicated with multiple DMR IDs\n**DMR IDs:** "
			else:
				message += "**DMR ID:** "
			count = content["count"]
			for item in range(count):
				message += str(content["results"][item]["id"])
				if item != (count-1):
					message += ", "
			message += "\n"
			message += "**Name: **" + content["results"][0]["fname"] + " " + content["results"][0]["surname"] + "\n"
			message += "**Country: **" + content["results"][0]["country"] + "\n"
			message += "**Location: **" + content["results"][0]["city"]
			if content["results"][0]["state"] != "":
				message += ", " + content["results"][0]["state"]

	return message

# Define commands

@slash.slash(name="dmridbycall", description="Look up a DMR ID by callsign",options=[
			   create_option(
				 name="callsign",
				 description="Callsign",
				 option_type=3,
				 required=True
			   )], guild_ids=GUILD_IDS)
async def _dmridbycall(ctx, callsign: str):
  await ctx.send(content=dmr_by_call(callsign))

@slash.slash(name="callbydmrid", description="Look up a callsign by DMR ID",options=[
			   create_option(
				 name="dmrid",
				 description="DMR ID",
				 option_type=3,
				 required=True
			   )], guild_ids=GUILD_IDS)
async def _callbydmrid(ctx, dmrid: str):
  await ctx.send(content=call_by_dmrid(dmrid))

@slash.slash(name="lookup", description="Look up a callsign on QRZ",options=[
			   create_option(
				 name="callsign",
				 description="Callsign",
				 option_type=3,
				 required=True
			   )], guild_ids=GUILD_IDS)
async def _lookup(ctx, callsign: str):
  await ctx.send(content=lookup_call(callsign))

@slash.slash(name="distance", description="Calculate distance between two Maidenhead gridsqare locators",options=[
			   create_option(
				 name="gridsquare1",
				 description="Gridsquare 1",
				 option_type=3,
				 required=True
			   ),
			   create_option(
				 name="gridsquare2",
				 description="Gridsquare 2",
				 option_type=3,
				 required=True
			   )], guild_ids=GUILD_IDS)
async def _distance(ctx, gridsquare1: str, gridsquare2: str):
  await ctx.send(content=distance(gridsquare1, gridsquare2))

@slash.slash(name="ping", description="Display SlashCommand to Bot to API Latency. Used for debug purposes.", guild_ids=GUILD_IDS)
async def _ping(ctx):
  await ctx.send(f"Command to Bot to API Latency: ({client.latency*1000}ms)")

@slash.slash(name="help", description="Display help and general bot information", guild_ids=GUILD_IDS)
async def _help(ctx):
  await ctx.send("""```HELP FOR HAMYAM BOT:
/lookup <CALLSIGN> - Look up a callsign on QRZ
/conditions - Display current ham band conditions
/distance <GRIDSQARE 1> <GRIDSQUARE 2> - Calculate distance between two Maidenhead gridsqare locators
/muf - Display current calculated Maximum Usable Frequency information
/bands - Display ARRL ham bands document
/dmridbycall <CALLSIGN> - Look up a DMR ID by callsign
/callbydmrid <DMR ID> - Look up a callsign by DMR ID
/help - Display this help document
/ping - Display SlashCommand to Bot to API Latency. Used for debug purposes.

HAMYAM bot originally created for Telegram by V
Ported to Discord by Red in 2021
73 de KD2SSH

https://github.com/rdragonz/hamyamdiscord

This version of HAMYAM bot is licensed under the GNU General Public License v3.0
For more information on the GPLv3.0 visit https://www.gnu.org/licenses/gpl-3.0.en.html
	
HAMYAMDiscord v1.00 10/03/2021
```
	""")

@slash.slash(name="conditions", description="Display current ham band conditions", guild_ids=GUILD_IDS)
async def _conditions(ctx):
  await ctx.send("http://www.hamqsl.com/solar101vhfpic.php?id={0}".format(random.randint(0, 9999999999)))

@slash.slash(name="muf", description="Display current calculated Maximum Usable Frequency information", guild_ids=GUILD_IDS)
async def _muf(ctx):
  await ctx.send("http://www.hamqsl.com/solarmuf.php?id={0}".format(random.randint(0, 9999999999)))

@slash.slash(name="bands", description="Display ARRL ham bands document", guild_ids=GUILD_IDS)
async def _bands(ctx):
  await ctx.send("https://i.imgur.com/j18VSeB.png")

def main():
	"""Run bot."""
	client.run(DISCORD_TOKEN)

if __name__ == '__main__':
	main()
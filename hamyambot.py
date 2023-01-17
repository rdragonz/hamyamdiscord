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

# ----- FOR CONFIGURATION INFORMATION, PLEASE REFERENCE THE README.md FILE -----
# ----- BEGIN SECRETS AND KEYS FOR BOT -----
QRZ_USERNAME = '' # Remove before flight
QRZ_PASSWORD = '' # Remove before flight
DISCORD_TOKEN = '' # Remove before flight
GUILD_IDS = [] # Remove before flight
# ----- END SECRETS AND KEYS FOR BOT -----

# GLOBALS

QRZ_URL = "https://xmldata.qrz.com/xml/current/"
QRZ_PROFILE = "https://www.qrz.com/db/"
DMRID_URL = "https://www.radioid.net/api/dmr/user/"
GRIDSQUARE_URL = "https://www.karhukoti.com/maidenhead-grid-square-locator/"
CONDITIONS_URL = "http://www.hamqsl.com/solar101vhfpic.php"
MUF_URL = "http://www.hamqsl.com/solarmuf.php"
BANDS_URL = "https://i.imgur.com/j18VSeB.png"
VERSION_STRING = "HAMYAMDiscord v3.00-BETA2 01/16/2023"

import logging
import requests
import xmltodict
import interactions
import pycountry
from uuid import uuid4
import numpy as np
import maidenhead as mh
import json
import random
import zipcodes


# Define global objects
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
client = interactions.Client(token=DISCORD_TOKEN)

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
	url = '''{0}?username={1}&password={2}'''.format(QRZ_URL, QRZ_USERNAME, QRZ_PASSWORD)
	session = requests.Session()
	r = session.get(url)
	raw_session = xmltodict.parse(r.content)
	session_key = raw_session.get('QRZDatabase').get('Session').get('Key')

	url2 = """{0}?s={1}&callsign={2}""".format(QRZ_URL, session_key, callsign)
	r2 = session.get(url2)
	raw = xmltodict.parse(r2.content).get('QRZDatabase')
	ham = raw.get('Callsign')
	return ham

def lookup_call(callsign):
	"""Add a job to the queue."""

	if len(callsign) < 3 or len(callsign) >= 15:
		return '__**{}**__\nThis callsign does not appear to be valid.'.format(callsign)

	outs = qrz_lookup(str(callsign))

	if not outs:
		return '__**{}**__\nNo results found on QRZ.com'.format(callsign)
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
			message += ' \[[{0}]({1})\]'.format(grid_code, '{0}?grid='.format(GRIDSQUARE_URL) + str(grid_code))

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


		message += '\n[Profile on QRZ]({0}{1})'.format(QRZ_PROFILE, str(outs['call']).upper())

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
	url = '''{0}callsign={1}'''.format(DMRID_URL, callsign)
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
	url = '''{0}?id={1}'''.format(DMRID_URL, callsign)
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

def ziptogrid(zipcode):
	# Quick validity check
	try:
		int(zipcode)

	except ValueError:
		return "The entered Zipcode does not appear to be a valid United States Zipcode."

	if len(zipcode) != 5:
		return "The entered Zipcode does not appear to be a valid United States Zipcode."

	try:
		zipParsed = zipcodes.matching(zipcode)
		if len(zipParsed) == 0:
			return "The entered Zipcode was unable to be located. Is it a valid United States Zipcode?"

	except ValueError:
		return "The entered Zipcode does not appear to be a valid United States Zipcode."

	# Convert to Gridsquare
	lat = float(zipParsed[0]['lat'])
	lon = float(zipParsed[0]['long'])
	state = zipParsed[0]['state']
	city = zipParsed[0]['city']

	gridsquare = mh.to_maiden(lat, lon)

	message = "**{0}, {1} {2}**\n{3}, {4}\n\n**Gridsquare:** {5}".format(city, state, zipcode, lat, lon, gridsquare)

	return message

# Define commands

@client.command(name="dmridbycall", description="Look up a DMR ID by callsign",
	options=[
		interactions.Option(
			name="callsign",
			description="Callsign",
			type=interactions.OptionType.STRING,
			required=True,
		),], scope=GUILD_IDS)
async def _dmridbycall(ctx: interactions.CommandContext, callsign: str):
	await ctx.send(dmr_by_call(callsign))

@client.command(name="callbydmrid", description="Look up a callsign by DMR ID",options=[
			interactions.Option(
			name="dmrid",
			description="DMR ID",
			type=interactions.OptionType.STRING,
			required=True
			)], scope=GUILD_IDS)
async def _callbydmrid(ctx: interactions.CommandContext, dmrid: str):
	await ctx.send(call_by_dmrid(dmrid))

@client.command(name="lookup", description="Look up a callsign on QRZ",options=[
			interactions.Option(
			name="callsign",
			description="Callsign",
			type=interactions.OptionType.STRING,
			required=True
			)], scope=GUILD_IDS)
async def _lookup(ctx: interactions.CommandContext, callsign: str):
	await ctx.send(lookup_call(callsign))

@client.command(name="distance", description="Calculate distance between two Maidenhead gridsquare locators",options=[
			interactions.Option(
			name="gridsquare1",
			description="Gridsquare 1",
			type=interactions.OptionType.STRING,
			required=True
			),
			interactions.Option(
			name="gridsquare2",
			description="Gridsquare 2",
			type=interactions.OptionType.STRING,
			required=True
			)], scope=GUILD_IDS)
async def _distance(ctx: interactions.CommandContext, gridsquare1: str, gridsquare2: str):
	await ctx.send(distance(gridsquare1, gridsquare2))

@client.command(name="ping", description="Display SlashCommand to Bot to API Latency. Used for debug purposes.", scope=GUILD_IDS)
async def _ping(ctx: interactions.CommandContext):
	await ctx.send(f"Command to Bot to API Latency: ({client.latency*1000}ms)")

@client.command(name="help", description="Display help and general bot information", scope=GUILD_IDS)
async def _help(ctx: interactions.CommandContext):
	await ctx.send("""```HELP FOR HAMYAM BOT:
/lookup <CALLSIGN> - Look up a callsign on QRZ
/conditions - Display current ham band conditions
/distance <GRIDSQUARE 1> <GRIDSQUARE 2> - Calculate distance between two Maidenhead gridsquare locators
/muf - Display current calculated Maximum Usable Frequency information
/bands - Display ARRL ham bands document
/dmridbycall <CALLSIGN> - Look up a DMR ID by callsign
/callbydmrid <DMR ID> - Look up a callsign by DMR ID
/ziptogrid <US Zipcode> - Obtain the Maidenhead gridsquare of a United States Zipcode.
/help - Display this help document
/ping - Display SlashCommand to Bot to API Latency. Used for debug purposes.


HAMYAM bot originally created for Telegram by V
Ported to Discord by Red in 2021
73 de KD2SSH

https://github.com/rdragonz/hamyamdiscord

This version of HAMYAM bot is licensed under the GNU General Public License v3.0
For more information on the GPLv3.0 visit https://www.gnu.org/licenses/gpl-3.0.en.html
	
{}
```
	""".format(VERSION_STRING))

@client.command(name="conditions", description="Display current ham band conditions", scope=GUILD_IDS)
async def _conditions(ctx: interactions.CommandContext):
  await ctx.send("{0}?id={1}".format(CONDITIONS_URL, random.randint(0, 9999999999)))

@client.command(name="muf", description="Display current calculated Maximum Usable Frequency information", scope=GUILD_IDS)
async def _muf(ctx: interactions.CommandContext):
  await ctx.send("{0}?id={1}".format(MUF_URL, random.randint(0, 9999999999)))

@client.command(name="bands", description="Display ARRL ham bands document", scope=GUILD_IDS)
async def _bands(ctx: interactions.CommandContext):
  await ctx.send("{0}".format(BANDS_URL))

@client.command(name="ziptogrid", description="Convert a United States Zipcode to a Maidenhead gridsquare location",options=[
				interactions.Option(
				name="zipcode",
				description="United States Zip Code",
				type=interactions.OptionType.STRING,
				required=True
				)], scope=GUILD_IDS)
async def _ziptogrid(ctx: interactions.CommandContext, zipcode: str):
  await ctx.send(ziptogrid(zipcode))

def main():
	# Run the bot
	client.start()

if __name__ == '__main__':
	main()

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

import logging
import interactions
from uuid import uuid4
import random

import hamyam


# Define global objects
config_data = hamyam.config.Configuration("hamyam.conf")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
client = interactions.Client(token=config_data.config["DISCORD_TOKEN"])

# Define commands

# /dmridbycall
@client.command(name="dmridbycall", description="Look up a DMR ID by callsign",
	options=[
		interactions.Option(
			name="callsign",
			description="Callsign",
			type=interactions.OptionType.STRING,
			required=True,
		),], scope=config_data.config["GUILD_IDS"])
async def _dmridbycall(ctx: interactions.CommandContext, callsign: str):
	await ctx.send(embeds=hamyam.dmr_by_call.dmr_by_call(callsign, config_data))

# /callbydmrid
@client.command(name="callbydmrid", description="Look up a callsign by DMR ID",options=[
			interactions.Option(
			name="dmrid",
			description="DMR ID",
			type=interactions.OptionType.STRING,
			required=True
			)], scope=config_data.config["GUILD_IDS"])
async def _callbydmrid(ctx: interactions.CommandContext, dmrid: str):
	await ctx.send(embeds=hamyam.call_by_dmrid.call_by_dmrid(dmrid, config_data))

# /lookup
@client.command(name="lookup", description="Look up a callsign on QRZ",options=[
			interactions.Option(
			name="callsign",
			description="Callsign",
			type=interactions.OptionType.STRING,
			required=True
			)], scope=config_data.config["GUILD_IDS"])
async def _lookup(ctx: interactions.CommandContext, callsign: str):
	await ctx.send(hamyam.lookup_call.lookup_call(callsign, config_data))

# /distance
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
			)], scope=config_data.config["GUILD_IDS"])
async def _distance(ctx: interactions.CommandContext, gridsquare1: str, gridsquare2: str):
	await ctx.send(embeds=hamyam.distance.distance(gridsquare1, gridsquare2, config_data))

# /ping
@client.command(name="ping", description="Display SlashCommand to Bot to API Latency. Used for debug purposes.", scope=config_data.config["GUILD_IDS"])
async def _ping(ctx: interactions.CommandContext):
	await ctx.send(f"Command to Bot to API Latency: ({client.latency*1000}ms)")

# /help
@client.command(name="help", description="Display help and general bot information", scope=config_data.config["GUILD_IDS"])
async def _help(ctx: interactions.CommandContext):
	await ctx.send(hamyam.help.help(config_data))

# /conditions
@client.command(name="conditions", description="Display current ham band conditions", scope=config_data.config["GUILD_IDS"])
async def _conditions(ctx: interactions.CommandContext):
	await ctx.send("{0}?id={1}".format(config_data.config["CONDITIONS_URL"], random.randint(0, 9999999999)))

# /muf
@client.command(name="muf", description="Display current calculated Maximum Usable Frequency information", scope=config_data.config["GUILD_IDS"])
async def _muf(ctx: interactions.CommandContext):
	await ctx.send("{0}?id={1}".format(config_data.config["MUF_URL"], random.randint(0, 9999999999)))

# /bands
@client.command(name="bands", description="Display ARRL ham bands document", scope=config_data.config["GUILD_IDS"])
async def _bands(ctx: interactions.CommandContext):
	await ctx.send("{0}".format(config_data.config["BANDS_URL"]))

# /ziptogrid
@client.command(name="ziptogrid", description="Convert a United States Zipcode to a Maidenhead gridsquare location",options=[
				interactions.Option(
				name="zipcode",
				description="United States Zip Code",
				type=interactions.OptionType.STRING,
				required=True
				)], scope=config_data.config["GUILD_IDS"])
async def _ziptogrid(ctx: interactions.CommandContext, zipcode: str):
	await ctx.send(embeds=hamyam.ziptogrid.ziptogrid(zipcode, config_data))

def main():
	# Run the bot
	print(config_data.config["VERSION_STRING"])
	client.start()


if __name__ == '__main__':
	main()

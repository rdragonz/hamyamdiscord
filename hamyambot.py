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

import hamyam


# Define global objects
config_data = hamyam.config.Configuration("hamyam.conf")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
client = interactions.Client(token=config_data.config["DISCORD_TOKEN"])

# Define commands

# /dmridbycall
@interactions.slash_command(name="dmridbycall", description=config_data.lang["DESCRIPTION_DMRIDBYCALL"], scopes=config_data.config["GUILD_IDS"])
@interactions.slash_option(
	name="callsign",
	description=config_data.lang["CALLSIGN"],
	opt_type=interactions.OptionType.STRING,
	required=True,
)
async def _dmridbycall(ctx: interactions.SlashContext, callsign: str):
	await ctx.send(embeds=hamyam.dmr_by_call.dmr_by_call(callsign, config_data))

# /callbydmrid
@interactions.slash_command(name="callbydmrid", description=config_data.lang["DESCRIPTION_CALLBYDMRID"], scopes=config_data.config["GUILD_IDS"])
@interactions.slash_option(
	name="dmrid",
	description=config_data.lang["DMR_ID"],
	opt_type=interactions.OptionType.STRING,
	required=True
)
async def _callbydmrid(ctx: interactions.SlashContext, dmrid: str):
	await ctx.send(embeds=hamyam.call_by_dmrid.call_by_dmrid(dmrid, config_data))

# /lookup
@interactions.slash_command(name="lookup", description=config_data.lang["DESCRIPTION_LOOKUP"], scopes=config_data.config["GUILD_IDS"])
@interactions.slash_option(
	name="callsign",
	description=config_data.lang["CALLSIGN"],
	opt_type=interactions.OptionType.STRING,
	required=True
)
async def _lookup(ctx: interactions.SlashContext, callsign: str):
	await ctx.send(embeds=hamyam.lookup_call.lookup_call(callsign, config_data))

# /distance
@interactions.slash_command(name="distance", description=config_data.lang["DESCRIPTION_DISTANCE"], scopes=config_data.config["GUILD_IDS"])
@interactions.slash_option(
	name="gridsquare1",
	description=config_data.lang["GRIDSQUARE1"],
	opt_type=interactions.OptionType.STRING,
	required=True
)
@interactions.slash_option(
	name="gridsquare2",
	description=config_data.lang["GRIDSQUARE2"],
	opt_type=interactions.OptionType.STRING,
	required=True
) 
async def _distance(ctx: interactions.SlashContext, gridsquare1: str, gridsquare2: str):
	await ctx.send(embeds=hamyam.distance.distance(gridsquare1, gridsquare2, config_data))

# /ping
@interactions.slash_command(name="ping", description=config_data.lang["DESCRIPTION_PING"], scopes=config_data.config["GUILD_IDS"])
async def _ping(ctx: interactions.SlashContext):
	await ctx.send("{0} {1}ms".format(config_data.lang["PING_RESPONSE"],int(client.latency)))

# /help
@interactions.slash_command(name="help", description=config_data.lang["DESCRIPTION_HELP"], scopes=config_data.config["GUILD_IDS"])
async def _help(ctx: interactions.SlashContext):
	await ctx.send(hamyam.help.help(config_data))

# /conditions
@interactions.slash_command(name="conditions", description=config_data.lang["DESCRIPTION_CONDITIONS"], scopes=config_data.config["GUILD_IDS"])
async def _conditions(ctx: interactions.SlashContext):
	await ctx.send(embeds=hamyam.conditions.conditions(config_data))

# /muf
@interactions.slash_command(name="muf", description=config_data.lang["DESCRIPTION_MUF"], scopes=config_data.config["GUILD_IDS"])
async def _muf(ctx: interactions.SlashContext):
	embed, image = hamyam.muf.muf(config_data)
	await ctx.send(embeds=embed, file=image)

# /bands
@interactions.slash_command(name="bands", description=config_data.lang["DESCRIPTION_BANDS"], scopes=config_data.config["GUILD_IDS"])
async def _bands(ctx: interactions.SlashContext):
	await ctx.send(embeds=hamyam.bands.bands(config_data))

# /ziptogrid
@interactions.slash_command(name="ziptogrid", description=config_data.lang["DESCRIPTION_ZIPTOGRID"], scopes=config_data.config["GUILD_IDS"])
@interactions.slash_option(
	name="zipcode",
	description=config_data.lang["ZIPCODE"],
	opt_type=interactions.OptionType.STRING,
	required=True
)
async def _ziptogrid(ctx: interactions.SlashContext, zipcode: str):
	await ctx.send(embeds=hamyam.ziptogrid.ziptogrid(zipcode, config_data))

def main():
	# Run the bot
	print(config_data.config["VERSION_STRING"])
	client.start()


if __name__ == '__main__':
	main()

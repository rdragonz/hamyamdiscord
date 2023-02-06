import interactions
import pycountry
import hamyam.qrz_lookup
import hamyam.escapeChars

def lookup_call(callsign, config):
	# Look up a callsign on QRZ and generate a report
	# Takes: Callsign
	# Returns: Interactions.py embed format

	message = interactions.Embed(
		title="**__{0}__**".format(callsign.upper()),
		color=hamyam.callsign_color.callsign_color(callsign.upper())
	)

	# Quick validity check
	if len(callsign) > 250:
		message = interactions.Embed(
			title="**__SERIOUS ERROR__**",
			color=16711680
		)
		message.add_field("Error", "A serious error has occured. Please submit this as a bug to the [Github Issues Page]({}).".format(config.config["GITHUB_ISSUES_URL"]))
		return message

	if len(callsign) < 3 or len(callsign) >= 15:
		message.add_field("Error", "This callsign does not appear to be valid.")
		return message

	# Search QRZ for callsign
	outs = hamyam.qrz_lookup.qrz_lookup(str(callsign), config)

	# Alert if callsign not found on QRZ
	if not outs:
		message.add_field("Error", "No results found on QRZ.com.")
		return message
	else:
		# Begin processing data from QRZ

		# Name
		name = str()
		if 'fname' in outs:
			name += str(hamyam.escapeChars.escapeChars(outs['fname']))
		if 'name' in outs:
			name += " " + str(hamyam.escapeChars.escapeChars(outs['name']))

		message.add_field("Name", name)

		# Aliases/Trustee/Class
		if 'aliases' in outs:
			message.add_field("Aliases", str(outs['aliases']), inline=True)
		if 'trustee' in outs:
			message.add_field("Trustee", str(outs['trustee']), inline=True)
		if 'class' in outs:
			message.add_field("Class", str(outs['class']), inline=True)

		# Location
		location = str()
		if 'addr2' in outs:
			location += str(hamyam.escapeChars.escapeChars(outs['addr2']))
		if 'state' in outs:
			location += ', {0}'.format(str(hamyam.escapeChars.escapeChars(outs['state'])))
		if 'country' in outs:
			location += ', {0}'.format(str(hamyam.escapeChars.escapeChars(outs['country'])))
			try:
				# Find country information to generate the flag emoji
				country_emoji_search = pycountry.countries.search_fuzzy(outs['country'])
				if country_emoji_search:
					ces_first = country_emoji_search[0]
					if hasattr(ces_first, 'alpha_2'):
						ces_outs = (" :flag_" + ces_first.alpha_2.lower() + ":")
					location += ces_outs	
			except:
				location += ""
		message.add_field("Location", location)

		# Misc info
		if 'grid' in outs:
			grid_code = str(outs['grid'][:4])
			message.add_field("Gridsquare",  '[{0}]({1}{2})'.format(grid_code, config.config["GRIDSQUARE_URL"], str(grid_code)), inline=True)
		if 'cqzone' in outs:
			message.add_field("CQ Zone", str(outs['cqzone']), inline=True)
		if 'ituzone' in outs:
			message.add_field("ITU Zone", str(outs['ituzone']), inline=True)

		# Spacer
		message.add_field("", "")

		# Expiration and Grant Date
		if 'efdate' in outs and outs['efdate'] != '0000-00-00':
			message.add_field("Granted", str(hamyam.escapeChars.escapeChars(outs['efdate'])), inline=True)
		if 'expdate' in outs and outs['expdate'] != '0000-00-00':
			message.add_field("Expiry", str(hamyam.escapeChars.escapeChars(outs['expdate'])), inline=True)

		# Spacer
		message.add_field("", "")

		# QSL Methods
		yes_var = ':white_check_mark:'
		no_var = ':x:'
		if 'lotw' in outs:
			if outs['lotw'] == '1':
				message.add_field("QSL via LoTW", yes_var, inline=True)
			else:
				message.add_field("QSL via LoTW", no_var, inline=True)
		if 'eqsl' in outs:
			if outs['eqsl'] == '1':
				message.add_field("QSL via eQSL", yes_var, inline=True)
			else:
				message.add_field("QSL via eQSL", no_var, inline=True)
		if 'mqsl' in outs:
			if outs['mqsl'] == '1':
				message.add_field("QSL via Mail", yes_var, inline=True)
			else:
				message.add_field("QSL via Mail", no_var, inline=True)
		if 'qslmgr' in outs:
			message.add_field("QSL Manager", hamyam.escapeChars.escapeChars(str(outs['qslmgr'])), inline=True)

		# Links
		message.add_field("Links", "[Profile on QRZ]({0}{1})".format(config.config["QRZ_PROFILE"], str(outs['call']).upper()))

		return message
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

	if len(callsign) < 3 or len(callsign) >= 15:
		message.add_field("Error", "This callsign does not appear to be valid.")
		return message

	outs = hamyam.qrz_lookup.qrz_lookup(str(callsign), config)

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
			message += str(hamyam.escapeChars.escapeChars(outs['fname']))
		if 'name' in outs:
			message += " " + str(hamyam.escapeChars.escapeChars(outs['name']))

		if 'aliases' in outs:
			message += '\n**Aliases:** {0}'.format(str(outs['aliases']))

		if 'trustee' in outs:
			message += '\n**Trustee:** {0}'.format(str(outs['trustee']))

		if 'class' in outs:
			message += '\n**Class:** {0}'.format(str(outs['class']))

		if 'addr2' in outs:
			message += '\n**Location:** {0}'.format(str(hamyam.escapeChars.escapeChars(outs['addr2'])))

		if 'state' in outs:
			message += ', {0}'.format(str(hamyam.escapeChars.escapeChars(outs['state'])))

		if 'country' in outs:
			message += ', {0}'.format(str(hamyam.escapeChars.escapeChars(outs['country'])))

		if 'grid' in outs:
			grid_code = str(outs['grid'][:4])
			# https://aprs.fi/#!addr=EM89
			message += ' \[[{0}]({1})\]'.format(grid_code, '{0}?grid='.format(config.config["GRIDSQUARE_URL"]) + str(grid_code))

		if 'cqzone' in outs:
			message += '\n**CQ Zone:** {0}'.format(str(outs['cqzone']))

		if 'ituzone' in outs:
			message += '\n**ITU Zone:** {0}'.format(str(outs['ituzone']))

		if 'efdate' in outs and outs['efdate'] != '0000-00-00':
			message += '\n**Granted:** {0}'.format(str(hamyam.escapeChars.escapeChars(outs['efdate'])))

		if 'expdate' in outs and outs['expdate'] != '0000-00-00':
			message += '\n**Expiry:** {0}'.format(str(hamyam.escapeChars.escapeChars(outs['expdate'])))

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
			message += '\n**QSL Manager:** {0}'.format(hamyam.escapeChars.escapeChars(str(outs['qslmgr'])))


		message += '\n[Profile on QRZ]({0}{1})'.format(config.config["QRZ_PROFILE"], str(outs['call']).upper())

		return message
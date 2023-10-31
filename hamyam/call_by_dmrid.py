import interactions
import requests
import json
import hamyam.callsign_color
import hamyam.escapeChars

def call_by_dmrid(callsign, config):
	# Obtain callsign from DMR ID
	# Takes: DMR ID
	# Returns: Interactions embed format containing callsign report

	# Quick validity check and error message
	callsign = hamyam.escapeChars.escapeChars(callsign)

	if not callsign.isalnum():
		message = interactions.Embed(
			title="**__{0}__**".format(config.lang["INPUT_ERROR"]),
			color=16711680
		)
		message.add_field(config.lang["ERROR"], config.lang["INPUT_ERROR_LONG"])
		return message

	if len(callsign) != 7:
		message = interactions.Embed(
			title="**__{0}__**".format(config.lang["DMR_ID_REPORT"]),
			description=callsign.upper(),
			color=16711680
		)
		message.add_field(config.lang["ERROR"], config.lang["DMR_INVALID"])
		return message	

	# Search radioid database for callsign
	url = '''{0}?id={1}'''.format(config.config["DMRID_URL"], callsign)
	session = requests.Session()
	r = session.get(url)

	# If DMR ID is not in database, we can assume it's not linked with a callsign
	if not r:
		message = interactions.Embed(
			title="**__{0}__**".format(config.lang["DMR_ID_REPORT"]),
			description=callsign.upper(),
			color=16711680
		)
		message.add_field(config.lang["ERROR"], config.lang["DMR_UNASSOCIATED"])
	else:
		# If DMR ID does exist, decode it and being parsing
		content = json.loads(r.content.decode("utf-8"))
		if int(content["count"]) == 0:
			# If no data was returned, assume there is no callsign
			message = interactions.Embed(
				title="**__{0}__**".format(config.lang["DMR_ID_REPORT"]),
				description=callsign.upper(),
				color=16711680
			)
			message.add_field(config.lang["ERROR"], config.lang["DMR_UNASSOCIATED"])
		else:
			# Parse callsign
			message = interactions.Embed(
				title="**__{0}__**".format(config.lang["DMR_ID_REPORT"]),
				description=callsign.upper(),
				color=hamyam.callsign_color.callsign_color(content["results"][0]["callsign"])
			)
			message.add_field(config.lang["CALLSIGN"], content["results"][0]["callsign"])
			# If there's more than one DMR ID, add a note about it
			if int(content["count"]) > 1:
				message.add_field(config.lang["NOTE"], config.lang["DMR_MULTICALL"])
			ids = str()
			count = content["count"]
			# Add all DMR IDs to the message
			for item in range(count):
				ids += str(content["results"][item]["id"])
				if item != (count-1):
					ids += ", "
			if int(content["count"]) > 1:
				message.add_field(config.lang["DMR_PLURAL"], ids)
			else:
				# Support for proper pluralization
				message.add_field(config.lang["DMR_ID"], ids)
			# Grab the rest of the info from the RadioID database
			message.add_field(config.lang["NAME"], content["results"][0]["fname"] + " " + content["results"][0]["surname"])
			message.add_field(config.lang["COUNTRY"], content["results"][0]["country"])
			loc = content["results"][0]["city"]
			if content["results"][0]["state"] != "":
				loc += ", " + content["results"][0]["state"]
			message.add_field(config.lang["LOCATION"], loc)

	return message
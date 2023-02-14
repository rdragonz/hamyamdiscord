import interactions
import requests
import json
import hamyam.callsign_color
import hamyam.escapeChars

def dmr_by_call(callsign, config):
	# Obtain callsign from DMR ID
	# Takes: Callsign
	# Returns: Interactions embed format containing callsign report

	# Quick validity check and error message
	callsign = hamyam.escapeChars.escapeChars(callsign)
	
	if not callsign.isalnum():
		message = interactions.Embed(
			title="**__INPUT ERROR__**",
			color=16711680
		)
		message.add_field("Error", "An error was encountered with your input. Please run `/help` for more information on command usage.")
		return message

	message = interactions.Embed(
		title="**__DMR ID Report__**",
		description=callsign.upper(),
		color=hamyam.callsign_color.callsign_color(callsign.upper())
	)

	# Search radioid database for callsign
	if len(callsign) < 3 or len(callsign) >= 15:
		message.add_field("Error", "This callsign does not appear to be valid.")
		return message	
	url = '''{0}?callsign={1}'''.format(config.config["DMRID_URL"], callsign)
	session = requests.Session()
	r = session.get(url)
	
	# If DMR ID is not in database, we can assume it's not linked with a callsign
	if not r:
		message.add_field("Error", "This callsign is not associated with a DMR ID.")
	else:
		content = json.loads(r.content.decode("utf-8"))
		if int(content["count"]) == 0:
			# If no data was returned, assume there is no callsign
			message.add_field("Error", "This callsign is not associated with a DMR ID.")
		# If DMR ID does exist, decode it and being parsing
		else:
			# Parse callsign
			if int(content["count"]) > 1:
				message.add_field("Note", "This callsign is associated with multiple DMR IDs")
			# If there's more than one DMR ID, add a note about it
			ids = str()
			count = content["count"]
			# Add all DMRIDs to the results
			for item in range(count):
				ids += str(content["results"][item]["id"])
				if item != (count-1):
					ids += ", "
			if int(content["count"]) > 1:
				# Support for proper pluralization
				message.add_field("DMR IDs", ids)
			else:
				message.add_field("DMR ID", ids)
			# Grab the rest of the information from the RadioID database
			message.add_field("Name", content["results"][0]["fname"] + " " + content["results"][0]["surname"])
			message.add_field("Country", content["results"][0]["country"])
			loc = content["results"][0]["city"]
			if content["results"][0]["state"] != "":
				loc += ", " + content["results"][0]["state"]
			message.add_field("Location", loc)

	return message
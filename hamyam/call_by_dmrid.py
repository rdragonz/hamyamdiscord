import interactions
import requests
import json
import hamyam.callsign_color

def call_by_dmrid(callsign, config):
	# Obtain callsign from DMR ID
	# Takes: DMR ID
	# Returns: Interactions embed format containing callsign report

	# Quick validity check and error message
	if len(callsign) != 7:
		message = interactions.Embed(
			title="**__DMR ID Report__**",
			description=callsign.upper(),
			color=16711680
		)
		message.add_field("Error", "This DMR ID does not appear to be valid.")
		return message	

	# Search radioid database for callsign
	url = '''{0}?id={1}'''.format(config.config["DMRID_URL"], callsign)
	session = requests.Session()
	r = session.get(url)

	# If DMR ID is not in database, we can assume it's not linked with a callsign
	if not r:
		message = interactions.Embed(
			title="**__DMR ID Report__**",
			description=callsign.upper(),
			color=16711680
		)
		message.add_field("Error", "This DMR ID is not associated with a callsign.")
	else:
		# If DMR ID does exist, decode it and being parsing
		content = json.loads(r.content.decode("utf-8"))
		if int(content["count"]) == 0:
			# If no data was returned, assume there is no callsign
			message = interactions.Embed(
				title="**__DMR ID Report__**",
				description=callsign.upper(),
				color=16711680
			)
			message.add_field("Error", "This DMR ID is not associated with a callsign.")
		else:
			# Parse callsign
			message = interactions.Embed(
				title="**__DMR ID Report__**",
				description=callsign.upper(),
				color=hamyam.callsign_color.callsign_color(content["results"][0]["callsign"])
			)
			message.add_field("Callsign", content["results"][0]["callsign"])
			# If there's more than one DMR ID, add a note about it
			if int(content["count"]) > 1:
				message.add_field("Note", "This callsign is associated with multiple DMR IDs")
			ids = str()
			count = content["count"]
			# Add all DMR IDs to the message
			for item in range(count):
				ids += str(content["results"][item]["id"])
				if item != (count-1):
					ids += ", "
			if int(content["count"]) > 1:
				message.add_field("DMR IDs", ids)
			else:
				# Support for proper pluralization
				message.add_field("DMR ID", ids)
			# Grab the rest of the info from the RadioID database
			message.add_field("Name", content["results"][0]["fname"] + " " + content["results"][0]["surname"])
			message.add_field("Country", content["results"][0]["country"])
			loc = content["results"][0]["city"]
			if content["results"][0]["state"] != "":
				loc += ", " + content["results"][0]["state"]
			message.add_field("Location", loc)

	return message
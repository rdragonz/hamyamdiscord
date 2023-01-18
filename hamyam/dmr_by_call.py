import interactions
import requests
import json
import hamyam.callsign_color

def dmr_by_call(callsign, config):
	message = interactions.Embed(
		title="**__DMR ID Report__**",
		description=callsign.upper(),
		color=hamyam.callsign_color.callsign_color(callsign.upper())
	)

	if len(callsign) < 3 or len(callsign) >= 15:
		message.add_field("Error", "This callsign does not appear to be valid.")
		return message	
	url = '''{0}?callsign={1}'''.format(config.config["DMRID_URL"], callsign)
	session = requests.Session()
	r = session.get(url)
	
	if not r:
		message.add_field("Error", "This callsign is not associated with a DMR ID.")
	else:
		content = json.loads(r.content.decode("utf-8"))
		if int(content["count"]) == 0:
			message.add_field("Error", "This callsign is not associated with a DMR ID.")
		else:
			if int(content["count"]) > 1:
				message.add_field("Note", "This callsign is associated with multiple DMR IDs")
			ids = str()
			count = content["count"]
			for item in range(count):
				ids += str(content["results"][item]["id"])
				if item != (count-1):
					ids += ", "
			if int(content["count"]) > 1:
				message.add_field("DMR IDs", ids)
			else:
				message.add_field("DMR ID", ids)
			message.add_field("Name", content["results"][0]["fname"] + " " + content["results"][0]["surname"])
			message.add_field("Country", content["results"][0]["country"])
			loc = content["results"][0]["city"]
			if content["results"][0]["state"] != "":
				loc += ", " + content["results"][0]["state"]
			message.add_field("Location", loc)

	return message
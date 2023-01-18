import interactions
import requests
import json
import hamyam.callsign_color

def call_by_dmrid(callsign, config):
	if len(callsign) != 7:
		message = interactions.Embed(
			title="**__DMR ID Report__**",
			description=callsign.upper(),
			color=16711680
		)
		message.add_field("Error", "This DMR ID does not appear to be valid.")
		return message	
	url = '''{0}?id={1}'''.format(config.config["DMRID_URL"], callsign)
	session = requests.Session()
	r = session.get(url)

	if not r:
		message = interactions.Embed(
			title="**__DMR ID Report__**",
			description=callsign.upper(),
			color=16711680
		)
		message.add_field("Error", "This DMR ID is not associated with a callsign.")
	else:
		content = json.loads(r.content.decode("utf-8"))
		if int(content["count"]) == 0:
			message = interactions.Embed(
				title="**__DMR ID Report__**",
				description=callsign.upper(),
				color=16711680
			)
			message.add_field("Error", "This DMR ID is not associated with a callsign.")
		else:
			message = interactions.Embed(
				title="**__DMR ID Report__**",
				description=callsign.upper(),
				color=hamyam.callsign_color.callsign_color(content["results"][0]["callsign"])
			)
			message.add_field("Callsign", content["results"][0]["callsign"])
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
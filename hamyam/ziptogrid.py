import interactions
import zipcodes
import maidenhead as mh

def ziptogrid(zipcode, config):
	# Quick validity check
	message = interactions.Embed(
		title="**__Zipcode to Gridsquare__**",
		description=zipcode,
		color=7368816
	)
	try:
		int(zipcode)

	except ValueError:
		message.add_field("Error", "The entered Zipcode does not appear to be a valid United States Zipcode.")
		return message

	if len(zipcode) != 5:
		message.add_field("Error", "The entered Zipcode does not appear to be a valid United States Zipcode.")
		return message

	try:
		zipParsed = zipcodes.matching(zipcode)
		if len(zipParsed) == 0:
			message.add_field("Error", "The entered Zipcode was unable to be located. Is it a valid United States Zipcode?")
			return message

	except ValueError:
		message.add_field("Error", "The entered Zipcode does not appear to be a valid United States Zipcode.")
		return message
	# Convert to Gridsquare
	lat = float(zipParsed[0]['lat'])
	lon = float(zipParsed[0]['long'])
	state = zipParsed[0]['state']
	city = zipParsed[0]['city']

	gridsquare = mh.to_maiden(lat, lon)

	message.add_field("Location", "{0}, {1} {2}".format(city, state, zipcode))
	message.add_field("Gridsquare", "[{1}]({0}?grid={1})".format(config.config["GRIDSQUARE_URL"], gridsquare))
	message.add_field("Coordinates", "[{0}, {1}]({2}?mlat={0}&mlon={1}&zoom=12)".format(lat, lon, config.config["OSM_URL"]))

	return message
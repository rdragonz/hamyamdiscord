import interactions
import zipcodes
import maidenhead as mh

def ziptogrid(zipcode, config):
	# Convert a United States Zicode to a Maidenhead Gridsquare location
	# Takes: A US Zipcode
	# Returns: interactions Embed object

	message = interactions.Embed(
		title="**__{0}__**".format(config.lang["ZIPTOGRID"]),
		description=zipcode,
		color=7368816
	)
	if len(zipcode) > 250:
		message = interactions.Embed(
			title="**__{0}__**".format(config.lang["INPUT_ERORR"]),
			color=16711680
		)
		message.add_field(config.lang["ERROR"], config.lang["INPUT_ERROR_LONG"])
		return message

	# Quick validity checks
	if not zipcode.isalnum():
		message = interactions.Embed(
			title="**__{0}__**".format(config.lang["ERROR_SERIOUS"]),
			color=16711680
		)
		message.add_field(config.lang["ERROR"], config.lang["ERROR_SERIOUS_LONG"])
		return message
	try:
		int(zipcode) # Make sure the entered Zipcode is only digits
	except ValueError:
		message.add_field(config.lang["ERROR"], config.lang["ZIPCODE_INVALID"])
		return message
	if len(zipcode) != 5:
		# Length check, all US Zipcodes are 5 digits
		message.add_field(config.lang["ERROR"], config.lang["ZIPCODE_INVALID"])
		return message

	try:
		# Search for zipcode
		zipParsed = zipcodes.matching(zipcode)
		if len(zipParsed) == 0:
			# If no zipcode is found, it's probably invalid.
			message.add_field(config.lang["ERROR"], config.lang["ZIPCODE_UNLOCATEABLE"])
			return message
	# Another validity check incase all others failed
	except ValueError:
		message.add_field(config.lang["ERROR"], config.lang["ZIPCODE_INVALID"])
		return message
	# Convert to Gridsquare
	lat = float(zipParsed[0]['lat'])
	lon = float(zipParsed[0]['long'])
	state = zipParsed[0]['state']
	city = zipParsed[0]['city']
	# Convert lat/long to gridsquare
	gridsquare = mh.to_maiden(lat, lon)
	# Create properly formatted interactions embed
	message.add_field(config.lang["LOCATION"], "{0}, {1} {2}".format(city, state, zipcode))
	message.add_field(config.lang["GRIDSQUARE"], "[{1}]({0}?grid={1})".format(config.config["GRIDSQUARE_URL"], gridsquare))
	message.add_field(config.lang["COORDINATES"], "[{0}, {1}]({2}?mlat={0}&mlon={1}&zoom=12)".format(lat, lon, config.config["OSM_URL"]))

	return message
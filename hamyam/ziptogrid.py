import interactions
import zipcodes
import maidenhead as mh

def ziptogrid(zipcode, config):
	# Convert a United States Zicode to a Maidenhead Gridsquare location
	# Takes: A US Zipcode
	# Returns: interactions Embed object

	message = interactions.Embed(
		title="**__Zipcode to Gridsquare__**",
		description=zipcode,
		color=16711680
	)
	if len(zipcode) > 250:
		message = interactions.Embed(
			title="**__SERIOUS ERROR__**",
			color=16711680
		)
		message.add_field("Error", "A serious error has occured. Please submit this as a bug to the [Github Issues Page]({}).".format(config.config["GITHUB_ISSUES_URL"]))
		return message

	# Quick validity checks
	try:
		int(zipcode) # Make sure the entered Zipcode is only digits
	except ValueError:
		message.add_field("Error", "The entered Zipcode does not appear to be a valid United States Zipcode.")
		return message
	if len(zipcode) != 5:
		# Length check, all US Zipcodes are 5 digits
		message.add_field("Error", "The entered Zipcode does not appear to be a valid United States Zipcode.")
		return message

	try:
		# Search for zipcode
		zipParsed = zipcodes.matching(zipcode)
		if len(zipParsed) == 0:
			# If no zipcode is found, it's probably invalid.
			message.add_field("Error", "The entered Zipcode was unable to be located. Is it a valid United States Zipcode?")
			return message
	# Another validity check incase all others failed
	except ValueError:
		message.add_field("Error", "The entered Zipcode does not appear to be a valid United States Zipcode.")
		return message
	# Convert to Gridsquare
	lat = float(zipParsed[0]['lat'])
	lon = float(zipParsed[0]['long'])
	state = zipParsed[0]['state']
	city = zipParsed[0]['city']
	# Convert lat/long to gridsquare
	gridsquare = mh.to_maiden(lat, lon)
	# Create properly formatted interactions embed
	message.add_field("Location", "{0}, {1} {2}".format(city, state, zipcode))
	message.add_field("Gridsquare", "[{1}]({0}?grid={1})".format(config.config["GRIDSQUARE_URL"], gridsquare))
	message.add_field("Coordinates", "[{0}, {1}]({2}?mlat={0}&mlon={1}&zoom=12)".format(lat, lon, config.config["OSM_URL"]))

	return message
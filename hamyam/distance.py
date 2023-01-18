import interactions

import maidenhead as mh
import numpy as np

def distance(mh1, mh2, config):
	# Calculate the distance between two Maidenhead Gridsquares
	# Takes: mh1 and mh2 string values containing maidenhead gridsquares
	# Returns: interactions Embed object

	message = interactions.Embed(
			title="**__Distance__**",
			color=7368816
		)

	# Quick validity check
	if len(mh1) < 4 or len(mh2) < 4 or len(mh1) > 6 or len(mh2) > 6 or not mh1[:2].isalpha() or not mh2[:2].isalpha():
		message.add_field("Error", "Please provide two valid Maidenhead locations.")
		return message
	else:
		# Check for and stylize 6-digit Maidenhead gridsquares
		if len(mh1) != 4:
			mh1_styled = mh1[:2].upper() + mh1[2:4] + mh1[4:].lower()
		else:
			mh1_styled = mh1[:2].upper() + mh1[2:].lower()

		if len(mh1) != 4:
			mh2_styled = mh2[:2].upper() + mh2[2:4] + mh2[4:].lower()
		else:
			mh2_styled = mh2[:2].upper() + mh2[2:].lower()

		message.add_field("Position 1", "[{1}]({0}?grid={1})".format(config.config["GRIDSQUARE_URL"], mh1_styled), inline=True)
		message.add_field("Position 2", "[{1}]({0}?grid={1})".format(config.config["GRIDSQUARE_URL"], mh2_styled), inline=True)

	# Convert input maidenhead values to coordinates
	mh1_gps = mh.to_location(mh1)
	mh2_gps = mh.to_location(mh2)

	# Find haversine distance between locations
	answer = haversine_distance(mh1_gps[0], mh1_gps[1], mh2_gps[0], mh2_gps[1])
	answer_miles = np.round(answer * 0.62137119224, 2)

	message.add_field("Distance", "{0} km ({1} mi)".format(str(answer), str(answer_miles)))

	return message

def haversine_distance(lat1, lon1, lat2, lon2):
	r = 6371
	phi1 = np.radians(lat1)
	phi2 = np.radians(lat2)
	delta_phi = np.radians(lat2 - lat1)
	delta_lambda = np.radians(lon2 - lon1)
	a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
	res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
	return np.round(res, 2)
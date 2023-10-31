import interactions
import requests
import base64
import re

from io import BytesIO

def conditions(config):
	# Return ham band conditions
	# Takes: None
	# Returns: interactions.py embed format

	# Get current band conditions and convert it to base64
	# SPECIALTHANKS: 
	image = requests.get(config.config["CONDITIONS_URL"])
	# Coinvert
	image_b64 = base64.b64encode(image.content).decode("UTF-8")

	image_b64 = re.sub("data:image/jpeg;base64", '', image_b64)

	# Now decode it from base64 to a BaseIO byte stream
	image_bio = BytesIO(base64.b64decode(image_b64).read())
	# And provide that byte stream to the interactions library
	image_int = interactions.Image("conditions.gif", image_bio)

	message = interactions.Embed(
		title="**__{0}__**".format(config.lang["BAND_CONDITIONS"]),
		color=7368816,
		image=image_int,
		fields=[interactions.EmbedField(
			name="",
			value="[{0}]({1})".format(config.lang["SOURCE"], config.config["CONDITIONS_SOURCE_URL"])
		)]
	)

	return message
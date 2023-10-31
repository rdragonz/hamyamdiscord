import interactions
import requests
import base64
import re

from io import BytesIO

def muf(config):
	# Return maximum usable frequency information
	# Takes: None
	# Returns: interactions.py embed format

	# Get current MUF and convert it to base64
	image = requests.get(config.config["MUF_URL"])
	image_b64 = base64.b64encode(image.content)

	print(image_b64)

	# Now decode it from base64 to a BaseIO byte stream
	image_bio = BytesIO(base64.b64decode(re.sub("data:image/jpeg;base64", '', image_b64)))
	# And provide that byte stream to the interactions library
	image_int = interactions.Image("muf.gif", image_bio)

	message = interactions.Embed(
		title="**__{0}__**".format(config.lang["MUF"]),
		color=7368816,
		image=image_int,
		fields=[interactions.EmbedField(
			name="",
			value="[{0}]({1})".format(config.lang["SOURCE"], config.config["CONDITIONS_SOURCE_URL"])
		)]
	)

	return message
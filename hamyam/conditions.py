import interactions, base64, re, requests
from io import BytesIO

def conditions(config):
	# Return ham band conditions
	# Takes: None
	# Returns: interactions.py Image class object, ready to be sent via ctx.send

	# Get current band conditions and convert it to base64
	image = requests.get(config.config["CONDITIONS_URL"])
	image_b64 = base64.b64encode(image.content)
	# Now decode it from base64 to a BaseIO byte stream
	image_bio = BytesIO(base64.b64decode(re.sub("data:image/jpeg;base64", '', image_b64)))
	# And provide that byte stream to the interactions library
	image_int = interactions.Image("conditions.gif", image_bio)

	# Return the image to the caller
	return images_int

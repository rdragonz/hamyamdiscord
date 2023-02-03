import interactions
import requests
import base64
import json

def conditions(config):
	# Return ham band conditions
	# Takes: None
	# Returns: interactions.py embed format

	# Get current band conditions and convert it to base64
	image = requests.get(config.config["CONDITIONS_URL"])
	image_b64 = base64.b64encode(image.content)

	# Upload to Imgur
	headers = {
		'Authorization': 'Client-ID {0}'.format(config.config["IMGUR_CLIENT_ID"])
	}
	payload={
		'image': image_b64
	}
	imgur_response = requests.request("POST", config.config["IMGUR_UPLOAD_URL"], headers=headers, data=payload)

	# Get underlying URL back from Imgur
	data = json.loads(imgur_response.text)
	url = data["data"]["link"]

	message = interactions.Embed(
		title="**__Current Band Conditions__**",
		color=7368816,
		image=interactions.EmbedImageStruct(
			url=url,
			height=148,
			width=460,
		),
		fields=[interactions.EmbedField(
			name="",
			value="[Source]({0})".format(config.config["CONDITIONS_SOURCE_URL"])
		)]
	)

	return message
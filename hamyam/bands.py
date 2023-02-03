import interactions

def bands(config):
	# Return the ARRL ham bands document
	# Takes: None
	# Returns: interactions.py Embed object

	# Set up and return an embed containing the bands document
	message = interactions.Embed(
		title="**__US Ham Radio Bands__**",
		color=7368816,
		image=interactions.EmbedImageStruct(
			url=config.config["BANDS_URL"],
			height=534,
			width=700,
		),
		fields=[interactions.EmbedField(
			name="",
			value="[Download PDF]({0})".format(config.config["BANDS_PDF_URL"])
		)]
	)

	return message
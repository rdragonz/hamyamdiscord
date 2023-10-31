import interactions

def bands(config):
	# Return the ARRL ham bands document
	# Takes: None
	# Returns: interactions.py Embed object

	# Set up and return an embed containing the bands document
	message = interactions.Embed(
		title="**__{0}__**".format(config.lang["US_BANDS"]),
		color=7368816,
		image=interactions.EmbedImageStruct(
			url=config.config["BANDS_URL"],
			height=534,
			width=700,
		),
		fields=[interactions.EmbedField(
			name="",
			value="[{0}]({1})".format(config.lang["PDF_DOWNLOAD"], config.config["BANDS_PDF_URL"])
		)]
	)

	return message
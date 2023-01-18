import hashlib

def callsign_color(callsign):
	# Takes a pre-validated callsign and converts it into a color code usable by discord embeds.

	md5sum = hashlib.md5(callsign.encode("utf-8")).hexdigest() # Convert the callsign into an MD5 sum to generate a unique, repeatable, value for each callsign.
	colorcode = int(md5sum[:6], 16) # Chop off the first 6 characters and convert them to an int
	return colorcode
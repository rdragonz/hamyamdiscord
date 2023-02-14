import requests
import xmltodict

def qrz_lookup(callsign, config):
	# Look up a callsign on QRZ and parse returned XML data
	# Takes: Pre-validated callsign
	# Returns: Dict from XML data

	# Properly format URL, set up session, and get content
	url = '''{0}?username={1}&password={2}'''.format(config.config["QRZ_URL"], config.config["QRZ_USERNAME"], config.config["QRZ_PASSWORD"])
	session = requests.Session()
	r = session.get(url)
	# Process XML to a Python dict
	raw_session = xmltodict.parse(r.content)
	session_key = raw_session.get('QRZDatabase').get('Session').get('Key')
	# Get more information about the processed callsign from QRZ
	url2 = """{0}?s={1}&callsign={2}""".format(config.config["QRZ_URL"], session_key, callsign)
	r2 = session.get(url2)
	# Process XML to another Python dict
	raw = xmltodict.parse(r2.content).get('QRZDatabase')
	ham = raw.get('Callsign')
	return ham
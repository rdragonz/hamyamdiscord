import maidenhead as mh
import numpy as np

def distance(mh1, mh2):
	'''
	calculate the distance between two maidenhead locations
	'''

	error_mh = 'Please provide two valid Maidenhead locations.'

	if len(mh1) < 4 or len(mh2) < 4 or len(mh1) > 6 or len(mh2) > 6 or not mh1[:2].isalpha() or not mh2[:2].isalpha():
		return error_mh

	mh1_gps = mh.to_location(mh1)
	mh2_gps = mh.to_location(mh2)

	answer = haversine_distance(mh1_gps[0], mh1_gps[1], mh2_gps[0], mh2_gps[1])
	answer_miles = np.round(answer * 0.62137119224, 2)

	outs = 'Distance is: {0} km ({1} mi)'.format(str(answer), str(answer_miles))
	return outs

def haversine_distance(lat1, lon1, lat2, lon2):
	r = 6371
	phi1 = np.radians(lat1)
	phi2 = np.radians(lat2)
	delta_phi = np.radians(lat2 - lat1)
	delta_lambda = np.radians(lon2 - lon1)
	a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
	res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
	return np.round(res, 2)
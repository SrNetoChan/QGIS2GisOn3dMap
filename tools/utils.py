def rgba2argb(rgba):
	"""
	Function to convert RGBA color values (red, green, blue, alpha)
	to ARGB (alpha, red, green, blue)

	:param rgba: RGBA string with integers (0-255) separated by commas
	:type rgba: string
	:returns: ARGB string with integers (0-255) separated by commas
	:rtype: string
	"""

	# Create a list with the values inside the string
	band_values = rgba.split(',')
	# Remove alpha values of the end of the list and append it in the beginning
	alpha = band_values.pop()
	band_values.insert(0,alpha)
	# Convert list back to comma separated string
	argb = ",".join(band_values)
	return argb

def mm2px(mm_value):
	"""
	Function to convert units form milimiter to pixels

	:param mm_value: value in milimeter (integer)
	:type mm_value: string
	:returns: Float value in pixels (Float)
	:rtype: string
	"""
	FACTOR = 3.0 # FIXME:: review this values, it may depend of the resolution
	px_value = str(int(float(mm_value) * FACTOR + 0.5)) 

	return px_value 

#testing
print rgba2argb('101,102,103,127')
print mm2px('0.10')
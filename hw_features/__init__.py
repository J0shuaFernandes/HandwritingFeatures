import numpy as np
import math
import cv2
import os

def positive_negative(points):
	a, b = points[0], points[1]
	m = (b[1]-a[1])/(b[0]-a[0])

	if m > 0:
		return True
	else:
		return False

def direction(points):
	a, b = points[0], points[1]
	dy, dx = b[1]-a[1], b[0]-a[1]

	t5 = math.tan( (5*math.pi)/180 ) # vertical
	t60 = math.sqrt(3)/2 # horizontal 
	
	vertical = dy != 0 and abs(dx/dy) < t5
	horizontal = dx != 0 and abs(dy/dx) < t60

	if vertical and not horizontal:  
		return 'vertical'
	
	elif horizontal and not vertical:
		return 'horizontal'

	else:
		return 'zero'

def normalize(arr, t_min, t_max):
    norm_arr = []
    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)   
    for i in arr:
        temp = (((i - min(arr))*diff)/diff_arr) + t_min
        norm_arr.append(temp)
    return norm_arr

def measures_of_pen_pressure(img):
	# grey_level_distribution, threshold value, no_black_pixel
	# get grayscale histogram of image
	t_min, t_max = 0, 1
	hist, bin = np.histogram(img.ravel(),256,[0,255])
	# normalize histogram
	norm_arr = normalize(bin, 0, 1)
	# sum
	gray_level_distribution = (np.sum(norm_arr))/len(norm_arr)    
	# threshold value
	thresh_val, thresh_img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	# no of black pixels
	no_black_pixels = int(np.sum(thresh_img == 0))
	return gray_level_distribution, thresh_val, no_black_pixels

# measures of writing movement
def no_of_contours(img):
	# no of interior and exterior contours
	ret, thresh = cv2.threshold(img, 127, 255, 0)
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	#contours = list(contours)
	#contours.pop(0)
	hierarchy = hierarchy[0]

	interior_contours, exterior_contours = 0, 0 
	for x in list(range(len(contours))):
		current_hierarchy = hierarchy[x]
		current_contour = contours[x]

		if current_hierarchy[3] == 0 or current_hierarchy[3] == -1:
			exterior_contours += 1
		else:
			interior_contours += 1

	return interior_contours, exterior_contours

# measures of stroke formation
def slope_components(img):
	ret, thresh = cv2.threshold(img, 127, 255, 0)
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	#contours = list(contours)
	#contours.pop(0)
	hierarchy = hierarchy[0]

	n_slopes = 0
	n_pos, n_neg = 0, 0
	n_ver, n_hor = 0, 0

	#print('No of contours: {}'.format(len(contours)))
	for c in contours:
		epsilon = 0.018*cv2.arcLength(c, True)
		approx = list(cv2.approxPolyDP(c, epsilon, True))	
		n_slopes = n_slopes + (len(approx)-1)

		slopes = []
		while len(approx) > 1:
			slopes.append([ list((approx[0])[0]), list((approx[1])[0]) ])
			approx.pop(0)

		for slope in slopes:
			if positive_negative(slope):
				n_pos += 1
			else:
				n_neg += 1

			if direction(slope) == 'vertical':
				n_ver += 1
			elif direction(slope) == 'horizontal':
				n_hor += 1

	n_pos, n_neg = round(n_pos/n_slopes, 2), round(n_neg/n_slopes, 2)
	n_ver, n_hor = round(n_ver/n_slopes, 2), round(n_hor/n_slopes, 2)

	return n_pos, n_neg, n_ver, n_hor

def all(img):
	"""
	Extracts all features in the following order:
	1, 2, 3 => gl distribution, gl threshold value, no_black_pixels
	4, 5 => interior Contours, exterior Contours
	6, 7, 8, 9 => avg no of positive negative, vertical, horizontal slopes
	"""
	img = cv2.imread(img,0)

	gl_dist, gl_thresh, no_black_pixels = measures_of_pen_pressure(img)
	int_contours, ext_contours = no_of_contours(img)
	pos, neg, vert, hori = slope_components(img)

	return [gl_dist, gl_thresh, no_black_pixels, int_contours, ext_contours, 
			pos, neg, vert, hori]

if __name__ == '__main__':
	for y in [x for x in os.listdir('imgs/') if x.startswith('the')]:
		print(all_features('imgs/'+y))
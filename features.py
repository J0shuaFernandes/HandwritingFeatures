import matplotlib.pyplot as plt
import numpy as np
import math
import cv2

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
	no_black_pixels = np.sum(thresh_img == 0)
	return gray_level_distribution, thresh_val, no_black_pixels

# measures of writing movement
def no_of_contours(img):
	# no of interior and exterior contours
	ret, thresh = cv2.threshold(img, 127, 255, 0)
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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

# F1   F2  F3   F4 F5 F6   F7   F8   F9   F10 F11
# 0.50 188 184K 15 14 0.31 0.13 0.28 0.28 8.8 25
	
if __name__ == '__main__':
	img = cv2.imread('imgs/the-5.png', 0)
	#edges = cv2.Canny(img,100,200)
	
	ret, thresh = cv2.threshold(img, 127, 255, 0)
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	contours = list(contours)
	contours.pop(0)
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


	print(n_pos/n_slopes, n_neg/n_slopes)
	print(n_ver/n_slopes, n_hor/n_slopes)

		#cv2.drawContours(img, [approx], -1, 0, 2)
		#print('No of points: {}'.format(len(approx)))
		#slope_components(approx)
	


	#n_pos, n_neg = n_pos/slopes, n_neg/slopes
	#n_hor, n_ver = n_hor/slopes, n_ver/slopes
	#print(n_slopes)
	
	cv2.imshow("title", img)	
	cv2.waitKey()
	#print(measures_of_pen_pressure(img))
	#print(no_of_contours(img))
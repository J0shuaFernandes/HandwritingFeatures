import matplotlib.pyplot as plt
import numpy as np
import math
import cv2

class MacroFeatures:
	def __init__(self, img):
		self.ret, self.thresh = cv2.threshold(img, 127, 255, 0)
		self.contours, self.hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		self.hierarchy = self.hierarchy[0]
	
	def normalize(self, arr, t_min, t_max):
	    norm_arr = []
	    diff = t_max - t_min
	    diff_arr = max(arr) - min(arr)   
	    for i in arr:
	        temp = (((i - min(arr))*diff)/diff_arr) + t_min
	        norm_arr.append(temp)
	    return norm_arr

	def measures_of_pen_pressure(self, img):
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

if __name__ == '__main__':
	mf = MacroFeatures()